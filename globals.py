import math

# Nb grid square
GRID_WIDTH = 10
GRID_HEIGHT = 10

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

def same_sign(a, b):
    return (a > 0) == (b > 0)

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

# Pythagorian distance between two points
def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)