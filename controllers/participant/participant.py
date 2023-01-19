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

"""Minimalist controller example for the Robot Wrestling Tournament.
   Demonstrates how to play a simple motion file."""

from controller import Robot
import sys
sys.path.append('..')
# We provide a set of utilities to help you with the development of your controller. You can find them in the utils folder.
# If you want to see a list of examples that use them, you can go to https://github.com/cyberbotics/wrestling#demo-robot-controllers

# from utils.accelerometer import Accelerometer
# from utils.camera import Camera
# from utils.current_motion_manager import CurrentMotionManager
# from utils.ellipsoid_gait_generator import EllipsoidGaitGenerator
# from utils.fall_detection import FallDetection
# from utils.finite_state_machine import FiniteStateMachine
# from utils.gait_manager import GaitManager
# from utils.image_processing import ImageProcessing as IP
# from utils.kinematics import Kinematics
from utils.motion_library import MotionLibrary
# from utils.pose_estimator import PoseEstimator
# from utils.running_average import RunningAverage


class Wrestler (Robot):
    def run(self):
        # to load all the motions from the motion folder, we use the Motion_library class:
        motion_library = MotionLibrary()
        # retrieves the WorldInfo.basicTimeTime (ms) from the world file
        time_step = int(self.getBasicTimeStep())
        while self.step(time_step) != -1:  # mandatory function to make the simulation run
            motion_library.play('Backwards')


# create the Robot instance and run main loop
wrestler = Wrestler()
wrestler.run()
