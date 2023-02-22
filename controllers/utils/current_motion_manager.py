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

class CurrentMotionManager:
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
