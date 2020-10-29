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
import json
import math
import operator
import re
import string
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd


def input(filename: str):
    with open('input_2015/' + filename, 'r') as input:
        data = [x.strip() for x in input]

    return data


def day25(size: List[int], target: Tuple[int, int] = None):
    if not target:
        target = (2980, 3074)  # subtract one from requested row, col for zero-indexing

    def remainder(a, b):
        return b - (math.floor(b / a) * a)

    code = np.zeros(size, dtype="int")
    code[0][0] = 20151125

    coordinates = [(x, y) for x in range(size[0] - 1) for y in range(size[1] - 1)]
    zigzag = sorted(sorted(coordinates, key=lambda x: x[1]), key=lambda x: sum(x))

    for c in zigzag[1:]:
        prev = (c[0] + 1, c[1] - 1)
        if -1 in prev:
            prev = (0, c[0] - 1)

        a = code[prev[0]][prev[1]]
    #     code[c[0]][c[1]] = a + 1
        code[c[0]][c[1]] = remainder(33554393, a * 252533)

    return code[target[0]][target[1]]


def day23(commands=None):
    p1 = {"a": 0, "b": 0}
    p2 = {"a": 1, "b": 0}
    if not commands:
        commands = input("day23.txt")

    # 'hlf r' sets register r to half its current value
    # 'tpl r' sets register r to triple its current value
    # 'inc r' increments register r, adding 1 to it
    # 'jmp offset' is a jump; it continues with the instruction offset away relative to itself.
    # 'jie r', offset is like jmp, but only jumps if register r is even ("jump if even").
    # 'jio r', offset is like jmp, but only jumps if register r is 1 ("jump if one", not odd).
    def assemble(reg):
        i = 0
        while i < len(commands):
            c = commands[i].split(' ')
            if c[0] == 'hlf':
                reg[c[1]] = reg[c[1]] / 2
                i += 1
            if c[0] == 'tpl':
                reg[c[1]] = reg[c[1]] * 3
                i += 1
            if c[0] == 'inc':
                reg[c[1]] += 1
                i += 1
            if c[0] == 'jmp':
                i += int(c[1])
            if c[0] == 'jie':
                if reg[c[1].strip(',')] % 2 == 0:
                    i += int(c[2])
                else:
                    i += 1
            if c[0] == 'jio':
                if reg[c[1].strip(',')] == 1:
                    i += int(c[2])
                else:
                    i += 1

        return reg

    return {"part1": assemble(p1)["b"], "part2": assemble(p2)["b"]}


def day21():
    boss = {'HP': 103, "damage": 9, "armor": 2}
    player = {}
    weapons = ["Weapons:    Cost  Damage  Armor",
               "Dagger        8     4       0",
               "Shortsword   10     5       0",
               "Warhammer    25     6       0",
               "Longsword    40     7       0",
               "Greataxe     74     8       0"]

    armor = ["Armor:      Cost  Damage  Armor",
             "Leather      13     0       1",
             "Chainmail    31     0       2",
             "Splintmail   53     0       3",
             "Bandedmail   75     0       4",
             "Platemail   102     0       5"]

    rings = ["Rings:      Cost  Damage  Armor",
             "Damage+1    25     1       0",
             "Damage+2    50     2       0",
             "Damage+3   100     3       0",
             "Defense+1   20     0       1",
             "Defense+2   40     0       2",
             "Defense+3   80     0       3"]

    def parse(tsv):
        splits = []
        for row in tsv:
            splits.append(row.split())
        return pd.DataFrame(splits[1:], columns=splits[0]).set_index(splits[0][0])

    # Damage is max(1, attacker_damage - defender_armor)
    def attack(p1, p2):
        return max(1, p1["damage"] - p2["armor"])

    # Player goes 1st
    def battle(player, boss):
        player["attack"] = attack(player, boss)
        boss["attack"] = attack(boss, player)
        while player["HP"] > 0:
            #         print("Player: " + str(player["HP"]) + ", Boss: " + str(boss["HP"]))
            boss["HP"] -= player["attack"]
            if boss["HP"] > 0:
                player["HP"] -= boss["attack"]
            else:
                return "Boss"
        return "Player"

    none = pd.DataFrame({"None": {"Cost": "0", "Damage": "0", "Armor": "0"}}).transpose()
    weapons = parse(weapons)
    armor = pd.concat([parse(armor), none])
    rings = pd.concat([parse(rings), none])
    ring_combos = list(itertools.combinations(rings.index, 2))

    outcomes = []
    for w in weapons.index:
        for a in armor.index:
            for r in ring_combos:
                # there must be a better way to write these
                cost = sum(map(int, [weapons.loc[(w, "Cost")], armor.loc[(a, "Cost")], rings.loc[r[0], "Cost"], rings.loc[r[1], "Cost"]]))
                player["damage"] = sum(map(int, [weapons.loc[(w, "Damage")], armor.loc[(a, "Damage")], rings.loc[r[0], "Damage"], rings.loc[r[1], "Damage"]]))
                player["armor"] = sum(map(int, [weapons.loc[(w, "Armor")], armor.loc[(a, "Armor")], rings.loc[r[0], "Armor"], rings.loc[r[1], "Armor"]]))

                player["HP"] = 100
                boss["HP"] = 103

                outcomes.append([cost, w, a, r, battle(player, boss)])

    results = {}

    victories = [x for x in outcomes if x[-1] == "Boss"]
    victories.sort()
    results['part1'] = victories[0][0]

    losses = [x for x in outcomes if x[-1] == "Player"]
    losses.sort(reverse=True)
    results['part2'] = losses[0][0]

    return results


def day20():
    def p1_elves(n):
        visits = set()
        for i in range(1, math.ceil(n / 2) + 1):
            if n % i == 0:
                visits.update([i, int(n / i)])

        return sum(visits) * 10

    def p2_elves(n):
        visits = set()
        for i in range(1, math.ceil(n / 2) + 1):
            if n % i == 0:
                if n <= 50 * i:
                    visits.add(i)
                if n <= 50 * int(n / i):
                    visits.add(int(n / i))

        return sum(visits) * 11

    results = {}
    for n in range(750000, 800000):
        if p1_elves(n) >= 33100000:
            results["part1"] = n
        if p2_elves(n) >= 33100000:
            results["part2"] = n

    return results


# def day19_part2(subs=None, molecule=None):
#     if not subs:
#         i = input("day19.txt")
#         molecule = i[-1]
#         s = [x.split(" => ") for x in i[-2]]
#     else:
#         s = [x.split(" => ") for x in subs]


def day19_part1(subs=None, molecule=None):
    if not subs:
        i = input("day19.txt")
        molecule = i[-1]
        subs = [x.split(" => ") for x in i[:-2]]
    else:
        subs = [x.split(" => ") for x in subs]

    results = []
    for x in range(0, len(molecule)):
        n = molecule[x:]
        p = molecule[:x]
        for s in subs:
            q = p + n.replace(s[0], s[1], 1)
            results.append(q)

    while molecule in results:
        results.remove(molecule)

    return len(set(results))


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

    # Part 2: Obviously, this is Conway's Game of Life, or it would be except
    # that 4 lights are stuck on, one in each corner. How many lights are on
    # after 100 cycles of this defective grid?

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

    # Part 1: You have a grid of 100x100 lights, which start with some on and
    # some off. Each light turns on or off based on its neighbors:

    # - a light which is on will stay on if 2 or 3 of its neighbors are on,
    # otherwise it will turn off
    # - a light which is off will turn on if exactly 3 neighbors are on,
    # otherwise it will stay off

    # Lights at the edge of the grid have fewer than 8 neighbors. All lights
    # update at the same time, using the same current state. How many lights
    # are on after 100 steps?

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

    # Part 1: Given a list of container sizes, how many combinations will hold
    # 150L of eggnog? Containers must be filled completely.

    # Part 2: How many valid combinations are there with the minimum number of
    # containers?

    if not containers:
        containers = list(map(int, input("day17.txt")))

    combos = []
    for i in range(len(containers)):
        combos += itertools.combinations(containers, i)

    part1 = [x for x in combos if sum(x) == eggnog]
    part2 = [x for x in part1 if len(x) == len(part1[0])]
    return {"part1": len(part1), "part2": len(part2)}


def day16():

    # Part 1: You need to figure out which one of your 500 Aunts Sue sent you a
    # gift. Luckily, you have a machine to detect the presence of various scents
    # and a list of what you recall about each Aunt. If the list doesn't mention
    # it, that doesn't mean that Aunt doesn't have it, just that you don't
    # recall.

    # Part 2: Rereading the instruction manual, you realize the machine results
    # are ranges in some cases: there are more cats and trees than indicated,
    # and fewer pomeranians and goldfish. Now which Aunt Sue is the best match?

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

    # Part 1: You're baking cookies, and want to find the best recipe. Each
    # ingredient in your kitchen has a different value for capacity, durability,
    # flavor, texture, and calories. The best cookie will be scored by the
    # product of the sums of the products of each ingredient's properties and
    # its quantity, which must add up to 100. If any property gives a negative
    # sum, it contributes 0. To begin with, ignore calories. For example:

    # Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    # Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3

    # A mixture of 44 tsp. Butterscotch and 56 tsp. Cinnamon results in:
    # capacity: 44*-1 + 56*2 = 68
    # durability: 44*-2 + 56*3 = 80
    # flavor: 44*6 + 56*-2 = 152
    # texture: 44*3 + 56*-1 = 76

    # The total score for this recipe is 68 * 80 * 152 * 76 = 62842880.

    # Given your actual ingredients, what is the score of the highest-scoring
    # cookie you can bake?

    # Part 2: What is the score of the highest-scoring cookie with a calorie
    # count of exactly 500?

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

    # Part 2: The scoring system has been changed, so that the reindeer(s) in
    # the lead at the end of every second get a point. After 2503 seconds, how
    # many points does the winning reindeer have?

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

    # Part 1: It's the Reindeer Olympics! You have a list of reindeer stats,
    # summarizing how fast they travel for how long, and how long they have to
    # rest before they can travel again. After 2503 seconds, how far has the
    # winning reindeer travelled?

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

    # Part 2: You forgot to seat yourself at the table! You're pretty apathetic
    # about the whole situations, thought, so you have a change in happiness of
    # zero for all pairings, and vice versa. What is the total change in
    # happiness for the best arrangement now?

    if not relations:
        relations = input("day13.txt")

    guests = set([s.split()[0] for s in relations])
    for g in guests:
        relations.append(g + " would gain 0 happiness units by sitting next to Talia.")
        relations.append("Talia would gain 0 happiness units by sitting next to " + g)

    return day13_part1(relations)


def day13_part1(relations=None):

    # Part 1: You are determining the seating arrangement for dinner by
    # optimizing for the total happiness of the guests. You have a list giving
    # the loss or gain for each pair of diners. What is the total change in
    # happiness for the best arrangement?

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


def day12(j=None):

    # Part 1: Given a JSON blob containing object, arrays, numbers, and strings,
    # what is the sum of all the numbers?

    if not j:
        j = input("day12.txt")

    part1 = sum(list(map(int, re.sub(r'[^0-9-]', ' ', j[0]).split())))

    def is_red(obj):
        if "red" in obj.values():
            return None
        return obj

    k = json.loads(j[0], object_hook=is_red)
    part2 = sum(list(map(int, re.sub(r'[^0-9-]', ' ', str(k)).split())))

    return {"part1": part1, "part2": part2}


def day11_alpha_inc(s):
    ab = string.ascii_lowercase
    while len(s) > 0:
        i = ab.index(s[-1])
        if i == 25:
            return day11_alpha_inc(s[:-1]) + "a"
        else:
            return s[:-1] + ab[i + 1]


def day11(pw=None):

    # Part 1: Santa is creating a new password by incrementing his previous
    # password until it passes the following criteria:

    # - must include at least one sequence of consecutive increasing letters,
    # like 'abc' or 'def', not 'abd'
    # - must not include 'i', 'o', or 'l'
    # - must contain at least 2 different pairs of letters, like 'bbazz'

    # Given the current password, what is the next valid password? Increment
    # alphabetically, wrapping around at z, e.g. bb, bc, bd...xx, xy, xz, ya, yb...

    # Part 2: What is the next valid password after the one you found in Part 1?

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

    # Part 1: Given an initial string, the next string consists of the spoken
    # description of that string.

    # - 1 expands to "one 1" -> 11
    # - 11 expands to "two 1s" -> 21
    # - 21 expands to "one 2, one 1" -> 1211

    # After 40 cycles, how long is the result?

    # Part 2: How long is the resulting number after 50 cycles?

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

    # Part 1: Given a list of cities and the distances between them, what is the
    # shortest distance you can travel, visiting each city exactly once? You may
    # start anywhere (and end somewhere else).

    # Part 2: What is the longest trip that visits each city exactly once?

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

    # Part 1: Given a string containing escaped literals (\\, \", \x27), what is
    # the difference between the number of characters in the code and the number
    # of characters in the rendered string?

    # - "" is 2 characters in code but 0 as a string
    # - "aaa\"aaa" is 10 characters in code but 7 as a string
    # - "\x27" is 6 characters in code but only 1 as a string (hex-encoded ASCII)

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

    # Part 2: Now go the other way, and encode each string by escaping each
    # backslash and quotation mark. What is the difference in the number of
    # characters in the encoded strings and the originals?

    # - "" encodes to "\"\"" for a total of 6 characters
    # - "aaa\"aaa" encodes to "\"aaa\\\"aaa\"" for a total of 16
    # - "\x27" encodes to "\"\\x27\"" for a total of 11

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

    # Part 1: You are given a set of instructions to assemble a set of logic gates.

    # - 123 -> x means that the signal 123 is provided to wire x.
    # - x AND y -> z means that the bitwise AND of wire x and wire y is
    # provided to wire z; x OR y -> z uses the bitwise OR
    # - p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2
    # and then provided to wire q. RSHIFT is the same but with right-shifting
    # - NOT e -> f means that the bitwise complement of the value from wire e
    # is provided to wire f.

    # Each wire can hold a value from 0 to 65535; every input must be provided
    # to a gate before it produces any output. What value is ultimately held
    # on wire a?

    # Part 2: Take the signal that arrived on wire a, set wire b to that value,
    # and reset all the other wires (including a). Now what value is held on wire a?

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


def day6(instructions: Optional[List[str]] = None) -> int:

    # Part 1: You have a grid of 1000x1000 lights and instructions to turn them on:

    # - turn on 0,0 through 999,999 means to turn on / leave on every light in
    # the rectangle between those coordinates, inclusive
    # - toggle 0,0 through 999,0 means to flip every light in the first row
    # - turn off 499,499 through 500,500 would turn off the middle 4 lights

    # After following all the directions in order, how many lights are turned on?

    # Part 2: In fact, you have mistranslated the directions. The lights have a
    # brightness setting, starting at zero. The actual instructions are:

    # - turn on means to increase the brightness by 1
    # - turn off means to decrease the brightness by 1
    # - toggle means to increase the brightness by 2

    # What is the total brightness of all the lights after executing all the instructions?

    part1 = np.zeros((1000, 1000), dtype=int)
    part2 = np.zeros((1000, 1000), dtype=int)

    if not instructions:
        instructions = input('day6.txt')

    for i in instructions:
        pieces = i.split()
        start = list(map(int, pieces[-3].split(',')))
        end = list(map(int, pieces[-1].split(',')))
        # target = [start[0]:end[0]+1, start[1]:end[1]+1]

        if pieces[1] == 'on':
            part1[start[0]:end[0] + 1, start[1]:end[1] + 1] = 1
            part2[start[0]:end[0] + 1, start[1]:end[1] + 1].__iadd__(1)
        if pieces[1] == 'off':
            part1[start[0]:end[0] + 1, start[1]:end[1] + 1] = 0
            part2[start[0]:end[0] + 1, start[1]:end[1] + 1].__isub__(1)
            np.clip(part2, 0, None, out=part2)
        if pieces[0] == 'toggle':
            part1[start[0]:end[0] + 1, start[1]:end[1] + 1] = np.bitwise_xor(part1[start[0]:end[0] + 1, start[1]:end[1] + 1], 1)
            part2[start[0]:end[0] + 1, start[1]:end[1] + 1].__iadd__(2)

    return {"part1": np.sum(part1), "part2": np.sum(part2)}


def day5(strings: Optional[List[str]] = None) -> int:

    # Part 1: Given a list of strings, how many satisfy the following requirements:

    # - contains at least 3 vowels (aeiou)
    # - contains at least one letter twice in a row (xx, abccde)
    # - does not contain the strings 'ab', 'cd', 'pq', 'xy'

    # Part 2: How many strings satisfy these requirements:

    # - contains a non-overlapping pair of any two letters at least twice
    # (xyxy, aabcdefaa, but not aaa which overlaps)
    # - contains at least one letter which repeats with one letter between them
    # (xyx, abcdefegh, aaa)

    if not strings:
        strings = input('day5.txt')

    part1: List[bool] = []
    part2: List[bool] = []

    for s in strings:
        nice = False
        if re.search(r'([aeiou].*){3}', s) and re.search(r'(\w)\1', s):
            nice = True
        if re.search(r'(ab|cd|pq|xy)', s):
            nice = False

        part1.append(nice)

        nice = False
        if re.search(r'(\w)\w\1', s) and re.search(r'(\w{2}).*\1', s):
            nice = True

        part2.append(nice)

    return {"part1": part1.count(True), "part2": part2.count(True)}


def day4(key: str = 'yzbqklnj') -> int:

    # Part 1: Given an initial key, find the lowest number which produces an MD5
    # hash with at least 5 leading zeros, when the number is appended to the key.

    # Part 2: Find the lowest number which produces a hash with 6 leading zeros.

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

    # Part 2: What if there are two Santas giving gifts, following every other
    # direction? How many houses receive gifts this year?

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

    # Part 1: Given a list of directions indicating each move (^, v, >, <),
    # starting at the origin of an infinite grid, how many houses receive
    # at least one present?

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

    # Part 1: Given a list of box dimensions, how much wrapping paper is
    # required? Each box requires enough paper to cover its sides (l*w + w*h +
    # h*l), plus the area of the smallest side.

    # Part 2: How much ribbon is required? For each gift, the ribbon must go
    # around the smallest perimeter (if h and w are the smallest edges, 2*(h+w))
    # plus a bow equal to the volume of the box (l*w*h).

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

    # Part 1: Given a set of instructions, where '(' means go up one floor, and
    # ')' means go down one floor, what floor do you end up on? You start on
    # floor 0.

    if not parens:
        with open('input_2015/day1.txt', 'r') as input:
            parens = input.read()

    # floor = parens.count('(') - parens.count(')')
    floor: int = 0
    basement: List[int] = []

    for i, p in enumerate(parens):
        if p == '(':
            floor += 1
        if p == ')':
            floor -= 1
        # if you reach the basement, make a note
        if floor == -1:
            basement.append(i + 1)

    # Part 2: What is the position of the first instruction that causes you to
    # enter the basement?

    if len(basement) > 0:
        b = basement[0]
    else:
        b = 0

    return {'floor': floor, 'basement': b}
