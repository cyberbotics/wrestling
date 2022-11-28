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
from enum import Enum

State = Enum('State', ['IDLE', 'WALK', 'GET_UP_FRONT', 'GET_UP_BACK'])

class Wrestler (Robot):
    def __init__(self):
        Robot.__init__(self)
        self.state = State.IDLE
        self.startTime = None
        self.timeStep = int(self.getBasicTimeStep())  # retrieves the WorldInfo.basicTimeTime (ms) from the world file

        # camera
        #self.cameraTop = self.getDevice("CameraTop")
        #self.cameraBottom = self.getDevice("CameraBottom")
        #self.cameraTop.enable(4 * self.timeStep)
        #self.cameraBottom.enable(4 * self.timeStep)

        # accelerometer
        self.accelerometer = self.getDevice("accelerometer")
        self.accelerometer.enable(self.timeStep)
        self.accelerometerAverage = [0]*3

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

        # ankle roll motors
        self.RAnkleRoll = self.getDevice("RAnkleRoll")
        self.LAnkleRoll = self.getDevice("LAnkleRoll")

        # load motion files
        self.forwards = Motion('../motions/ForwardLoop.motion')
        self.forwards.setLoop(True)
        self.stand = Motion('../motions/Stand.motion')
        self.standUpFromFront = Motion('../motions/GetUpFront.motion')
        print(self.standUpFromFront.isValid())

        self.getDevice("LHipYawPitchS").enable(self.timeStep)
        self.getDevice("LHipRollS").enable(self.timeStep)
        self.getDevice("LHipPitchS").enable(self.timeStep)
        self.getDevice("LKneePitchS").enable(self.timeStep)
        self.getDevice("LAnklePitchS").enable(self.timeStep)
        self.getDevice("LAnkleRollS").enable(self.timeStep)
        self.getDevice("RHipYawPitchS").enable(self.timeStep)
        self.getDevice("RHipRollS").enable(self.timeStep)
        self.getDevice("RHipPitchS").enable(self.timeStep)
        self.getDevice("RKneePitchS").enable(self.timeStep)
        self.getDevice("RAnklePitchS").enable(self.timeStep)
        self.getDevice("RAnkleRollS").enable(self.timeStep)
        self.getDevice("LShoulderRollS").enable(self.timeStep)
        self.getDevice("LShoulderPitchS").enable(self.timeStep)
        self.getDevice("LElbowRollS").enable(self.timeStep)
        self.getDevice("RShoulderRollS").enable(self.timeStep)
        self.getDevice("RShoulderPitchS").enable(self.timeStep)
        self.getDevice("RElbowRollS").enable(self.timeStep)

    def run(self):
        self.RShoulderPitch.setPosition(1.57)  # arms down
        self.LShoulderPitch.setPosition(1.57)
        self.stand.play()

        while self.step(self.timeStep) != -1:
            t = self.getTime()
            self.accelerometerAverage = [0.9 * x + 0.1 * y for x, y in zip(self.accelerometerAverage, self.accelerometer.getValues())]
            #print("accelerometer: ", self.accelerometer.getValues())
            if self.accelerometerAverage[0] < -5:
                self.state = State.GET_UP_FRONT
            if self.accelerometerAverage[0] > 5:
                self.state = State.GET_UP_BACK
            self.stateAction(t)

    def stateAction(self, t):
        if self.state == State.IDLE:
            self.idle()
        elif self.state == State.GET_UP_FRONT:
            self.getUpFront(t)
        elif self.state == State.WALK:
            self.walk()
    
    def idle(self):
        #if self.stand.isOver():
        #    self.forwards.play()
        pass
    
    def walk(self):
        self.forwards.play()

    def getUpFront(self, t):
        self.standUpFromFront.play()

# create the Robot instance and run main loop
wrestler = Wrestler()
wrestler.run()
