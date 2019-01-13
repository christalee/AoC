# Christalee Bieber, 2018
# cbieber@alum.mit.edu

# Advent of Code 2015
# http://adventofcode.com/2015/

import hashlib
import re
from typing import Dict, List, Optional, Union

import numpy as np


def input(filename):
    with open(filename, 'r') as input:
        data = [x.strip() for x in input]

    return data


def day9(distances=None):
    if not distances:
        distances = input('day9.txt')

    legs = {}
    for d in distances:
        x = d.split(' = ')
        legs[x[1]] = x[0]
    km = list(legs.keys()).sort()

# def day8(strings=None):
#     if not strings:
#         with open('day8.txt', 'r') as input:
#             strings = input.read()
#
#     string_len = 0
#     byte_len = len(strings)
#     string_list = [x.strip() for x in strings]
#
#     for s in string_list:
#         t = s[1:-1]
#         if r'\\' in t:
#             t = t.replace(r'\\', '_')
#         if r'\"' in t:
#             t = t.replace(r'\"', '_')
#         if r'\x' in t:
#             t = re.sub(r'(\\x[a-fA-F0-9]{2})', '_', t)
#         string_len += len(t)
#
#     return byte_len - string_len


def day7(instructions=None):
    # For part 1, replace line 1 of day7.txt with '1674 -> b'
    if not instructions:
        instructions = input('day7.txt')

    wires = {}

    def valid(x):
        if x.isdecimal():
            return np.uint16(x)
        if x in wires:
            return wires[x]
        else:
            return None

    def valrun():
        for i in instructions:
            x = i.split()
            v = False

            # assign a signal to a wire
            if x[1] == '->' and valid(x[0]) is not None:
                v = valid(x[0])

            # invert a signal
            if x[0] == 'NOT' and valid(x[1]) is not None:
                v = ~valid(x[1])

            if valid(x[0]) is not None and valid(x[2]) is not None:
                # LSHIFT a signal
                if x[1] == 'LSHIFT':
                    v = valid(x[0]) << valid(x[2])

                # RSHIFT a signal
                if x[1] == 'RSHIFT':
                    v = valid(x[0]) >> valid(x[2])

                # AND two signals
                if x[1] == 'AND':
                    v = valid(x[0]) & valid(x[2])

                # OR two signals
                if x[1] == 'OR':
                    v = valid(x[0]) | valid(x[2])

            if v is not False:
                wires[x[-1]] = v
                # print(x, v, wires.keys())

    for x in range(500):
        valrun()
    return wires


def day6_part2(instructions=None):
    lights = np.zeros((1000, 1000), dtype=int)

    if not instructions:
        instructions = input('day6.txt')

    for i in instructions:
        pieces = i.split()
        start = list(map(int, pieces[-3].split(',')))
        end = list(map(int, pieces[-1].split(',')))

        if pieces[1] == 'on':
            lights[start[0]:end[0] + 1, start[1]:end[1] + 1].__iadd__(1)
        if pieces[1] == 'off':
            lights[start[0]:end[0] + 1, start[1]:end[1] + 1].__isub__(1)
            np.clip(lights, 0, None, out=lights)
        if pieces[0] == 'toggle':
            lights[start[0]:end[0] + 1, start[1]:end[1] + 1].__iadd__(2)

    return np.sum(lights)


def day6_part1(instructions=None):
    lights = np.zeros((1000, 1000), dtype=int)

    if not instructions:
        instructions = input('day6.txt')

    for i in instructions:
        pieces = i.split()
        start = list(map(int, pieces[-3].split(',')))
        end = list(map(int, pieces[-1].split(',')))
        # target = [start[0]:end[0]+1, start[1]:end[1]+1]

        if pieces[1] == 'on':
            lights[start[0]:end[0] + 1, start[1]:end[1] + 1] = 1
        if pieces[1] == 'off':
            lights[start[0]:end[0] + 1, start[1]:end[1] + 1] = 0
        if pieces[0] == 'toggle':
            lights[start[0]:end[0] + 1, start[1]:end[1] +
                   1] = np.bitwise_xor(lights[start[0]:end[0] + 1, start[1]:end[1] + 1], 1)

    return np.sum(lights)


def day5_part2(strings: List[str] = None) -> int:
    if not strings:
        strings = input('day5.txt')

    results: List[bool] = []

    for s in strings:
        nice = False
        if re.search(r'(\w)\w\1', s) and re.search(r'(\w{2}).*\1', s):
            nice = True

        results.append(nice)

    return results.count(True)


def day5_part1(strings: List[str] = None) -> int:
    if not strings:
        strings = input('day5.txt')

    results: List[bool] = []

    for s in strings:
        nice = False
        if re.search(r'([aeiou].*){3}', s) and re.search(r'(\w)\1', s):
            nice = True
        if re.search(r'(ab|cd|pq|xy)', s):
            nice = False

        results.append(nice)

    return results.count(True)


def day4(key: str = 'yzbqklnj') -> int:
    i: int = 1
    found: bool = False

    while not found:
        m = hashlib.md5()
        m.update(bytes(key + str(i), 'utf-8'))
        if m.hexdigest()[:5] == '00000':    # Edit here for part 2
            found = True
        i += 1

    return i - 1


def day3(arrows: str = None) -> int:
    if not arrows:
        with open('day3.txt', 'r') as input:
            arrows = input.read()

    # location: Dict[str, int] = {'x': 0, 'y': 0}
    santa: Dict[str, int] = {'x': 0, 'y': 0}
    robot: Dict[str, int] = {'x': 0, 'y': 0}
    presents: Dict[str, int] = {'[0, 0]': 2}

    for i, a in enumerate(arrows):
        if i % 2 == 0:
            location = santa
        else:
            location = robot

        if a == '>':
            location['y'] += 1
        if a == '<':
            location['y'] -= 1
        if a == '^':
            location['x'] += 1
        if a == 'v':
            location['x'] -= 1

        here = str(list(location.values()))
        if here in presents.keys():
            presents[here] += 1
        else:
            presents[here] = 1

    return len(presents)


def day2(box_list: Optional[List[str]] = None) -> Dict[str, int]:
    if not box_list:
        box_list = input('day2.txt')

    paper: int = 0
    ribbon: int = 0

    for box in box_list:
        l, w, h = list(map(int, box.split('x')))
        a = l * w
        b = w * h
        c = h * l

        paper += 2 * sum([a, b, c]) + min(a, b, c)

        d = [l, w, h]
        d.remove(max(d))
        ribbon += (l * w * h) + 2 * sum(d)

    return {'paper': paper, 'ribbon': ribbon}


def day1(parens: Optional[str] = None) -> Dict[str, Union[int, List[int]]]:
    if not parens:
        with open('day1.txt', 'r') as input:
            parens = input.read()

    floor: int = 0
    basement: List[int] = []

    for i, p in enumerate(parens):
        if p == '(':
            floor += 1
        if p == ')':
            floor -= 1
        if floor == -1:
            basement.append(i + 1)

    # floor = parens.count('(') - parens.count(')')
    return {'floor': floor, 'basement': basement}
