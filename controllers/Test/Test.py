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

        # arm motors
        self.RShoulderPitch = self.getDevice("RShoulderPitch")
        self.LShoulderPitch = self.getDevice("LShoulderPitch")

        self.RShoulderRoll = self.getDevice("RShoulderRoll")
        self.LShoulderRoll = self.getDevice("LShoulderRoll")

        self.RElbowRoll = self.getDevice("RElbowRoll")
        self.LElbowRoll = self.getDevice("LElbowRoll")

        self.RElbowYaw = self.getDevice("RElbowYaw")
        self.LElbowYaw = self.getDevice("LElbowYaw")

        # leg motors
        self.RHipPitch = self.getDevice("RHipPitch")
        self.LHipPitch = self.getDevice("LHipPitch")

        self.RHipRoll = self.getDevice("RHipRoll")
        self.LHipRoll = self.getDevice("LHipRoll")

        self.RHipYawPitch = self.getDevice("RHipYawPitch")
        self.LHipYawPitch = self.getDevice("LHipYawPitch")

        self.RKneePitch = self.getDevice("RKneePitch")
        self.LKneePitch = self.getDevice("LKneePitch")

        self.RAnklePitch = self.getDevice("RAnklePitch")
        self.LAnklePitch = self.getDevice("LAnklePitch")

        self.RAnkleRoll = self.getDevice("RAnkleRoll")
        self.LAnkleRoll = self.getDevice("LAnkleRoll")

        # load motion files
        self.forwards = Motion('../motions/ForwardLoop.motion')
        self.forwards.setLoop(True)
        self.stand = Motion('../motions/Stand.motion')
        self.standUpFromFront = Motion('../motions/GetUpFront.motion')
        self.standUpFromBack = Motion('../motions/GetUpBack.motion')

    def run(self):
        self.RShoulderPitch.setPosition(1.57)  # arms down
        self.LShoulderPitch.setPosition(1.57)
        self.stand.play()

        while self.step(self.timeStep) != -1:
            t = self.getTime()
            # pseudo moving average
            self.accelerometerAverage = [0.9 * x + 0.1 * y for x, y in zip(self.accelerometerAverage, self.accelerometer.getValues())]
            #print(self.accelerometerAverage)
            if self.accelerometerAverage[0] < -7:
                self.state = State.GET_UP_FRONT
            if self.accelerometerAverage[0] > 7:
                self.state = State.GET_UP_BACK
            self.stateAction(t)

    def stateAction(self, t):
        if self.state == State.IDLE:
            self.idle()
        elif self.state == State.WALK:
            self.walk()
        elif self.state == State.GET_UP_FRONT:
            self.getUpFront(t)
        elif self.state == State.GET_UP_BACK:
            self.getUpBack(t)
    
    def idle(self):
        #if self.stand.isOver():
        #    self.forwards.play()
        pass
    
    def walk(self):
        self.forwards.play()

    def getUpFront(self, time):
        if self.startTime == None:
            self.startTime = time 
        elif self.standUpFromFront.isOver():
            self.state = State.IDLE
            self.startTime = None
            # reset the isOver state
            self.standUpFromFront.play()
            self.standUpFromFront.stop()
            return
        self.standUpFromFront.play()

    def getUpBack(self, time):
        if self.startTime == None:
            self.startTime = time 
        elif self.standUpFromBack.isOver():
            self.state = State.IDLE
            self.startTime = None
            # reset the isOver state
            self.standUpFromBack.play()
            self.standUpFromBack.stop()
            return
        self.standUpFromBack.play()

    def getUpBackOld(self, time):
        if self.startTime == None:
            self.startTime = time        

        #print(f"Running time: {time - self.startTime}")
        if time - self.startTime < 0.5:
            # crouched T shape
            self.RHipPitch.setPosition(-1)
            self.RKneePitch.setPosition(2.11)
            self.RAnklePitch.setPosition(-1.18)
            self.LHipPitch.setPosition(-1)
            self.LKneePitch.setPosition(2.11)
            self.LAnklePitch.setPosition(-1.18)
            self.RShoulderRoll.setPosition(-1.32)
            self.RShoulderPitch.setPosition(1.57)
            self.LShoulderRoll.setPosition(1.32)
            self.LShoulderPitch.setPosition(1.57)
        elif time - self.startTime < 1.0:
            # weight on head and feet
            self.RHipPitch.setPosition(0.48)
            self.RKneePitch.setPosition(1.47)
            self.RAnklePitch.setPosition(0.106)
            self.LHipPitch.setPosition(0.48)
            self.LKneePitch.setPosition(1.47)
            self.LAnklePitch.setPosition(0.106)
        elif time - self.startTime < 1.5:
            # arms behind the back
            self.RShoulderRoll.setPosition(-0.13)
            self.RShoulderPitch.setPosition(2.08)
            self.RElbowRoll.setPosition(1.5)
            self.RElbowYaw.setPosition(-0.2)
            self.LShoulderRoll.setPosition(0.13)
            self.LShoulderPitch.setPosition(2.08)
            self.LElbowRoll.setPosition(-1.5)
            self.LElbowYaw.setPosition(0.2)
        elif time - self.startTime < 2.0:
            # lever action of body on the hands
            self.RHipPitch.setPosition(-1.7)
            self.RKneePitch.setPosition(0.175)
            self.RAnklePitch.setPosition(0.9)
            self.LHipPitch.setPosition(-1.7)
            self.LKneePitch.setPosition(0.175)
            self.LAnklePitch.setPosition(0.9)
        elif time - self.startTime < 2.75:
            # pull body to the front
            self.RHipYawPitch.setPosition(-1.14)
            self.RHipPitch.setPosition(-1.77)
            self.RKneePitch.setPosition(1.8)
            self.RAnklePitch.setPosition(0.7)
            self.LHipYawPitch.setPosition(-1.14)
            self.LHipPitch.setPosition(-1.3)
            self.LKneePitch.setPosition(0)
            self.LAnklePitch.setPosition(0)
            # other hand to help leaning forward
            self.RShoulderRoll.setPosition(-1.23)
            self.RShoulderPitch.setPosition(0)
            self.RElbowRoll.setPosition(0.65)
            # one hand back on the ground
            self.LShoulderRoll.setPosition(0.5)
            self.LElbowRoll.setPosition(-0.34)
        elif time - self.startTime < 4:
            # pull back right leg to put the weight on it
            self.RHipRoll.setPosition(-0.475)
            self.RHipPitch.setPosition(0.1)
            self.RKneePitch.setPosition(2.11)
            self.RAnklePitch.setPosition(-0.9)
            self.RAnkleRoll.setPosition(0.14)
            # left leg straight and pushing back to help leaning forward
            self.LHipYawPitch.setPosition(-0.24)
            self.LHipRoll.setPosition(0.77)
            self.LHipPitch.setPosition(-1.77)
            self.LKneePitch.setPosition(2.11)
            self.LAnklePitch.setPosition(-0.4)
            self.RShoulderRoll.setPosition(0)
            self.RElbowRoll.setPosition(0.83)
        elif time - self.startTime < 4.5:
            # now weight is on right foot, tilt forward the body
            self.LHipPitch.setPosition(-0.9)
            self.LAnklePitch.setPosition(-0.4)
            pass
        #elif time - self.startTime < 5.0:
        #    # stand up
        #    self.RHipYawPitch.setPosition(0)
        #    self.RHipRoll.setPosition(0)
        #    self.RHipPitch.setPosition(-0.524)
        #    self.RKneePitch.setPosition(1.047)
        #    self.RAnklePitch.setPosition(-0.524)
        #    self.RAnkleRoll.setPosition(0)
        #    self.LHipYawPitch.setPosition(0)
        #    self.LHipRoll.setPosition(0)
        #    self.LHipPitch.setPosition(-0.524)
        #    self.LKneePitch.setPosition(1.047)
        #    self.LAnklePitch.setPosition(-0.524)
        #    self.LAnkleRoll.setPosition(0)
        #    # reset arms
        #    self.RShoulderRoll.setPosition(0)
        #    self.RShoulderPitch.setPosition(0)
        #    self.RElbowRoll.setPosition(0)
        #    self.RElbowYaw.setPosition(0)
        #    self.LShoulderRoll.setPosition(0)
        #    self.LShoulderPitch.setPosition(0)
        #    self.LElbowRoll.setPosition(0)
        #    self.LElbowYaw.setPosition(0)
        #elif time - self.startTime < 6.0:
        #    self.state = State.IDLE
        #    self.startTime = None

# create the Robot instance and run main loop
wrestler = Wrestler()
wrestler.run()
