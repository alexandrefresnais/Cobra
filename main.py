import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import random
import math

import numpy as np

from globals import *

from Env import Env
from Cobra import Cobra
from Viper import Viper

def display_help():
    print("Welcome to Cobra : the reinforcement learning Snake.")
    print("Here are the options")
    print("--play : Manual game of Snake")
    print("--viper : deterministic AI playing")
    print("--cobra : Reinforcement Learning AI training & playing")
    print("-------------------------------------------")
    print("Authors : Alexandre Fresnais & Thibault Gaillard")

# Gets user events
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

# Main function to play normal snake with keyboard
def play_main():
    env = Env()

    while (True):
        action = handle_actions()
        env.step(action)

# Main function to see deterministic AI playing
def viper_main():
    env = Env()
    viper = Viper()

    cur_state = env.reset()
    while (True):
        action = viper.act(cur_state)
        cur_state, _ , _ = env.step(directions.index(action))

# Cobra main function
def cobra_main(dqn_agent = Cobra(), nb_gens=200, max_action=500, show=True):
    """
    Learns and play Snake
    dqn_agent : Agent with preset
    nb_gens = number of games for training
    max_action = max number of action before next game
    show : True if you want to play with no randomness after training
    """
    env = Env(False)

    # Nb games played with no random move
    nb_games = 10

    # Recording score
    gen_scores = [0] * nb_gens
    real_scores = [0] * nb_games

    for trial in range(nb_gens + nb_games):
        print("Game : ", trial, " | Epsilon is ", dqn_agent.epsilon)

        # Does not show game until this end of the traning
        if trial == nb_gens and show:
            print("Traning Done")
            env.init_pygame()
            pygame.event.get()
            dqn_agent.epsilon = 0
            print('--- Cobra is playing ---')

        cur_state = np.array(env.reset()).reshape(1,8)
        for step in range(max_action):
            # Get the action from Cobra based on the current state
            action = dqn_agent.act(cur_state)

            # Applying move to environement to get a reward and a new state
            new_state, reward, done = env.step(action)

            # reward = reward if not done else -20
            new_state = np.array(new_state).reshape(1,8)

            # Remember the state, the move and the reward it got.
            dqn_agent.remember(cur_state, action, reward, new_state, done)

            cur_state = new_state
            # If has lost/won
            if done:
                dqn_agent.replay()
                dqn_agent.target_train()
                break
        if trial < nb_gens:
            gen_scores[trial] = env.score
        else :
            real_scores[trial-nb_gens] = env.score
    print("Done")
    return gen_scores, real_scores

def main():
    if (len(sys.argv) > 1):
        if (sys.argv[1] == "--play"):
            play_main()
        elif (sys.argv[1] == "--viper"):
            viper_main()
        elif (sys.argv[1] == "--cobra"):
            cobra_main(dqn_agent= Cobra())
        elif (sys.argv[1] == "--help"):
            display_help()
        else:
            print("Error: Unknown option")
        return
    # Default : Cobra playing
    cobra_main()

if __name__ == "__main__":
    main()
