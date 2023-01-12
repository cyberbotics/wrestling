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
This module provides a basic Finite State Machine class.
"""


class FiniteStateMachine:
    def __init__(self, states, initial_state, actions=None):
        """Create a finite state machine.

        Args:
            states (list): List of states.
            initial_state (str): Initial state.
            actions (dict): Dictionary of actions to execute for each state.
        """
        self.states = states
        self.current_state = initial_state
        self.actions = actions

    def transition_to(self, state):
        """Transition to a new state."""
        if state not in self.states:
            raise ValueError("Invalid state: {}".format(state))
        self.current_state = state

    def execute_action(self):
        """Execute the action of the current state."""
        action = self.actions[self.current_state]
        action()
