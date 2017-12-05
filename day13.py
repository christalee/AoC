# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 13
# http://adventofcode.com/2016/day/13

# TODO: check all code for map, filter, list comprehension, and loop refactoring

# Part 1: Given a map of a space defined by the function below, what is the shortest path from (1,1) to (31, 39)? You may not move diagonally.

# Generating fn: 
# Find x*x + 3*x + 2*x*y + y + y*y.
# Add your puzzle input.
# Find the binary representation of that sum; count the number of bits that are 1.
# If the number of bits that are 1 is even, it's an open space.
# If the number of bits that are 1 is odd, it's a wall.

# Example:
# puzzle input = 10, walls are #, spaces are .

#   0123456789
# 0 .#.####.##
# 1 ..#..#...#
# 2 #....##...
# 3 ###.#.###.
# 4 .##..#..#.
# 5 ..##....#.
# 6 #...##.###

# shortest route from (1,1) to (7,4) is 11 steps (marked as O)
#   0123456789
# 0 .#.####.##
# 1 .O#..#...#
# 2 #OOO.##...
# 3 ###O#.###.
# 4 .##OO#OO#.
# 5 ..##OOO.#.
# 6 #...##.###

import numpy as np

steps = 0
origin = (1, 1)
destination = (31, 39)
q = 1350

# Generate the floor layout first, using handy numpy routines
def f(x, y):
    s = x*x + 3*x + 2*x*y + y + y*y + q

layout = np.fromfunction(f, (40, 40), dtype=int)
for x in np.nditer(layout, op_flags=["readwrite"]):
    b = bin(x)
    if b.count('1') % 2 == 1:
        x[...] = 1
    else:
        x[...] = 0

# Pathfinding: Start at origin. While position is not destination, check for 0 (empty space), starting with whichever of (x, y) is farther from destination? or clockwise? If you can move, update position and steps, and add this path to dictionary? (cf. day11 code)