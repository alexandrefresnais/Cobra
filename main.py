import pygame
import sys
import random
import math

from globals import *

from Env import Env

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

def main():
    pygame.init()

    env = Env()

    while (True):
        env.clock.tick(8)
        action = handle_actions()
        env.step(action)

main()