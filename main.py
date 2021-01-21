import pygame
import sys
import random
import math

from globals import *

from Env import Env

def main():
    pygame.init()

    env = Env()

    while (True):
        env.step()

main()