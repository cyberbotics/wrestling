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

'''Routine to detect a fall and recover from it.'''

from .accelerometer import Accelerometer
from .motion_library import MotionLibrary
from .finite_state_machine import FiniteStateMachine
from .current_motion_manager import CurrentMotionManager


class FallDetection:
    def __init__(self, time_step, robot):
        self.time_step = time_step
        self.robot = robot
        # the Finite State Machine (FSM) is a way of representing a robot's behavior as a sequence of states
        self.fsm = FiniteStateMachine(
            states=['NO_FALL', 'BLOCKING_MOTION', 'FRONT_FALL', 'BACK_FALL', 'SIDE_FALL'],
            initial_state='NO_FALL',
            actions={
                'NO_FALL': self.wait,
                'BLOCKING_MOTION': self.pending,
                'FRONT_FALL': self.front_fall,
                'BACK_FALL': self.back_fall,
                'SIDE_FALL': self.wait
            }
        )
        self.accelerometer = Accelerometer(robot, self.time_step)
        # Shoulder roll motors to recover from a side fall
        self.RShoulderRoll = robot.getDevice('RShoulderRoll')
        self.LShoulderRoll = robot.getDevice('LShoulderRoll')
        self.current_motion = CurrentMotionManager()
        self.library = MotionLibrary()

    def check(self):
        '''Check if the robot has fallen.
        If that is the case, block everything to recover from it.'''
        if self.detect_fall():
            while self.fsm.current_state != 'NO_FALL':
                # block everything and run the recovery motion until the robot is back on its feet
                self.fsm.execute_action()
                self.robot.step(self.time_step)
                self.detect_fall()

    def detect_fall(self):
        '''Detect a fall from the accelerometer and update the FSM state.'''
        self.accelerometer.update_average()
        [acc_x, acc_y, _] = self.accelerometer.get_average()
        fall = False
        if acc_x < -7:
            self.fsm.transition_to('FRONT_FALL')
            fall = True
        elif acc_x > 7:
            self.fsm.transition_to('BACK_FALL')
            fall = True
        if acc_y < -7:
            # Fell to its right, pushing itself on its back
            self.RShoulderRoll.setPosition(-1.2)
            self.fsm.transition_to('SIDE_FALL')
            fall = True
        elif acc_y > 7:
            # Fell to its left, pushing itself on its back
            self.LShoulderRoll.setPosition(1.2)
            self.fsm.transition_to('SIDE_FALL')
            fall = True
        return fall

    def pending(self):
        '''Wait for the current motion to finish before going back to NO_FALL.'''
        if self.current_motion.is_over():
            self.current_motion.set(self.library.get('Stand'))
            self.fsm.transition_to('NO_FALL')

    def front_fall(self):
        self.current_motion.set(self.library.get('GetUpFront'))
        self.fsm.transition_to('BLOCKING_MOTION')

    def back_fall(self):
        self.current_motion.set(self.library.get('GetUpBack'))
        self.fsm.transition_to('BLOCKING_MOTION')

    def wait(self):
        pass
