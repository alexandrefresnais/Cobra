import pygame

from Snake import Snake
from Apple import Apple
from globals import *

class Env:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.drawGrid()

        self.snake = Snake()
        self.apple = Apple()

        self.myfont = pygame.font.SysFont("monospace",16)
        self.previous_dist = distance(self.snake.get_head_position(), self.apple.position)

    def drawGrid(self):
        for y in range(0, int(GRID_HEIGHT)):
            for x in range(0, int(GRID_WIDTH)):
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                if (x+y) % 2 == 0:
                    pygame.draw.rect(self.surface, (93, 216, 228), r)
                else:
                    pygame.draw.rect(self.surface, (84, 194, 205), r)

    def reset(self):
        self.snake.reset()
        return self.snake.get_state(self.apple)

    def step(self, action):
        if (action >= 0 and action <= 3):
            self.snake.turn(directions[action])
        self.drawGrid()

        reward = 0

        died = self.snake.move()
        if died:
            reward = -100
        elif self.snake.get_head_position() == self.apple.position:
            self.snake.length += 1
            self.snake.score += 1
            self.apple.randomize_position(self.snake)
            reward = 10
        else:
            # Calculating reward based on distance
            dist = distance(self.snake.get_head_position(), self.apple.position)
            reward = 1 if dist < self.previous_dist else -1
            self.previous_dist = dist

        state = self.snake.get_state(self.apple)

        self.snake.draw(self.surface)
        self.apple.draw(self.surface)

        self.screen.blit(self.surface, (0,0))
        text = self.myfont.render("Score {0}".format(self.snake.score), 1, (0,0,0))
        self.screen.blit(text, (5,10))
        pygame.display.update()

        return (state, reward, 1)