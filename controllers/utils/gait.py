# Copyright 1996-2023 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from scipy.spatial.transform import Rotation as R
from .kinematics import Kinematics

class Ellipsoid_gait_generator():
    """Simple gait generator, based on an ellipsoid path.
    Derived from chapter 2 in paper:
    G. Endo, J. Morimoto, T. Matsubara, J. Nakanishi, and G. Cheng,
    “Learning CPG-based Biped Locomotion with a Policy Gradient Method: Application to a Humanoid Robot,”
    The International Journal of Robotics Research, vol. 27, no. 2, pp. 213-228,
    Feb. 2008, doi: 10.1177/0278364907084980.
    """
    def __init__(self, robot, time_step):
        self.robot = robot
        self.time_step = time_step
        self.theta = 0 # angle of the ellipsoid path
        self.imu = robot.getDevice('inertial unit')
        self.imu.enable(self.time_step)
        self.right_foot_sensor = robot.getDevice('RFsr')
        self.right_foot_sensor.enable(self.time_step)
        self.left_foot_sensor = robot.getDevice('LFsr')
        self.left_foot_sensor.enable(self.time_step)

        self.roll_reflex_factor = 5e-4 # h_VSR in paper
        self.force_reflex_factor = 3e-3/(5.305*9.81) # h_ER/(mass*gravity) in paper
        self.robot_height_offset = 0.31 # desired height for the robot's center of mass
        self.lateral_leg_offset = 0.05 # distance between the center of mass and the feet
        self.step_period = 0.4 # time to complete one step
        self.step_length = 0.045 # distance traveled by the feet in one step
        self.step_height = 0.04 # height of the ellipsoid path
        self.step_penetration = 0.005 # depth of the ellipsoid path
        self.calibration_factor = 0.93
    
    def update_theta(self):
        """Update the angle of the ellipsoid path and clip it to [-pi, pi]"""
        self.theta = -(2 * np.pi * self.robot.getTime() / self.step_period) % (2 * np.pi) - np.pi

    def compute_leg_position(self, is_right, desired_radius=1e3, heading_angle=0):
        """Compute the desired positions of a leg for a desired radius (R > 0 is a right turn)."""
        desired_radius *= self.calibration_factor # actual radius is bigger than the desired one, so we "correct" it
        factor = 1 if is_right else -1 # the math is the same for both legs, except for some signs

        amplitude_x = self.step_length * (desired_radius - factor * self.lateral_leg_offset) / desired_radius
        x = factor * amplitude_x * np.cos(self.theta)
        
        # ellipsoid path
        amplitude_z = self.step_penetration if factor * self.theta < 0 else self.step_height
        # vestibulospinal reflex: corrects the robot's roll
        amplitude_z += factor * self.imu.getRollPitchYaw()[0] * self.roll_reflex_factor
        # extensor response: pushes on the leg when it is on the ground
        force_values = self.right_foot_sensor.getValues() if is_right else self.left_foot_sensor.getValues()
        force_magnitude = np.linalg.norm(np.array([force_values[0], force_values[1], force_values[2]]))
        if force_magnitude > 5:
            amplitude_z += self.force_reflex_factor * force_magnitude
        z = factor * amplitude_z * np.sin(self.theta) - self.robot_height_offset
        
        yaw = - x/(desired_radius - factor * self.lateral_leg_offset)
        y = - (1 - np.cos(yaw)) * (desired_radius - factor * self.lateral_leg_offset)
        if heading_angle != 0:
            x, y = rotate(x, y, heading_angle)
        y += - factor * self.lateral_leg_offset
        return x, y, z, yaw

class Gait_manager():
    """Connects the Kinematics class and the Ellipsoid_gait_generator class together to have a simple gait interface."""
    def __init__(self, robot, time_step):
        self.time_step = time_step
        self.kinematics = Kinematics()
        self.gait_generator = Ellipsoid_gait_generator(robot, self.time_step)
        self.L_leg_motors = []
        for link in self.kinematics.left_leg_chain.links:
            if link.name != 'Base link' and link.name != "LLeg_effector_fixedjoint":
                motor = robot.getDevice(link.name)
                position_sensor = motor.getPositionSensor()
                position_sensor.enable(time_step)
                self.L_leg_motors.append(motor)
        
        self.R_leg_motors = []
        for link in self.kinematics.right_leg_chain.links:
            if link.name != 'Base link' and link.name != "RLeg_effector_fixedjoint":
                motor = robot.getDevice(link.name)
                position_sensor = motor.getPositionSensor()
                position_sensor.enable(time_step)
                self.R_leg_motors.append(motor)
    
    def update_theta(self):
        self.gait_generator.update_theta()
    
    def command_to_motors(self, desired_radius=1e3, heading_angle=0):
        """
        Compute the desired positions of the robot's legs for a desired radius (R > 0 is a right turn) and a desired heading angle (in radians).
        Send the commands to the motors.
        """
        x, y, z, yaw = self.gait_generator.compute_leg_position(is_right=True, desired_radius=desired_radius, heading_angle=heading_angle)
        right_target_commands = self.kinematics.ik_right_leg(
            [x, y, z],
            R.from_rotvec(yaw * np.array([0, 0, 1])).as_matrix()
        )
        for command, motor in zip(right_target_commands[1:], self.R_leg_motors):
            motor.setPosition(command)

        x, y, z, yaw = self.gait_generator.compute_leg_position(is_right=False, desired_radius=desired_radius, heading_angle=heading_angle)
        left_target_commands = self.kinematics.ik_left_leg(
            [x, y, z],
            R.from_rotvec(yaw * np.array([0, 0, 1])).as_matrix()
        )
        for command, motor in zip(left_target_commands[1:], self.L_leg_motors):
            motor.setPosition(command)

def rotate(x, y, angle):
    """Rotate a point by a given angle."""
    return x * np.cos(angle) - y * np.sin(angle), x * np.sin(angle) + y * np.cos(angle)
