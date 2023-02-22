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

"""
Constants for the inverse kinematics code from this paper:
N. Kofinas, “Forward and inverse kinematics for the NAO humanoid robot,” Diploma Thesis,
Technical University of Crete, Greece, 2012,
available at: https://www.cs.umd.edu/~nkofinas/Projects/KofinasThesis.pdf
C++ code available at: https://github.com/kouretes/NAOKinematics
/!\ This code works in millimeters, not meters like Webots
"""

# Constants from paper's C++ code
ShoulderOffsetY = 98.0
ElbowOffsetY = 15.0
UpperArmLength = 105.0
ShoulderOffsetZ = 100.0
LowerArmLength = 57.75
HandOffsetX = 55.95
HandOffsetZ = 12.31
HipOffsetZ = 85.0
HipOffsetY = 50.0
ThighLength = 100.0
TibiaLength = 102.9
FootHeight = 45.11
NeckOffsetZ = 126.5
CameraBottomX = 48.8
CameraBottomZ = 23.81
CameraTopX = 53.9
CameraTopZ = 67.9

# Head Limits
HeadYawHigh = 2.0857
HeadYawLow = -2.0857
HeadPitchHigh = 0.5149
HeadPitchLow = -0.6720

# Left Hand limits
LShoulderPitchHigh = 2.0857
LShoulderPitchLow = -2.0857
LShoulderRollHigh = 1.3265
LShoulderRollLow = -0.3142
LElbowYawHigh = 2.0875
LElbowYawLow = -2.0875
LElbowRollHigh = -0.0349
LElbowRollLow = -1.5446
LWristYawHigh = 1.8238
LWristYawLow = -1.8238

# Right Hand limits
RShoulderPitchHigh = 2.0857
RShoulderPitchLow = -2.0857
RShoulderRollHigh = 0.3142
RShoulderRollLow = -1.3265
RElbowYawHigh = 2.0875
RElbowYawLow = -2.0875
RElbowRollHigh = 1.5446
RElbowRollLow = 0.0349
RWristYawHigh = 1.8238
RWristYawLow = -1.8238

# Left Leg limits
# thetas = [LHipYawPitch, LHipRoll, LHipPitch, LKneePitch, LAnklePitch, LAnkleRoll]
LHipYawPitchHigh = 0.7408
LHipYawPitchLow = -1.1453
LHipRollHigh = 0.7904
LHipRollLow = -0.3794
LHipPitchHigh = 0.4840
LHipPitchLow = -1.7739
LKneePitchHigh = 2.1125
LKneePitchLow = -0.0923
LAnklePitchHigh = 0.9227
LAnklePitchLow = -1.1895
LAnkleRollHigh = 0.7690
LAnkleRollLow = -0.3978

# Left Right limits
RHipYawPitchHigh = 0.7408
RHipYawPitchLow = -1.1453
RHipRollHigh = 0.4147
RHipRollLow = -0.7383
RHipPitchHigh = 0.4856
RHipPitchLow = -1.7723
RKneePitchHigh = 2.1201
RKneePitchLow = -0.1030
RAnklePitchHigh = 0.9320
RAnklePitchLow = -1.1864
RAnkleRollHigh = 0.3886
RAnkleRollLow = -1.1864
