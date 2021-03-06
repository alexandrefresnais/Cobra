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

# Returns true if a and b have same signs
def same_sign(a, b):
    return (a > 0) == (b > 0)

# Important : clockwise
directions = [UP, RIGHT, DOWN, LEFT]

# Get local right direction from our current direction
def get_local_right(direction):
    i = directions.index(direction) + 1
    return directions[i % 4]

def get_local_down(direction):
    i = directions.index(direction) + 2
    return directions[i % 4]

def get_local_left(direction):
    i = directions.index(direction) + 3
    return directions[i % 4]

# Return a + b with a and b being tuples
def add_tuple(a, b):
    res = (0, 0)
    res[0] = a[0] + b[0]
    res[1] = a[1] + b[1]
    return res

# Pythagorian distance between two points
def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)