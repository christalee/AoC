# Christalee Bieber, 2019
# cbieber@alum.mit.edu

# Advent of Code 2019
# http://adventofcode.com/2019/

import math
import re
from typing import Dict, List, Optional, Tuple, Union


def input(filename: str):
    with open('input_2019/' + filename, 'r') as input:
        data = [x.strip() for x in input]

    return data


def day5(sysid, opcodes=None):
    if not opcodes:
        opcodes = input('day5.txt')[0]

    ops = list(map(int, opcodes.split(',')))
    i = 0
    result = 0

    def getints(ops, params, modes):
        results = []
        for p, m in zip(params, modes):
            if m == "0":
                results.append(ops[p])
            if m == "1":
                results.append(p)
        return results

    while True:
        o = str(ops[i])
        if o[-2:] == "99":
            break
        if o[-1] == "3":
            ops[ops[i + 1]] = sysid
            i += 2
        if o[-1] == "4":
            if o[0] == "1":
                result = ops[i + 1]
            else:
                result = ops[ops[i + 1]]
            i += 2

        if o[-1] in '125678':
            while len(o) < 5:
                o = '0' + o
            a, b = getints(ops, [ops[i + 1], ops[i + 2]], [o[2], o[1]])
            c = ops[i + 3]

            if o[-1] == "1":
                ops[c] = a + b
                i += 4
            if o[-1] == "2":
                ops[c] = a * b
                i += 4

            if o[-1] == "5":
                if a != 0:
                    i = b
                else:
                    i += 3
            if o[-1] == "6":
                if a == 0:
                    i = b
                else:
                    i += 3

            if o[-1] == "7":
                if a < b:
                    ops[c] = 1
                else:
                    ops[c] = 0
                i += 4
            if o[-1] == "8":
                if a == b:
                    ops[c] = 1
                else:
                    ops[c] = 0
                i += 4

    return result


def day4():
    p1 = 0
    p2 = 0
    for x in range(245182, 790572):
        y = str(x)
        n = list(y)
        if n == sorted(n) and re.search(r'(\d)\1', y):
            p1 += 1
            m = re.sub(r'(.)\1\1+', '_', y)
            if re.search(r'(\d)\1', m):
                p2 += 1
    return {'part1': p1, 'part2': p2}


def day3(paths=None):
    if not paths:
        paths = input('day3.txt')

    [pathA, pathB] = paths

    def pathfind(path):
        # Start at the origin, keep a list of points visited.
        coordinates: List[List[int]] = [(0, 0)]

        # Starting at the last known coordinate, break the direction into a turn and a distance, and update the location accordingly
        for step in path:
            nextstep: List[int] = coordinates[-1][:]
            d: str = step[0]
            l: int = int(step[1:])

            for x in range(1, l + 1):
                if d == "R":
                    coordinates.append((nextstep[0], nextstep[1] + x))
                if d == "L":
                    coordinates.append((nextstep[0], nextstep[1] - x))
                if d == "U":
                    coordinates.append((nextstep[0] + x, nextstep[1]))
                if d == "D":
                    coordinates.append((nextstep[0] - x, nextstep[1]))

        return coordinates

    pathA = pathfind(pathA.split(','))
    pathB = pathfind(pathB.split(','))
    crossings = set(pathA) & set(pathB)

    p1 = [abs(c[0]) + abs(c[1]) for c in crossings]
    p1.sort()
    p2 = [pathA.index(c) + pathB.index(c) for c in crossings]
    p2.sort()

    return {'part1': p1[1], 'part2': p2[1]}


def day2_part2():
    for n in range(100):
        for v in range(100):
            if day2(input('day2.txt')[0], (n, v)) == 19690720:
                return n, v


def day2(opcodes: Optional[List[str]] = None, nv: Optional[Tuple[int]] = False):
    if not opcodes:
        opcodes = input('day2.txt')[0]

    ops = list(map(int, opcodes.split(',')))
    i = 0

    if nv:
        ops[1] = nv[0]
        ops[2] = nv[1]

    while True:
        o = ops[i]
        if o == 99:
            break
        if o == 1:
            ops[ops[i + 3]] = ops[ops[i + 1]] + ops[ops[i + 2]]
        if o == 2:
            ops[ops[i + 3]] = ops[ops[i + 1]] * ops[ops[i + 2]]
        i += 4

    return ops[0]


def day1():
    modules = input('day1.txt')
    fuel = 0
    while len(modules) > 0:
        next = []
        for m in modules:
            f = math.floor(int(m) / 3) - 2
            if f >= 0:
                fuel += f
                next.append(f)
        modules = next[:]

    return fuel
