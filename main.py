import pygame
import sys
import random
import math

import numpy as np

from globals import *

from Env import Env
from Cobra import Cobra

def handle_actions():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return 0
            elif event.key == pygame.K_DOWN:
                return 2
            elif event.key == pygame.K_LEFT:
                return 3
            elif event.key == pygame.K_RIGHT:
                return 1
    return -1

"""
def main():
    pygame.init()

    env = Env()

    while (True):
        action = handle_actions()
        env.step(action)

main()"""



def main():
    pygame.init()

    env = Env()

    trials  = 1000
    trial_len = 500

    # updateTargetNetwork = 1000
    dqn_agent = Cobra()
    steps = []
    i = 0
    for trial in range(trials):
        cur_state = np.array(env.reset()).reshape(1,8)
        for step in range(trial_len):
            env.clock.tick(10)
            action = dqn_agent.act(cur_state)
            new_state, reward, done = env.step(action)

            # reward = reward if not done else -20
            new_state = np.array(new_state).reshape(1,8)
            dqn_agent.remember(cur_state, action, reward, new_state, done)

            cur_state = new_state
            i+=1
            if done:
                dqn_agent.replay()
                dqn_agent.target_train()
                break
        print("Game : ", trial)
    print("done")

main()