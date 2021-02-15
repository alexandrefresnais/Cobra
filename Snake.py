from globals import *
import random
import pygame
import sys

class Snake:
    def __init__(self):
        self.length = 1
        # Always starting at middle
        self.positions = [((GRID_WIDTH / 2), GRID_HEIGHT / 2)]
        # Random direction at startup
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17,24,47)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    # Apply direction only if not going back
    def turn(self, point):
        if (self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction):
            return
        else:
            self.direction = point

    # Returns 1 if died from his movement
    # Moves toward his current direction
    def move(self):
        cur = self.get_head_position()
        x , y = self.direction

        # Temporary storing new pos
        new_x = (cur[0] + x)
        new_y = (cur[1] + y)

        # if bumped a wall
        if new_x < 0 or new_y < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
            self.reset()
            return 1

        new = (new_x, new_y)

        #If hit itself
        if (len(self.positions) > 2 and new in self.positions[2:]):
            self.reset()
            return 1

        # Trick : we go forward by adding an element at the head
        # And popping an element at the tail
        # (and popping nothing if we ate an Apple)
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return 0

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

    def get_state(self, apple):
        # [0:3] : apple location relatively to our direction
        # [4:7] : obstacle presence relatively to our direction

        state = [0] * 8

        # if apple not strictly on the right or left of snake
        if not ((self.direction[0] == 0 or self.positions[0][0] == apple.position[0]) and (self.direction[1] == 0 or self.positions[0][1] == apple.position[1])):
            # If above (= in the direction)
            state[0] = 1 if (self.direction[0] == 0 or same_sign(self.direction[0], apple.position[0] - self.positions[0][0])) and (self.direction[1] == 0 or same_sign(self.direction[1], apple.position[1] - self.positions[0][1])) else 0
            # it is behind if not above and if not on same line
            state[2] = 1 if not state[0] else 0

        r_dir = get_local_right(self.direction)
        # if apple not strictly on above or behind snake
        if not ((r_dir[0] == 0 or self.positions[0][0] == apple.position[0]) and (r_dir[1] == 0 or self.positions[0][1] == apple.position[1])):
            # if on the right of the snake
            state[1] = 1 if (r_dir[0] == 0 or same_sign(r_dir[0], apple.position[0] - self.positions[0][0])) and (r_dir[1] == 0 or same_sign(r_dir[1], apple.position[1] - self.positions[0][1])) else 0
            # it is on left if it is not on right and if not on same line
            state[3] = 1 if not state[1] else 0

        # Simuating going forward to see if obstable for each direction
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

        return state