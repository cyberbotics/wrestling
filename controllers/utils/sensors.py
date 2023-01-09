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
This module provides a set of classes to interact with the robot's sensors.
"""

import sys
sys.path.append('..')
from utils.utils import Average

class Accelerometer():
    """Class that provides an interface to the accelerometer sensor."""

    def __init__(self, device, time_step, history_steps=10):
        self.device = device
        self.device.enable(time_step)
        self.average = Average(dimensions=3, history_steps=history_steps)

    def get_values(self):
        """Returns the current accelerometer values."""
        return self.device.getValues()

    def get_average(self):
        """Returns the current accelerometer average of the last HISTORY_STEPS values."""
        return self.average.average

    def update_average(self):
        """Updates the accelerometer average."""
        values = self.get_values()
        self.average.update_average(values)

    def get_new_average(self):
        """Updates the accelerometer average and returns it."""
        values = self.get_values()
        self.average.update_average(values)
        return self.get_average()
