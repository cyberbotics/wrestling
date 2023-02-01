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
        self.robot[0] = self.getFromDef('WRESTLER_RED').getFromProtoDef('HEAD_SLOT')
        self.robot[1] = self.getFromDef('WRESTLER_BLUE').getFromProtoDef('HEAD_SLOT')
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
        participant = os.environ['PARTICIPANT_NAME'] if 'PARTICIPANT_NAME' in os.environ else 'Participant'
        opponent = os.environ['OPPONENT_NAME'] if 'OPPONENT_NAME' in os.environ else 'Opponent'
        self.setLabel(0, '█' * 100, 0, 0, 0.1, 0xffffff, 0.3, 'Lucida Console')
        self.setLabel(1, '█' * 100, 0, 0.048, 0.1, 0xffffff, 0.3, 'Lucida Console')
        self.setLabel(2, participant, 0.01, 0.003, 0.08, 0xff0000, 0, 'Arial')
        self.setLabel(3, opponent, 0.01, 0.051, 0.08, 0x0000ff, 0, 'Arial')
        ko_labels = ['', '']
        coverage_labels = ['', '']
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
                    color = 0xff0000 if i == 0 else 0x0000ff
                    if abs(position[0]) < 1 and abs(position[1]) < 1:  # inside the ring
                        coverage = 0
                        for j in range(2):
                            if position[j] < self.min[i][j]:
                                self.min[i][j] = position[j]
                            elif position[j] > self.max[i][j]:
                                self.max[i][j] = position[j]
                            box[j] = self.max[i][j] - self.min[i][j]
                            coverage += box[j] * box[j]
                        coverage = math.sqrt(coverage)
                        self.coverage[i] = coverage
                        self.indicator[i].setPosition(self.coverage[i] / 7)
                        string = '{:.3f}'.format(coverage)
                        if string != coverage_labels[i]:
                            self.setLabel(4 + i, string, 0.8, 0.003 + 0.048 * i, 0.08, color, 0, 'Arial')
                        coverage_labels[i] = string
                    if position[2] < 0.9:  # low position threshold
                        self.ko_count[i] = self.ko_count[i] + 200
                        if self.ko_count[i] > 10000:  # 10 seconds
                            ko = i
                    else:
                        self.ko_count[i] = 0
                    counter = 10 - self.ko_count[i] // 1000
                    string = '' if self.ko_count[i] == 0 else str(counter) if counter > 0 else 'KO'
                    if string != ko_labels[i]:
                        self.setLabel(6 + i, string, 0.7 - len(string) * 0.01, 0.003 + 0.048 * i, 0.08, color, 0, 'Arial')
                    ko_labels[i] = string

            if self.step(time_step) == -1 or time > game_duration or ko != -1:
                break
            time += time_step
        if ko == 0:
            print('Red is KO. Blue wins!')
            performance = 0
        elif ko == 1:
            print('Blue is KO. Red wins!')
            performance = 1
        # in case of coverage equality, blue wins
        elif self.coverage[0] > self.coverage[1]:
            print('Red wins coverage: %s > %s' % (self.coverage[0], self.coverage[1]))
            performance = 1
        else:
            print('Blue wins coverage: %s >= %s' % (self.coverage[1], self.coverage[0]))
            performance = 0
        self.setLabel(7 - performance, 'WIN', 0.673, 0.051 - 0.048 * performance,
                      0.08, 0x0000ff if performance == 0 else 0xff0000, 0, 'Arial')
        if CI:
            self.step(3000)  # wait 3 seconds to display the result
            self.animationStopRecording()  # stop the recording of the animation
            self.step(time_step)
            print(f'performance:{performance}')


# create the referee instance and run main loop
CI = os.environ.get("CI")
referee = Referee()
referee.init()
referee.run(CI)
if CI:
    referee.simulationSetMode(referee.SIMULATION_MODE_PAUSE)
