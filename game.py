import pygame
import sys
import random

def same_sign(a, b):
    return (a > 0) == (b > 0)

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

# important : clockwise
directions = [UP, RIGHT, DOWN, LEFT]

# get local right from our current direction
def get_local_right(direction):
    i = directions.index(direction) + 1
    return directions[i % 4]

def get_local_down(direction):
    i = directions.index(direction) + 2
    return directions[i % 4]

def get_local_left(direction):
    i = directions.index(direction) + 3
    return directions[i % 4]

def add_tuple(a, b):
    res = (0, 0)
    res[0] = a[0] + b[0]
    res[1] = a[1] + b[1]
    return res

class Cobra:
    def __init__(self):
        self.length = 8
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

    def get_state(self, apple):
        # [0:3] : apple location relatively to our direction
        # [4:7] obstacle presence
        # [8:11] snake direction

        state = [0] * 12

        # if apple not strictly on the right or left of snake
        if not ((self.direction[0] == 0 or self.positions[0][0] == apple.position[0]) and (self.direction[1] == 0 or self.positions[0][1] == apple.position[1])):
            # If above (= in the direction)
            state[0] = (self.direction[0] == 0 or same_sign(self.direction[0], apple.position[0] - self.positions[0][0])) and (self.direction[1] == 0 or same_sign(self.direction[1], apple.position[1] - self.positions[0][1]))
            # it is behind if not above and if not on same line
            state[2] = not state[0]

        r_dir = get_local_right(self.direction)
        # if apple not strictly on above or behind snake
        if not ((r_dir[0] == 0 or self.positions[0][0] == apple.position[0]) and (r_dir[1] == 0 or self.positions[0][1] == apple.position[1])):
            # if on the right of the snake
            state[1] = (r_dir[0] == 0 or same_sign(r_dir[0], apple.position[0] - self.positions[0][0])) and (r_dir[1] == 0 or same_sign(r_dir[1], apple.position[1] - self.positions[0][1]))
            # it is on left if not on right and if not on same line
            state[3] = not state[1]

        # going forward to see if obstable
        tmp = tuple(map(sum, zip(self.positions[0], self.direction))) # Python, i just want to add two tuple please
        if tmp[0] < 0 or tmp[1] < 0 or tmp[0] >= GRID_WIDTH or tmp[1] >= GRID_HEIGHT or tmp in self.positions:
            state[4] = 1

        tmp = tuple(map(sum, zip(self.positions[0], get_local_right(self.direction))))
        if tmp[0] < 0 or tmp[1] < 0 or tmp[0] >= GRID_WIDTH or tmp[1] >= GRID_HEIGHT or tmp in self.positions:
            state[5] = 1

        tmp = tuple(map(sum, zip(self.positions[0], get_local_down(self.direction))))
        if tmp[0] < 0 or tmp[1] < 0 or tmp[0] >= GRID_WIDTH or tmp[1] >= GRID_HEIGHT or tmp in self.positions:
            state[6] = 1

        tmp = tuple(map(sum, zip(self.positions[0], get_local_left(self.direction))))
        if tmp[0] < 0 or tmp[1] < 0 or tmp[0] >= GRID_WIDTH or tmp[1] >= GRID_HEIGHT or tmp in self.positions:
            state[7] = 1

        # Setting direction
        state[8] = self.direction == UP
        state[9] = self.direction == RIGHT
        state[10] = self.direction == DOWN
        state[11] = self.direction == LEFT

        return state



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

    snake = Cobra()
    food = Apple()

    myfont = pygame.font.SysFont("monospace",16)

    while (True):
        clock.tick(2)

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

        state = snake.get_state(food)

        snake.draw(surface)
        food.draw(surface)


        screen.blit(surface, (0,0))
        text = myfont.render("Score {0}".format(snake.score), 1, (0,0,0))
        screen.blit(text, (5,10))
        pygame.display.update()



main()