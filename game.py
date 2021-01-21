import pygame
import sys
import random
import math

from globals import *
from Snake import Snake

class Apple:
    def __init__(self):
        self.position = (0,0)
        self.color = (223,163,49)
        self.randomize_position()

    def randomize_position(self, snake = None):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        # while position is taken by a part of snake
        if snake != None:
            while self.position in snake.positions:
                self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, surface):
        r = pygame.Rect((self.position[0] * GRIDSIZE, self.position[1] * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93,216,228), r, 1)


def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (84, 194, 205), rr)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    apple = Apple()

    myfont = pygame.font.SysFont("monospace",16)

    while (True):
        clock.tick(8)

        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.score += 1
            apple.randomize_position(snake)
            if snake.length == GRID_WIDTH * GRIDSIZE:
                # WON
                snake.reset()

        state = snake.get_state(apple)

        snake.draw(surface)
        apple.draw(surface)


        screen.blit(surface, (0,0))
        text = myfont.render("Score {0}".format(snake.score), 1, (0,0,0))
        screen.blit(text, (5,10))
        pygame.display.update()

main()