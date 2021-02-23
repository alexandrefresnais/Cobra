import pygame

from Snake import Snake
from Apple import Apple
from globals import *

class Env:
    def __init__(self, show=True):
        self.show = show
        if show:
            self.init_pygame()

        self.snake = Snake()
        self.apple = Apple()

        self.score = 0

        self.previous_dist = distance(self.snake.get_head_position(), self.apple.position)

    def init_pygame(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.myfont = pygame.font.SysFont("monospace",16)
        self.show = True

    def drawGrid(self):
        """
        Draws background grid
        """
        for y in range(0, int(GRID_HEIGHT)):
            for x in range(0, int(GRID_WIDTH)):
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                if (x+y) % 2 == 0:
                    pygame.draw.rect(self.surface, (93, 216, 228), r)
                else:
                    pygame.draw.rect(self.surface, (84, 194, 205), r)

    def draw(self):
        """
        Draws every object in the env
        """
        self.drawGrid()
        self.snake.draw(self.surface)
        self.apple.draw(self.surface)

        #Score
        self.screen.blit(self.surface, (0,0))
        text = self.myfont.render("Score {0}".format(self.score), 1, (0,0,0))
        self.screen.blit(text, (5,10))
        pygame.display.update()

        self.clock.tick(10)


    # Reset game and returns a state
    def reset(self):
        self.score = 0
        self.snake.reset()
        return self.snake.get_state(self.apple)

    # Apply the action of the snake to the environement
    def step(self, action):
        if (action >= 0 and action <= 3):
            self.snake.turn(directions[action])

        reward = 0

        died = self.snake.move()
        if died:
            reward = -100
            self.apple.randomize_position()
        elif self.snake.get_head_position() == self.apple.position: # Hit apple
            self.snake.length += 1
            self.score += 1
            self.apple.randomize_position(self.snake)
            reward = 10
        else:
            # Calculating reward based on distance
            dist = distance(self.snake.get_head_position(), self.apple.position)
            reward = 1 if dist < self.previous_dist else -1
            self.previous_dist = dist

        #Gets new state
        state = self.snake.get_state(self.apple)

        if self.show:
            self.draw()

        return (state, reward, died)