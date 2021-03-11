"""
Deterministic AI.
Not using deep learning.
For testing purpose
"""

from globals import *

class Viper:
    # def __init__(self):
    def act(self, state):
        # From snake.py, state is :
        # [0:3] : apple location relatively to our direction
        # [4:7] : obstacle presence relatively to our direction

        # if obstacle in front of snake
        if state[4]:
            # if obstacle on right
            if state[5]:
                return LEFT
            if state[7]:
                return RIGHT

        # if Apple on right
        if state[1] and not state[5]:
            return RIGHT
        # if on left
        if state[3] and not state[7]:
            return LEFT
        # If strictly behind, moving right by default
        if state[2] and not state[5]:
            return RIGHT
        return UP