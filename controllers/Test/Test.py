# Copyright 1996-2022 Cyberbotics Ltd.
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

"""Controller example for the Robot Wrestling Tournament.
   Demonstrates how to access sensors and actuators"""

from controller import Robot, Motion


class Wrestler (Robot):
    def __init__(self):
        Robot.__init__(self)
        self.timeStep = int(self.getBasicTimeStep())  # retrieves the WorldInfo.basicTimeTime (ms) from the world file

        self.startTime = -1

        # camera
        #self.cameraTop = self.getDevice("CameraTop")
        #self.cameraBottom = self.getDevice("CameraBottom")
        #self.cameraTop.enable(4 * self.timeStep)
        #self.cameraBottom.enable(4 * self.timeStep)

        # accelerometer
        self.accelerometer = self.getDevice("accelerometer")

        # there are 7 controllable LEDs on the NAO robot, but we will use only the ones in the eyes
        self.leds = []
        self.leds.append(self.getDevice('Face/Led/Right'))
        self.leds.append(self.getDevice('Face/Led/Left'))

        # shoulder pitch motors
        self.RShoulderPitch = self.getDevice("RShoulderPitch")
        self.LShoulderPitch = self.getDevice("LShoulderPitch")

        # shoulder roll motors
        self.RShoulderRoll = self.getDevice("RShoulderRoll")
        self.LShoulderRoll = self.getDevice("LShoulderRoll")

        # elbow roll motors
        self.RElbowRoll = self.getDevice("RElbowRoll")
        self.LElbowRoll = self.getDevice("LElbowRoll")

        # hip pitch motors
        self.RHipPitch = self.getDevice("RHipPitch")
        self.LHipPitch = self.getDevice("LHipPitch")

        # hip roll motors
        self.RHipRoll = self.getDevice("RHipRoll")
        self.LHipRoll = self.getDevice("LHipRoll")

        # hip yaw pitch motors
        self.RHipYawPitch = self.getDevice("RHipYawPitch")
        self.LHipYawPitch = self.getDevice("LHipYawPitch")

        # knee pitch motors
        self.RKneePitch = self.getDevice("RKneePitch")
        self.LKneePitch = self.getDevice("LKneePitch")

        # ankle pitch motors
        self.RAnklePitch = self.getDevice("RAnklePitch")
        self.LAnklePitch = self.getDevice("LAnklePitch")

        # load motion files
        self.forwards = Motion('motions/Forwards50.motion')
        self.standUpFromFront = Motion('motions/StandUpFromFront.motion')

    def run(self):
        self.RShoulderPitch.setPosition(1.57)  # arms down
        self.LShoulderPitch.setPosition(1.57)

        while self.step(self.timeStep) != -1:
            t = self.getTime()
            self.getUp(t)
    
    def getUp(self, time):
        if self.startTime == -1:
            self.startTime = time
        #print(f"Running time: {time - self.startTime}")
        if time - self.startTime < 0.5:
            # face plant:
            # crouching
            self.RHipPitch.setPosition(-1)
            self.RKneePitch.setPosition(2.11)
            self.RAnklePitch.setPosition(-1.18)
            self.LHipPitch.setPosition(-1)
            self.LKneePitch.setPosition(2.11)
            self.LAnklePitch.setPosition(-1.18)
            # arms to the sides
            self.RShoulderRoll.setPosition(-1.32)
            self.RShoulderPitch.setPosition(-1.57)
            self.LShoulderRoll.setPosition(1.32)
            self.LShoulderPitch.setPosition(-1.57)
        elif time - self.startTime < 1.0:
            # arms up
            self.RShoulderRoll.setPosition(-0.5)
            self.LShoulderRoll.setPosition(0.5)
        elif time - self.startTime < 1.5:
            # push with arms and hips yaw pitch
            self.RShoulderPitch.setPosition(0)
            self.RElbowRoll.setPosition(1.54)
            self.RHipYawPitch.setPosition(-1.14)
            self.LShoulderPitch.setPosition(0)
            self.LElbowRoll.setPosition(-1.54)
            self.LHipYawPitch.setPosition(-1.14)
        elif time - self.startTime < 2.0:
            # pop up with arms
            self.RShoulderRoll.setPosition(0)
            self.RElbowRoll.setPosition(0)
            self.LShoulderRoll.setPosition(0)
            self.LElbowRoll.setPosition(0)
        elif time - self.startTime < 2.5:
            # feet to the ground
            self.RHipRoll.setPosition(0.37)
            self.LHipRoll.setPosition(-0.37)
        elif time - self.startTime < 3.0:
            # extend left leg with foot still on the ground
            # the weight of the robot will be on the right foot
            self.LKneePitch.setPosition(0)
            self.LHipYawPitch.setPosition(-0.6)
            self.LHipPitch.setPosition(-1.7)
            self.LAnklePitch.setPosition(0.9)
        elif time - self.startTime < 3.5:
            # swivel the right leg to put the weight on both legs
            self.RAnklePitch.setPosition(-0.5)
            self.RHipPitch.setPosition(-1.7)
        elif time - self.startTime < 4.0:
            # pull torso back up
            self.RHipYawPitch.setPosition(-0.5)
            self.LHipYawPitch.setPosition(-0.2)
            self.LHipRoll.setPosition(0.6)

        #elif time - self.startTime < 3.0:
        #    # on all fours
        #    self.RHipPitch.setPosition(-1.77)
        #    self.RHipYawPitch.setPosition(0)
        #    self.RHipRoll.setPosition(0)
        #    self.RKneePitch.setPosition(1.8)
        #    self.LHipPitch.setPosition(-1.77)
        #    self.LHipYawPitch.setPosition(0)
        #    self.LHipRoll.setPosition(0)
        #    self.LKneePitch.setPosition(1.8)
        #elif time - self.startTime < 3.5:
        #    # arms back
        #    self.RShoulderPitch.setPosition(1.57)
        #    self.LShoulderPitch.setPosition(1.57)
        #    # knees crouched even more
        #    self.RKneePitch.setPosition(2.11)
        #    self.LKneePitch.setPosition(2.11)
        #    # kick back with hips
        #    self.RHipPitch.setPosition(-0.8)
        #    self.LHipPitch.setPosition(-0.8)

# create the Robot instance and run main loop
wrestler = Wrestler()
wrestler.run()
