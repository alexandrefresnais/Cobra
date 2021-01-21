import pygame
import sys
import random

class Cobra:
    def __init__(self):
        self.length = 1
        self.positions = [((GRID_WIDTH / 2), GRID_HEIGHT / 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17,24,47)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if (self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction):
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x , y = self.direction

        new_x = (cur[0] + x)
        new_y = (cur[1] + y)

        # Bumping a wall
        if new_x < 0 or new_y < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
            self.reset()
            return

        new = (new_x, new_y)

        #If hit itself
        if (len(self.positions) > 2 and new in self.positions[2:]):
            self.reset()
        else:
            self.positions.insert(0, new)
            #this does not apply if apple is eaten
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((GRID_WIDTH / 2), GRID_HEIGHT / 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0] * GRIDSIZE, p[1] * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93,216,228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

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

# Nb grid square
GRID_WIDTH = 12
GRID_HEIGHT = 12

# Absolute size of a grid square
GRIDSIZE = 20

# Size of window
SCREEN_WIDTH = GRID_WIDTH * GRIDSIZE
SCREEN_HEIGHT = GRID_HEIGHT * GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Cobra()
    food = Apple()

    myfont = pygame.font.SysFont("monospace",16)

    while (True):
        clock.tick(8)

        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position(snake)
            if snake.length == GRID_WIDTH * GRIDSIZE:
                # WON
                snake.reset()

        snake.draw(surface)
        food.draw(surface)


        screen.blit(surface, (0,0))
        text = myfont.render("Score {0}".format(snake.score), 1, (0,0,0))
        screen.blit(text, (5,10))
        pygame.display.update()



main()