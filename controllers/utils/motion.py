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

import os
from controller import Motion

class Current_motion_manager:
    def __init__(self):
        self.currentMotion = None
    
    def get(self):
        """Returns the motion that is currently playing."""
        return self.currentMotion
    
    def is_over(self):
        """Returns True if the current motion is over."""
        return self.currentMotion.isOver()
    
    def set(self, motion):
        """Sets the current motion to the given motion."""
        if self.currentMotion:
            self.currentMotion.stop()
            self._reset_is_over_flag(self.currentMotion)
        self.currentMotion = motion
        motion.play()

    def _reset_is_over_flag(self, motion):
        """Resets Webots' isOver() flag of the given motion."""
        motion.play()
        motion.stop()

class Motion_library:
    def __init__(self):
        """Initializes the motion library with the motions in the motions folder."""
        self.motions = {}
        motion_dir = '../motions/'
        for motion_file in os.listdir(motion_dir):
            motion_path = os.path.join(motion_dir, motion_file)
            motion_name = os.path.splitext(motion_file)[0]
            motion = Motion(motion_path)
            if motion_name.endswith('Loop'): # if the file ends with "Loop", it is played on loop
                motion.setLoop(True)
            self.motions[motion_name] = motion

    
    def add(self, name, motion_path, loop=False):
        """Adds a custom motion to the library."""
        self.motions[name] = Motion(motion_path)
        if loop:
            self.motions[name].setLoop(loop)
    
    def get(self, name):
        """Returns the motion with the given name."""
        return self.motions[name]

    def play(self, name):
        """Plays the motion with the given name."""
        self.motions[name].play()
