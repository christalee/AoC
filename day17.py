# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 17
# http://adventofcode.com/2016/day/17

import hashlib

path = ''
seed = 'yjjvjgan'
location = (0, 0)

def doorcheck(x):
    doors = []
    for each in x:
        if each in 'bcdef':
            doors.append(True)
        else:
            doors.append(False)
    return doors

while location is not (3, 3):
    m = hashlib.md5()
    m.update(seed + path)
    doorcheck(m[0:4])