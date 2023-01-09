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

from ikpy.chain import Chain
import numpy as np

class Kinematics():
    """Class that takes care of the computation of the inverse kinematics."""
    IKPY_MAX_ITERATIONS = 4
    def __init__(self):
        self.left_leg_chain = Chain.from_urdf_file(
            '../../protos/nao.urdf',
            base_elements=['base_link', 'LHipYawPitch'],
            active_links_mask=[False, True, True,
                               True, True, True, True, False]
        )

        self.right_leg_chain = Chain.from_urdf_file(
            '../../protos/nao.urdf',
            base_elements=['base_link', 'RHipYawPitch'],
            active_links_mask=[False, True, True,
                               True, True, True, True, False]
        )

        self.left_previous_joints = [0, 0, 0, -0.524, 1.047, -0.524, 0, 0]
        self.right_previous_joints = [0, 0, 0, -0.524, 1.047, -0.524, 0, 0]
    
    def ik_left_leg(self, target_position, target_orientation=np.eye(3)):
        """Computes the inverse kinematics of the left leg.
        
        Args:
            target_position (array[3]): The target position of the left foot.
            target_orientation (array[3, 3]): The target orientation of the left foot as a matrix.
        """
        self.left_previous_joints = self.left_leg_chain.inverse_kinematics(
            target_position,
            target_orientation,
            initial_position=self.left_previous_joints,
            max_iter=self.IKPY_MAX_ITERATIONS,
            orientation_mode='all'
        )
        return self.left_previous_joints
    
    def ik_right_leg(self, target_position, target_orientation=np.eye(3)):
        """Computes the inverse kinematics of the right leg."""
        self.right_previous_joints = self.right_leg_chain.inverse_kinematics(
            target_position,
            target_orientation,
            initial_position=self.right_previous_joints,
            max_iter=self.IKPY_MAX_ITERATIONS,
            orientation_mode='all'
        )
        return self.right_previous_joints
