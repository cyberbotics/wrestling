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

from .ellipsoid_gait_generator import EllipsoidGaitGenerator
from .kinematics import Kinematics


class GaitManager():
    """Connects the Kinematics class and the EllipsoidGaitGenerator class together to have a simple gait interface."""

    def __init__(self, robot, time_step):
        self.time_step = time_step
        self.gait_generator = EllipsoidGaitGenerator(robot, self.time_step)
        self.kinematics = Kinematics()
        joints = ['HipYawPitch', 'HipRoll', 'HipPitch', 'KneePitch', 'AnklePitch', 'AnkleRoll']
        self.L_leg_motors = []
        for joint in joints:
            motor = robot.getDevice(f'L{joint}')
            position_sensor = motor.getPositionSensor()
            position_sensor.enable(time_step)
            self.L_leg_motors.append(motor)

        self.R_leg_motors = []
        for joint in joints:
            motor = robot.getDevice(f'R{joint}')
            position_sensor = motor.getPositionSensor()
            position_sensor.enable(time_step)
            self.R_leg_motors.append(motor)

    def update_theta(self):
        self.gait_generator.update_theta()

    def command_to_motors(self, desired_radius=None, heading_angle=0):
        """
        Compute the desired positions of the robot's legs for a desired radius (R > 0 is a right turn)
        and a desired heading angle (in radians. 0 is straight on, > 0 is turning left).
        Send the commands to the motors.
        """
        if not desired_radius:
            desired_radius = 1e3
        x, y, z, yaw = self.gait_generator.compute_leg_position(
            is_left=False, desired_radius=desired_radius, heading_angle=heading_angle)
        right_target_commands = self.kinematics.inverse_leg(x * 1e3, y * 1e3, z * 1e3, 0, 0, yaw, is_left=False)
        for command, motor in zip(right_target_commands, self.R_leg_motors):
            motor.setPosition(command)

        x, y, z, yaw = self.gait_generator.compute_leg_position(
            is_left=True, desired_radius=desired_radius, heading_angle=heading_angle)
        left_target_commands = self.kinematics.inverse_leg(x * 1e3, y * 1e3, z * 1e3, 0, 0, yaw, is_left=True)
        for command, motor in zip(left_target_commands, self.L_leg_motors):
            motor.setPosition(command)
