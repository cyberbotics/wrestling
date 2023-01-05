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

"""Referee supervisor controller for the Robot Wrestling Tournament."""

import math
import os
from controller import Supervisor, AnsiCodes


class Referee (Supervisor):
    def init(self):
        # create an array of size [3][10] filled in with zeros
        self.digit = [[0] * 10 for i in range(3)]
        for j in range(3):
            for i in range(10):
                self.digit[j][i] = self.getDevice('digit ' + str(j) + str(i))
        self.current_digit = [0, 0, 0]  # 0:00
        self.robot = [0] * 2
        self.robot[0] = self.getFromDef('WRESTLER_RED')
        self.robot[1] = self.getFromDef('WRESTLER_BLUE')
        self.min = [[0] * 3 for i in range(2)]
        self.max = [[0] * 3 for i in range(2)]
        for i in range(2):
            self.min[i] = self.robot[i].getPosition()
            self.max[i] = self.robot[i].getPosition()
        self.coverage = [0] * 2
        self.ko_count = [0] * 2
        # linear motors on the side of the ring to display the coverage visually
        self.indicator = [0] * 2
        self.indicator[0] = self.getDevice('red indicator')
        self.indicator[1] = self.getDevice('blue indicator')

    def display_time(self, minutes, seconds):
        for j in range(3):
            self.digit[j][self.current_digit[j]].setPosition(1000)  # far away, not visible
        self.current_digit[0] = minutes
        self.current_digit[1] = seconds // 10
        self.current_digit[2] = seconds % 10
        for j in range(3):
            self.digit[j][self.current_digit[j]].setPosition(0)  # visible

    def run(self, CI):
        # Performance output used by automated CI script
        game_duration = 3 * 60 * 1000  # a game lasts 3 minutes
        # retrieves the WorldInfo.basicTimeTime (ms) from the world file
        time_step = int(self.getBasicTimeStep())
        time = 0
        seconds = -1
        ko = -1
        while True:
            if time % 200 == 0:
                s = int(time / 1000) % 60
                if seconds != s:
                    seconds = s
                    minutes = int(time / 60000)
                    self.display_time(minutes, seconds)
                box = [0] * 3
                for i in range(2):
                    position = self.robot[i].getPosition()
                    if abs(position[0]) < 1 and abs(position[1]) < 1:  # inside the ring
                        coverage = 0
                        for j in range(3):
                            if position[j] < self.min[i][j]:
                                self.min[i][j] = position[j]
                            elif position[j] > self.max[i][j]:
                                self.max[i][j] = position[j]
                            box[j] = self.max[i][j] - self.min[i][j]
                            coverage += box[j] * box[j]
                        coverage = math.sqrt(coverage)
                        self.coverage[i] = coverage
                        self.indicator[i].setPosition(self.coverage[i] / 7)
                    if position[2] < 0.75:  # low position threshold
                        self.ko_count[i] = self.ko_count[i] + 200
                        if self.ko_count[i] > 10000:  # 10 seconds
                            ko = i
                    else:
                        self.ko_count[i] = 0
                if self.ko_count[0] > self.ko_count[1]:
                    print(AnsiCodes.CLEAR_SCREEN)
                    print('Red KO: %d' % (10 - self.ko_count[0] // 1000))
                elif self.ko_count[1] > self.ko_count[0]:
                    print(AnsiCodes.CLEAR_SCREEN)
                    print('Blue KO: %d' % (10 - self.ko_count[1] // 1000))
            if self.step(time_step) == -1 or time > game_duration or ko != -1:
                break
            time += time_step
        if ko == 0:
            print('performance:0' if CI else 'Red is KO. Blue wins!')
            print('Red is KO. Blue wins!')
        elif ko == 1:
            print('performance:1' if CI else 'Blue is KO. Red wins!')
            print('Blue is KO. Red wins!')
        # in case of coverage equality, red wins
        elif self.coverage[0] >= self.coverage[1]:
            print('performance:1' if CI else 'Red wins coverage: %s >= %s' % (self.coverage[0], self.coverage[1]))
            print('Red wins coverage: %s >= %s' % (self.coverage[0], self.coverage[1]))
        else:
            print('performance:0' if CI else 'Blue wins coverage: %s > %s' % (self.coverage[1], self.coverage[0]))
            print('Blue wins coverage: %s > %s' % (self.coverage[1], self.coverage[0]))


# create the referee instance and run main loop
CI = os.environ.get("CI")
referee = Referee()
referee.init()
referee.run(CI)
if CI:
    referee.simulationSetMode(referee.SIMULATION_MODE_PAUSE)
