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

'''
Class that estimates the pose of the Nao based on the accelerometer and gyroscope values.
'''

from ahrs.filters import Mahony, Madgwick, AngularRate
from scipy.spatial.transform import Rotation as R
from .accelerometer import Accelerometer
import numpy as np


class PoseEstimator:

    def __init__(self, robot, time_step, algorithm='madgwick'):
        '''Initializes the pose estimator.'''
        self.time_step_ms = time_step
        self.accelerometer = Accelerometer(robot, time_step, history_steps=2)
        self.gyroscope = robot.getDevice('gyro')
        self.gyroscope.enable(time_step)
        self.time_step = time_step
        self.algorithm = algorithm
        self.time_step_s = self.time_step_ms / 1000.
        self.mahony = Mahony(Dt=self.time_step_s, q0=[1., 0., 0., 0.])
        self.madgwick = Madgwick(Dt=self.time_step_s, q0=[1., 0., 0., 0.])
        self.angular_rate = AngularRate(Dt=self.time_step_s, q0=[1., 0., 0., 0.])
        self.Q = np.array([1., 0., 0., 0.])
        self.euler_angles = np.array([0., 0., 0.])

    def update_pose_estimation(self):
        '''Update the pose estimation depending on the chosen algorithm and return the roll, pitch and yaw.'''
        acc = self.accelerometer.get_new_average()
        acc = np.array(acc)
        acc = self.correct_accelerometer_orientation(acc)
        gyro = self.gyroscope.getValues()
        gyro = np.array(gyro)
        # algorithm list: tilt, mahony, madgwick, angular_rate, manual_angular_rate
        if self.algorithm == 'tilt':
            self.euler_angles = self.get_tilt(acc)
            self.Q = self.roll_pitch_yaw_to_quaternion(self.euler_angles)
        elif self.algorithm == 'mahony':
            self.Q = self.mahony.updateIMU(self.Q, gyr=gyro, acc=acc)
        elif self.algorithm == 'madgwick':
            self.Q = self.madgwick.updateIMU(self.Q, gyr=gyro, acc=acc)
        elif self.algorithm == 'angular_rate':
            self.Q = self.angular_rate.update(self.Q, gyr=gyro)
        elif self.algorithm == 'manual_angular_rate':
            self.Q = self.integrate_gyro(self.Q, gyro)
        else:
            raise Exception('Unknown algorithm: ' + self.algorithm)
        self.euler_angles = self.quaternion_to_roll_pitch_yaw(self.Q)

    def get_roll_pitch_yaw(self):
        '''Return the roll, pitch and yaw.'''
        self.update_pose_estimation()
        return self.euler_angles

    def get_quaternion(self):
        '''Return the quaternion.'''
        self.update_pose_estimation()
        return self.Q

    def correct_accelerometer_orientation(self, acc):
        '''The accelerometer is rotated by 180° in the x axis inside the Nao, so we correct for that.'''
        acc[1] = -acc[1]
        acc[2] = -acc[2]
        return acc

    def from_ahrs_quaternion_convention_to_scipy(self, Q):
        '''Convert a quaternion from the ahrs convention to the Scipy convention.'''
        # [w,x,y,z] -> [x,y,z,w]
        Q_prime = np.array([Q[1], Q[2], Q[3], Q[0]])
        return Q_prime

    def from_scipy_to_ahrs_quaternion_convention(self, Q):
        '''Convert a quaternion from the Scipy convention to the ahrs convention.'''
        # [x,y,z,w] -> [w,x,y,z]
        Q_prime = np.array([Q[3], Q[0], Q[1], Q[2]])
        return Q_prime

    def integrate_gyro(self, current_value, gyro_values):
        '''Compute rotation matrix from gyro rates
        source: https://ahrs.readthedocs.io/en/latest/filters/angular.html
        input: current_value is a quaternion [w,x,y,z]'''
        identity_matrix = np.eye(4, 4)
        gyro_matrix = np.array([[0., -gyro_values[0], -gyro_values[1], -gyro_values[2]],
                                [gyro_values[0], 0., gyro_values[2], -gyro_values[1]],
                                [gyro_values[1], -gyro_values[2], 0., gyro_values[0]],
                                [gyro_values[2], gyro_values[1], -gyro_values[0], 0.]])

        rotation_matrix = self.time_step_s / 2 * gyro_matrix + identity_matrix
        new_quaternion = rotation_matrix @ current_value
        return new_quaternion / np.linalg.norm(new_quaternion)

    def get_tilt(self, acc):
        '''Compute the tilt (roll and pitch) based on the accelerometer values.
        Yaw cannot be computed from the accelerometer alone.'''
        ax, ay, az = acc
        roll = np.arctan2(ay, az)
        pitch = np.arctan2(-ax, np.sqrt(ay**2 + az**2))
        yaw = 0.0
        return np.array([roll, pitch, yaw])

    def quaternion_to_roll_pitch_yaw(self, Q):
        '''Return the roll, pitch and yaw correspondind to the quaternion Q.
        Q is a quaternion [w,x,y,z]'''
        Q = self.from_ahrs_quaternion_convention_to_scipy(Q)
        R_orientation = R.from_quat(Q)
        return R_orientation.as_euler('xyz')

    def roll_pitch_yaw_to_quaternion(self, angles):
        '''Return the quaternion [w,x,y,z] from the euler angles: roll, pitch and yaw.'''
        R_orientation = R.from_euler('xyz', angles)
        Q = R_orientation.as_quat()
        return self.from_scipy_to_ahrs_quaternion_convention(Q)
