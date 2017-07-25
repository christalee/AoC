# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 1
# http://adventofcode.com/2016/day/1

# Part 1: You are given a series of directions indicating a direction to turn and a number of blocks of travel on a grid. How many blocks away from the origin do you end up? Count total blocks as x + y, not as the crow flies.

# Given a string, convert to a list
path = "R3, L5, R2, L2, R1, L3, R1, R3, L4, R3, L1, L1, R1, L3, R2, L3, L2, R1, R1, L1, R4, L1, L4, R3, L2, L2, R1, L1, R5, R4, R2, L5, L2, R5, R5, L2, R3, R1, R1, L3, R1, L4, L4, L190, L5, L2, R4, L5, R4, R5, L4, R1, R2, L5, R50, L2, R1, R73, R1, L2, R191, R2, L4, R1, L5, L5, R5, L3, L5, L4, R4, R5, L4, R4, R4, R5, L2, L5, R3, L4, L4, L5, R2, R2, R2, R4, L3, R4, R5, L3, R5, L2, R3, L1, R2, R2, L3, L1, R5, L3, L5, R2, R4, R1, L1, L5, R3, R2, L3, L4, L5, L1, R3, L5, L2, R2, L3, L4, L1, R1, R4, R2, R2, R4, R2, R2, L3, L3, L4, R4, L4, L4, R1, L4, L4, R1, L2, R5, R2, R3, R3, L2, L5, R3, L3, R5, L2, R3, R2, L4, L3, L1, R2, L2, L3, L5, R3, L1, L3, L4, L3".split(", ")

# Start at the origin facing direction North = 0. var coordinates holds a list of points visited.
facing = 0
coordinates = [[0, 0]]

# Processing each direction
for each in path:
    nextstep = coordinates[-1][:]   # start at the last known coordinate
    turn = each[0]                  # break the direction into a turn and a distance
    steps = int(each[1:len(each)])
    if turn == "R":
        facing += 1
    else:
        facing -= 1

    while steps > 0:
        if facing % 4 == 0:
            nextstep[1] += 1
        if facing % 4 == 1:
            nextstep[0] += 1
        if facing % 4 == 2:
            nextstep[1] -= 1
        if facing % 4 == 3:
            nextstep[0] -= 1
        coordinates.append(nextstep[:])
        steps -= 1

# Part 2: How many blocks away is the first location you visit twice?

for point in coordinates:
    if coordinates.count(point) >= 2:
        position = [point, coordinates.index(point)]
        print position