# Christalee Bieber, 2018
# cbieber@alum.mit.edu

# Advent of Code 2015
# http://adventofcode.com/2015/

# TODO
# - finish solutions for problems 11-25
# - add problem statements for all solutions
# - combine any part1/part2 solutions into single fns
# - review all ipynb for cruft & comments
# - factor out nested fns and subproblems
# - refactor for elegance, clarity, and performance (see timeit notes)
# - add types to all nested fns and key vars
# - resolve all TODOs
# - refactor: list/dict comprehensions, iterator/generators, collections.Counter, map/filter

import collections
import hashlib
import itertools
import operator
import re
import string
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd


def input(filename: str):
    with open('input_2015/' + filename, 'r') as input:
        data = [x.strip() for x in input]

    return data


def day18_neighbors(point, lights):
    n = []
    for x in [point[0] - 1, point[0], point[0] + 1]:
        for y in [point[1] - 1, point[1], point[1] + 1]:
            if x >= 0 and x < lights.shape[0] and y >= 0 and y < lights.shape[1]:
                n.append(lights[(x, y)])
            else:
                n.append('.')
    n.remove(lights[point])
    return n


def day18_part2(cycles, lights=None):
    if not lights:
        lights = input('day18.txt')
    lights = np.array(list(map(list, lights)))

    for x in range(cycles):
        for c in [(0, 0), (0, lights.shape[0] - 1), (lights.shape[1] - 1, 0), (lights.shape[1] - 1, lights.shape[0] - 1)]:
            lights[c] = '#'
        nditer = np.nditer(lights, flags=['multi_index', 'refs_ok'], op_flags=['readonly', 'copy'])
        with nditer as it:
            newlights = np.empty(lights.shape, dtype='<U1')
            for light in it:
                i = it.multi_index
                n = day18_neighbors(i, lights)
                if light == '#':
                    if n.count('#') != 2 and n.count('#') != 3:
                        newlights[i] = '.'
                    else:
                        newlights[i] = '#'
                if light == ".":
                    if n.count("#") == 3:
                        newlights[i] = '#'
                    else:
                        newlights[i] = '.'

        lights = np.array(newlights)

    for c in [(0, 0), (0, lights.shape[0] - 1), (lights.shape[1] - 1, 0), (lights.shape[1] - 1, lights.shape[0] - 1)]:
        lights[c] = '#'
    return np.sum(np.char.count(lights, '#'))


def day18_part1(cycles, lights=None):
    if not lights:
        lights = input('day18.txt')
    lights = np.array(list(map(list, lights)))

    for x in range(cycles):
        nditer = np.nditer(lights, flags=['multi_index', 'refs_ok'], op_flags=['readonly', 'copy'])
        with nditer as it:
            newlights = np.empty(lights.shape, dtype='<U1')
            for light in it:
                i = it.multi_index
                n = day18_neighbors(i, lights)
                if light == '#':
                    if n.count('#') != 2 and n.count('#') != 3:
                        newlights[i] = '.'
                    else:
                        newlights[i] = '#'
                if light == ".":
                    if n.count("#") == 3:
                        newlights[i] = '#'
                    else:
                        newlights[i] = '.'

        lights = np.array(newlights)

    return np.sum(np.char.count(lights, '#'))


def day17(eggnog, containers=None):
    if not containers:
        containers = list(map(int, input("day17.txt")))

    combos = []
    for i in range(len(containers)):
        combos += itertools.combinations(containers, i)

    part1 = [x for x in combos if sum(x) == eggnog]
    part2 = [x for x in part1 if len(x) == len(part1[0])]
    return {"part1": len(part1), "part2": len(part2)}


def day16():
    target = {"children": 3,
              "cats": 7,
              "samoyeds": 2,
              "pomeranians": 3,
              "akitas": 0,
              "vizslas": 0,
              "goldfish": 5,
              "trees": 3,
              "cars": 2,
              "perfumes": 1}
    text = input('day16.txt')

    sues = {}
    for s in text:
        t = s.split(':', 1)
        k = dict([x.split(':') for x in t[1].split(',')])
        sues[int(t[0].split()[1])] = dict(zip(map(str.strip, k.keys()), map(int, k.values())))

    part1 = []
    part2 = []

    for k, v in sues.items():
        for t in target:
            if t in v:
                if target[t] == v[t]:
                    part1.append(k)
                if t in ["cats", "trees"] and target[t] < v[t]:
                    part2.append(k)
                if t in ["pomeranians", "goldfish"] and target[t] > v[t]:
                    part2.append(k)
                if t not in ["cats", "trees", "pomeranians", "goldfish"] and target[t] == v[t]:
                    part2.append(k)

    results = {}
    results["part1"] = collections.Counter(part1).most_common(1)[0][0]
    results["part2"] = collections.Counter(part2).most_common(1)[0][0]
    return results


def day15(text=None):
    if not text:
        text = input('day15.txt')

    stats = {}
    for s in text:
        q = {}
        i = s.split(":")
        t = i[1].split(",")
        for u in t:
            v = u.split()
            q[v[0]] = int(v[1])
        stats[i[0]] = q

    ingredients = set([s.split()[0].strip(':') for s in text])
    amounts = [(a, b, c, 100 - a - b - c) for a in range(101) for b in range(101 - a) for c in range(101 - a - b)]
    part1 = {}
    part2 = {}
    keys = list(stats[list(ingredients)[0]])
    keys.remove("calories")
    for a in amounts:
        score = 1
        for j in keys:
            score *= max(0, sum(map(operator.mul, [stats[k][j] for k in ingredients], a)))
        part1[score] = dict(zip(ingredients, a))

        calories = sum(map(operator.mul, [stats[k]['calories'] for k in ingredients], a))
        if calories == 500:
            part2[score] = dict(zip(ingredients, a))

    return {"part1": max(part1.keys()), "part2": max(part2.keys())}


def day14_part2(time, text=None):
    if not text:
        text = input("day14.txt")

    reindeer = set([s.split()[0] for s in text])
    stats = dict.fromkeys(reindeer, {})
    for s in text:
        parsed = {}
        t = s.split()
        parsed["speed"] = int(t[3])
        parsed["sprint"] = int(t[6])
        parsed["rest"] = int(t[13])
        stats[t[0]] = parsed

    scores = dict.fromkeys(reindeer, 0)
    for x in range(1, time + 1):
        distances = dict.fromkeys(reindeer, 0)
        for r in reindeer:
            d = 0
            vals = stats[r]
            remainder = x % (vals["sprint"] + vals["rest"])
            cycles = (x - remainder) / (vals["sprint"] + vals["rest"])
            d = vals["speed"] * (cycles * vals["sprint"] + min(remainder, vals["sprint"]))
            distances[r] += d

        winner = max(distances.values())
        for r in distances:
            if distances[r] == winner:
                scores[r] += 1

    return max(scores.values())


def day14_part1(time, text=None):
    if not text:
        text = input("day14.txt")

    reindeer = set([s.split()[0] for s in text])
    stats = dict.fromkeys(reindeer, {})
    for s in text:
        parsed = {}
        t = s.split()
        parsed["speed"] = int(t[3])
        parsed["sprint"] = int(t[6])
        parsed["rest"] = int(t[13])
        stats[t[0]] = parsed

    scores = {}
    for r in reindeer:
        vals = stats[r]
        remainder = time % (vals["sprint"] + vals["rest"])
        cycles = (time - remainder) / (vals["sprint"] + vals["rest"])
        d = cycles * vals["speed"] * vals["sprint"]
        if vals["sprint"] <= remainder:
            d += vals["speed"] * vals["sprint"]

        scores[r] = d

    return max(scores.values())


def day13_part2(relations=None):
    # TODO: make this more elegant
    if not relations:
        relations = input("day13.txt")

    guests = set([s.split()[0] for s in relations])
    for g in guests:
        relations.append(g + " would gain 0 happiness units by sitting next to Talia.")
        relations.append("Talia would gain 0 happiness units by sitting next to " + g)

    return day13_part1(relations)


def day13_part1(relations=None):
    if not relations:
        relations = input("day13.txt")

    guests = set([s.split()[0] for s in relations])
    parsed = []
    for s in relations:
        t = s.split()
        if t[2] == "gain":
            t[2] = "+"
        if t[2] == "lose":
            t[2] = '-'
        parsed.append([t[0], int(t[2] + t[3]), t[-1].strip('.')])

    # TODO again, is this really necessary? It is convenient.
    vals = pd.DataFrame(columns=guests, index=guests)
    for d in parsed:
        vals.loc[d[0], d[2]] = d[1]

    # TODO this checks each route multiple times, since they loop
    scores = {}
    seating = itertools.permutations(guests)
    for i in seating:
        d = 0
        for n, s in enumerate(i):
            t = (n + 1) % len(guests)
            d += vals.loc[s, i[t]] + vals.loc[i[t], s]
        scores[i] = d

    return max(scores.values())


def day12(json=None):
    if not json:
        json = input("day12.txt")

    part1 = sum(list(map(int, re.sub(r'[^0-9-]', ' ', json[0]).split())))

    return {"part1": part1}


def day11_alpha_inc(s):
    ab = string.ascii_lowercase
    while len(s) > 0:
        i = ab.index(s[-1])
        if i == 25:
            return day11_alpha_inc(s[:-1]) + "a"
        else:
            return s[:-1] + ab[i + 1]


def day11(pw=None):
    if not pw:
        pw = 'aaaaaaaa'
    ab = string.ascii_lowercase
    while pw != "zzzzzzzz":
        if not re.search(r'[iol]', pw) and re.search(r'.*(.)\1.*(.)\2.*', pw):
            for i in range(len(ab)):
                t = ab[i:i + 3]
                if len(t) == 3 and t in pw:
                    return pw
        pw = day11_alpha_inc(pw)


def day10(i: int, digits: str = '1113122113'):
    while i > 0:
        numerals: List[str] = []
        while len(digits) > 0:
            m = re.match(r'(\d)\1*', digits)
            if m:
                numerals.append(m.group())
                digits = digits[m.end():]

        for n in numerals:
            c = len(n)
            digits += str(c) + n[0]
        i -= 1
    return digits


def day9(distances=None):
    if not distances:
        distances = input('day9.txt')

    parsed: List[List[str]] = []
    for d in distances:
        s = d.split()
        s.remove('to')
        s.remove('=')
        parsed.append(s)

    stops: List[str] = []
    for d in parsed:
        if d[0] not in stops:
            stops.append(d[0])
        if d[1] not in stops:
            stops.append(d[1])

    # this is probably unnecessary
    legs = pd.DataFrame(columns=stops, index=stops)
    for d in parsed:
        legs.loc[d[0], d[1]] = d[2]
        legs.loc[d[1], d[0]] = d[2]

    # TODO that for/enumerate/if loop is clumsy - fix it
    # maybe lookup distances directly in parsed[] instead of legs[DF]?
    journeys: Dict[str, int] = {}
    itineraries = itertools.permutations(stops)
    for i in itineraries:
        d = 0
        for n, s in enumerate(i):
            if n + 1 < len(i):
                d += int(legs.loc[s, i[n + 1]])
        journeys[i] = d

    return (min(journeys.values()), max(journeys.values()))


# TODO change these all to re.sub / skip the if clauses
def day8(strings=None):
    if not strings:
        with open('input_2015/day8.txt', 'r') as input:
            strings = input.read().split()

    raw = sum(map(len, strings))

    def decode(strings):
        decoded = 0

        for s in strings:
            t = s.strip('"')
            if r'\x' in t:
                t = re.sub(r'(\\x[a-fA-F0-9]{2})', '_', t)
            if r'\"' in t:
                t = t.replace(r'\"', '_')
            if r'\\' in t:
                t = t.replace(r'\\', '_')
            decoded += len(t)

        return raw - decoded

    def encode(strings):
        encoded = 0
        # TODO this modifies strings in place - make a copy instead?
        for s in strings:
            if '\"' in s:
                s = s.replace('\"', '__')
            if '\\' in s:
                s = s.replace('\\', '__')
            encoded += len(s) + 2

        return encoded - raw

    return {'part1': decode(strings), 'part2': encode(strings)}


def day7(instructions=None):
    # For part 1, replace line 1 of day7.txt with '1674 -> b'
    if not instructions:
        instructions = input('day7.txt')

    wires: Dict[str, int] = {}

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


def day6_part2(instructions: Optional[List[str]] = None) -> int:
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


def day6_part1(instructions: Optional[List[str]] = None) -> int:
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
            lights[start[0]:end[0] + 1, start[1]:end[1] + 1] = np.bitwise_xor(lights[start[0]:end[0] + 1, start[1]:end[1] + 1], 1)

    return np.sum(lights)


def day5_part2(strings: Optional[List[str]] = None) -> int:
    if not strings:
        strings = input('day5.txt')

    results: List[bool] = []
    for s in strings:
        nice = False
        if re.search(r'(\w)\w\1', s) and re.search(r'(\w{2}).*\1', s):
            nice = True

        results.append(nice)

    return results.count(True)


def day5_part1(strings: Optional[List[str]] = None) -> int:
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


def day3_part2(arrows: Optional[str] = None) -> int:
    if not arrows:
        with open('input_2015/day3.txt', 'r') as input:
            arrows = input.read()

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
        if here in presents:
            presents[here] += 1
        else:
            presents[here] = 1

    return len(presents)


def day3_part1(arrows: Optional[str] = None) -> int:
    if not arrows:
        with open('input_2015/day3.txt', 'r') as input:
            arrows = input.read()

    location: Dict[str, int] = {'x': 0, 'y': 0}
    presents: Dict[str, int] = {'[0, 0]': 2}

    for a in arrows:
        if a == '>':
            location['y'] += 1
        if a == '<':
            location['y'] -= 1
        if a == '^':
            location['x'] += 1
        if a == 'v':
            location['x'] -= 1

        here = str(list(location.values()))
        if here in presents:
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
        with open('input_2015/day1.txt', 'r') as input:
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
    if len(basement) > 0:
        b = basement[0]
    else:
        b = 0
    return {'floor': floor, 'basement': b}
