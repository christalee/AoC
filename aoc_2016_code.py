# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016
# http://adventofcode.com/2016/


import copy
import hashlib
import itertools
import re
import string
from typing import Dict, List, Optional

import numpy as np
import pandas as pd


def input(filename: str):
    with open('input_2016/' + filename, 'r') as input:
        data = [x.strip() for x in input]

    return data

# day25 - see day25.ipynb for details
# Problem: using the assembler from day23, find the lowest positive integer that will produce a clock signal (0, 1, 0, 1...) when input as register a.

# Solution: This problem has no tgl instructions, but it adds an 'output x' that sends x to the antenna. Collecting 100 samples of signal in a list allows me to test a range of inputs and check the output against the desired [0, 1] * 50; maybe not the most elegant but it does work.

# TODO translate all this assembly into the corresponding loops and operations


def day24(raw=None):

    # Part 1: given a maze and a robot that can only move in x and y, what is the least number of steps required to visit all the goals (marked with integers), starting from location 0?

    # Part 2: What is the least number of steps required to visit all the goals and then return to location 0?

    # Another pathfinding problem, hooray
    # First, draw the map and locate all the goal locations
    if not raw:
        raw = input('day24.txt')
    chars = list(map(list, raw))
    maze = np.array(chars, ndmin=2)

    goals = {}
    # TODO is there a simpler way of extracting the goal locations?
    i = np.nditer(maze, flags=['multi_index'], op_flags=['readwrite'])
    while not i.finished:
        if np.char.isdecimal(i[0]):
            goals[int(i[0])] = i.multi_index
        i.iternext()

    # cf. day13, pathfinding utilities
    def pathfind(border):
        nonlocal d, visited
        newborder = []
        for p in border:
            if p == goal:
                return d
            else:
                newborder.extend(nextstep(p))

        d += 1
        visited = visited | set(newborder)
        return list(set(newborder))

    def nextstep(point):
        x, y = point
        around = [a for a in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                  if (maze[a] != '#' and a not in visited)]

        return around

    # cf. aoc_2015_code/day9, populate a table with distances for each trip leg
    g = list(goals.keys())
    g.sort()
    distances = pd.DataFrame(columns=g, index=g)

    for (x, y) in itertools.combinations(g, 2):
        if pd.isna(distances.loc[x, y]):
            visited = set([goals[x]])
            goal = goals[y]
            d = 0
            frontier = [goals[x]]

            while not isinstance(frontier, int):
                frontier = pathfind(frontier)

            distances.loc[x, y] = frontier
            distances.loc[y, x] = frontier

    # Starting from 0, find the total distance for each possible trip
    g.remove(0)
    x = itertools.permutations(g)
    trips = {}
    rounds = {}

    for itinerary in x:
        itinerary = (0,) + itinerary
        d = 0
        for i, s in enumerate(itinerary):
            if i + 1 < len(itinerary):
                d += int(distances.loc[s, itinerary[i + 1]])
        trips[itinerary] = d
        rounds[itinerary] = d + int(distances.loc[itinerary[-1], 0])

    # Sort the results and return the shortest trip and roundtrip
    t = sorted(trips, key=lambda x: trips[x])
    r = sorted(rounds, key=lambda x: rounds[x])

    return {'part1': trips[t[0]], 'part2': rounds[r[0]]}

# day23 - see day23.ipynb for details
# Problem: given a set of assembly instructions, similar to those in day12, what value is left in register a for an input value of a = 7? a = 12?

# Solution: This problem adds a 'tgl x' instruction that flips the instruction x away ('inc' -> 'dec', 'dec' -> 'inc', 'tgl' -> 'inc', 'cpy' -> 'jnz', 'jnz' -> 'cpy'). After implementing that and inspecting the register periodically for a range of input values, I noticed the instructions calculate factorial(a) + 85*76. This is quite slow & expensive for a = 12, since 'inc' is the only operation available, so a closed-form solution is preferable by far.

# TODO translate all this assembly into the corresponding loops and operations

# day22 - see day22.ipynb for details
# Part 1: Given the disk space Used/Available for each node in a massive storage cluster, how many pairs of nodes exist in the grid, such that the current contents of node A could fit on node B if it were empty?

# Solution: I parsed the input into a pandas DataFrame to facilitate further calculation. From there, it was straightforward (though slow) to count up each pair of nodes which met the stated criteria.

# Part 2: You would like to transfer all the data from the top right node to the top left node. Unfortunately there's only 1 node currently empty, and some nodes are so large/full they're effectively unmoveable. What is the smallest number of transfers required to move the data?

# Solution: This was simplest to solve by inspection; I printed the maze, with each node symbolized by a '.' for regular nodes, '*' for unmoveable nodes, and '_' for the empty node. Then I could easily count how many steps were needed to reach the top row and move the data from one end to the other.


def day21(pw=None, commands=None):

    # Part 1: Given an input string and a set of scrambling instructions, what is the resulting output?

    if not pw:
        pw = 'abcdefgh'
    if not commands:
        commands = input('day21.txt')

    # Commands:
    # 'swap position X with position Y' swaps the letters at indices X and Y
    # 'swap letter X with letter Y'
    # 'rotate left/right X steps'
    # 'rotate based on position of letter X' means find the index of X, add 1, and if the result is > 4, add 1 again. Then rotate right that many steps.
    # 'reverse positions X through Y' means reverse the substring from indices X to Y
    # 'move position X to position Y' means remove the letter at index X and insert it at index Y

    def scramble(text):
        letters = list(text)

        for com in commands:
            c = com.split(' ')
            x = c[2]
            y = c[-1]

            if c[0] == 'swap':
                newtext = letters[:]
                if c[1] == 'position':
                    newtext[int(x)] = letters[int(y)]
                    newtext[int(y)] = letters[int(x)]
                if c[1] == 'letter':
                    newtext[letters.index(x)] = y
                    newtext[letters.index(y)] = x

            if c[0] == 'rotate':
                if c[1] == 'left':
                    newtext = letters[int(x):] + letters[0:int(x)]
                if c[1] == 'right':
                    newtext = letters[-int(x):] + letters[0:-int(x)]
                if c[1] == 'based':
                    i = letters.index(y) + 1
                    if i >= 5:
                        i += 1
                    i = i % len(letters)
                    newtext = letters[-i:] + letters[0:-i]

            if c[0] == 'reverse':
                ss = letters[int(x):int(y) + 1]
                newtext[int(x):int(y) + 1] = ss[::-1]

            if c[0] == 'move':
                l = letters.pop(int(x))
                letters.insert(int(y), l)
                newtext = letters[:]

            letters = newtext

        return ''.join(letters)

    # Part 2: Given an output string that has already been scrambled, what was the input string?

    # Solution: The simplest way to handle this was to scramble all the possible input strings and check which one gave the requested output.

    pws = itertools.permutations('abcdefgh')
    for p in pws:
        if scramble(p) == 'fbgdceah':
            p2 = ''.join(p)

    return {'part1': scramble(pw), 'part2': p2}


def day20(blocked=None):

    # Problem: given a list of blacklisted IP ranges, written as 32-bit integers, what is the lowest-valued IP that is not blocked? How many IPs are allowed?

    # Solution: Start by parsing the input into a sorted list of ranges.

    if not blocked:
        blocked = input('day20.txt')
    blocked = [list(map(int, x.split('-'))) for x in blocked]
    blocked.sort()

    # Keep track of the lowest integer that's excluded from each range (greater than the end of the range). Append any IPs between that lowest IP and the bottom of the next range to the list of allowed IPs.

    lowest = blocked[0][1] + 1
    allowed = []
    for x, y in blocked:
        if x > lowest:
            allowed.extend(range(lowest, x))
        if y > lowest:
            lowest = y + 1

    return {'part1': allowed[0], 'part2': len(allowed)}


def day19(size=3001330):

    # Part 1: Imagine a circle of elves, numbered from 1, each holding a gift. Going around the circle in order, each elf steals a gift from the elf on their left. Any elf without a gift is removed from the circle. Which elf ends up with all the gifts?

    # Part 2: Imagine instead that the elves steal gifts from the elf directly across the circle from them, or the elf on the left (from the stealer's view) if there are two options. Now which elf ends up with all the gifts?

    # Solution: First I solved this problem by walking the list, which was prohibitively slow for large n

    # p1 = list(range(size))
    # while len(p1) > 1:
    #     for i, e in enumerate(p1):
    #         p1.pop((i + 1) % len(p1))

    # Seriously, this code threatened to run for 24+ hrs

    # p2 = list(range(size))
    # while len(p2) > 1:
    #     ref = copy.deepcopy(p2)
    #     for r in ref:
    #         if r in p2:
    #             x = p2.index(r)
    #             p2.pop((x + math.floor(len(p2) / 2)) % len(p2))
    #             if r == p2[x - 2]:
    #                 break

    # I tried speeding up execution with threading or multiprocessing, but concluded that the computation is CPU-bound and modifies a single massive data structure - I would have to chunk it manually. Along the way, I ran the above code for n from 2 to 50. Noticing a pattern in the output, I derived a formula for both results (see day19.ipynb to visualize)

    # part1: 2^n = 1, then follow 2^n odd numbers (so the last is 2^n+1 - 1 : 2^n+1 - 1)
    def part1(x):
        powers = [2**n for n in range(25)]
        odds = [1 + 2 * n for n in range(x)]

        t = [a for a in powers if a <= x]
        r = x - t[-1]
        return odds[r]

    # part2: 1 : 1, if n : n then start 1, 2, 3 until n : n/2, then continue sequence of odds until n : n
    def part2(x):
        odds = [1 + 2 * n for n in range(x)]

        for r in range(15):
            if 3**r >= x:
                a = r - 1
                break

        p = 3**a
        r = x - p
        d = 3**(a + 1) - p

        if r <= d // 2:
            y = r
        else:
            s = r - d // 2
            i = odds.index(p)
            y = odds[i + s]

        return y

    # These solutions return in less than a second!
    return {'part1': part1(size), 'part2': part2(size)}


def day18(size, row=None):

    # Problem: You face a room with many rows of tiles, some of which are safe (.) and some are traps (^). Given the layout of the first row, you can determine the layout of the next row by following the rules below. How many safe tiles are in a room with 40 rows? How many in a room with 400000 rows?

    # Rules:
    # For each tile, look at the tile in the prior row and the two adjacent to that tile. Call these tiles the left, center, and right tiles. A new tile is a trap if:
    #   - The left and center tiles are traps, but the right tile is not.
    #   - The center and right tiles are traps, but the left tile is not.
    #   - Only the left tile is a trap.
    #   - Only the right tile is a trap.
    # The wall (end of each row) counts as safe; any tile that is not a trap per these rules is safe.

    if not row:
        row = input('day18.txt')

    def traps(row):
        newrow = ''
        for x in range(len(row)):
            # going down the row, check what's to the left and right of each char
            c = row[x]
            if x == 0:
                l = '.'
            else:
                l = row[x - 1]

            if x == len(row) - 1:
                r = '.'
            else:
                r = row[x + 1]

            # traps happen when lcr = 110, 011, 100, or 001
            if (l == c == '^' and r == '.') or (c == r == '^' and l == '.') or (l == c == '.' and r == '^') or (c == r == '.' and l == '^'):
                newrow += '^'
            else:
                newrow += '.'

        return newrow

    # Build up the maze row by row
    maze = row
    for x in range(size - 1):
        maze.append(traps(maze[-1]))

    # Then count the number of safe tiles
    count = 0
    for r in maze:
        count += r.count('.')

    return count


def day17(seed='yjjvjgan'):

    # Problem: You are trapped in a 4x4 maze of rooms. At every step, the state of the doors in your current room are determined by the md5 hash of your puzzle input + your path so far (Up, Down, Left, Right). The first 4 characters of the hash correspond to the doors leading Up, Down, Left, and Right: open if the char is b-f, closed if a0-9. The walls of the maze have no doors, of course.

    #########
    #S| | | #
    #-#-#-#-#
    # | | | #
    #-#-#-#-#
    # | | | #
    #-#-#-#-#
    # | | |E#
    #########

    # Part 1: What is the shortest path from the top left to the bottom right?

    # Part 2: What is the length of the longest path that reaches the bottom right? Recall that once a path reaches the goal, all the doors open and the path ends.

    # Solution: Starting at [0, 0], accumulate a list of paths and their ending locations. If they reach the goal or deadend (all doors closed), add them to the appropriate list. Otherwise, keep stepping.

    path = ''
    location = [0, 0]
    pathlist = [[path, location]]
    results = []
    deadends = []

    # TODO review vs. day13, day24

    # This does the bulk of the work: hashing, determining which doors are open/closed, checking for walls, and adding the path to deadends if no doors are open.
    def doorfind(steps):
        path, location = steps
        m = hashlib.md5()
        m.update((seed + path).encode())
        doors = [x in 'bcdef' for x in m.hexdigest().lower()[0:4]]
        o = [d[0] for d in list(zip('UDLR', doors)) if d[1]]

        if ('U' in o and location[1] == 0):
            o.remove('U')
        if ("D" in o and location[1] == 3):
            o.remove('D')
        if ("R" in o and location[0] == 3):
            o.remove('R')
        if ("L" in o and location[0] == 0):
            o.remove('L')

        if o == []:
            deadends.append(path)

        return o

    # Given a [path, location], return the updated [path, location] for each open door
    # Note that if the path is a deadend, it returns []
    def nextstep(steps):
        path, location = steps
        options = []
        doors = doorfind(steps)

        for o in doors:
            q = copy.deepcopy(location)
            if o == "U":
                q[1] -= 1
            elif o == "D":
                q[1] += 1
            elif o == "R":
                q[0] += 1
            elif o == "L":
                q[0] -= 1

            p = path + o
            options.append([p, q])

        return options

    # This adds paths to results if they reach the goal [3, 3], and otherwise accumulates possible next steps. Any deadend path contributes nothing to newpaths.
    def pathfind(paths):
        newpaths = []
        for p in paths:
            if p[1] == [3, 3]:
                results.append(p[0])
            else:
                newpaths.extend(nextstep(p))

        return newpaths

    # Loop until all paths have either reached the goal or deadended.
    while len(pathlist) > 0:
        pathlist = pathfind(pathlist)

    # Since the search is breadth-first, the last result is the longest.
    return {"part1": results[0], "part2": len(results[-1])}


def day16(disk, seed=None):

    if not seed:
        seed = '11100010111110100'

    # Problem: you need to generate random data to fill a disk and calculate its checksum. Given an initial seed value, what is the checksum for a disk of size 272? What is the checksum for a disk of size 35651584?

    # First, generate data this way:
    # - Call the data you have at this point "a".
    # - Make a copy of "a"; call this copy "b".
    # - Reverse the order of the characters in "b".
    # - In "b", replace all instances of 0 with 1 and all 1s with 0.
    # - The resulting data is "a", then a single 0, then "b".

    def datagen(a):
        b = a[::-1]
        b = b.translate(str.maketrans('01', '10'))
        return a + '0' + b

    # Repeat until you have enough data to fill the disk; discard any extra data.
    while len(seed) < disk:
        seed = datagen(seed)
    seed = seed[0:disk]

    # Next, calculate the checksum this way:
    # - Break the data into pairs.
    # - If the pair is two identical digits (11 or 00), the checksum digit is 1. If not (01 or 10), it's 0.
    # - The result should be half the length of the initial data. If the length of the checksum is even, calculate its checksum.
    # - Repeat until you have a checksum with an odd length.

    def checksum(a):
        pairs = [a[x] + a[x + 1] for x in range(0, len(a), 2)]
        check = ''
        for each in pairs:
            if each[0] == each[1]:
                check += '1'
            else:
                check += '0'
        if len(check) % 2 == 1:
            return check
        else:
            return checksum(check)

    return checksum(seed)


def day15():

    # Problem: You have a machine of disks which rotate every second. You want to release a capsule at the top at the right time to pass through to the bottom. Each disk is 1s apart and has a slot at position 0. Given the initial positions and number of positions on each disk, at what time should you release the capsule?

    d1 = {'init': 1, 'rank': 1, 'mod': 13}
    d2 = {'init': 10, 'rank': 2, 'mod': 19}
    d3 = {'init': 2, 'rank': 3, 'mod': 3}
    d4 = {'init': 1, 'rank': 4, 'mod': 7}
    d5 = {'init': 3, 'rank': 5, 'mod': 5}
    d6 = {'init': 5, 'rank': 6, 'mod': 17}
    d7 = {'init': 0, 'rank': 7, 'mod': 11}

    p1 = [d1, d2, d3, d4, d5, d6]
    p2 = p1 + [d7]

    # Track global time t. Code each disk's position mod the time. Update each position until every disk reads 0 at the same time.

    def check(disks):
        time = 0
        while True:
            total = 0
            for d in disks:
                total += (d['init'] + time + d['rank']) % d['mod']
            if total == 0:
                return time

            time += 1

    return {'part1': check(p1), 'part2': check(p2)}


def day14(salt='zpqevtbw'):

    # Problem: You are looking for 64 one-time pad keys. To find each key, determine the md5 hash of your input salt with an index that starts at 0 and increases each time. A key is valid if the lowercase hexadecimal representation of the md5 result contains 3 characters in a row AND a hash containing the same characters 5 times in a row occurs in the next 1000 hashes.

    # Part 1: What index produces your 64th key?
    def gen_hash(y):
        m = hashlib.md5()
        m.update(y.encode())

        return m.hexdigest().lower()

    # Part 2: instead of simply hashing once, hash 2016 additional times! Now what index produces your 64th key?
    def stretch_hash(y):
        for i in range(2017):
            m = hashlib.md5()
            m.update(y.encode())
            y = m.hexdigest().lower()

        return m.hexdigest().lower()

    # Since part 2 uses a different hash fn, pass that as a parameter
    def find_keys(hashfn):
        keys = {}
        hashes = {}
        index = 0
        # quints and triples are dicts of dicts, with a key for each hex char
        quints = {k: {} for k in '0123456789abcdef'}
        triples = {k: {} for k in '0123456789abcdef'}

        # Starting from index 0, search in chunks of 5000
        while len(keys) < 64:
            for x in range(index, index + 5000):
                y = salt + str(x)
                hashes[x] = hashfn(y)

            # If a hash contains 3 or 5 of any char, store it in the appropriate subdict with index n as the key, with the char as the top-level key
            for n in hashes:
                t = re.search(r'([a-f0-9])\1\1', hashes[n])
                if t:
                    triples[t.group()[0]][n] = hashes[n]

                q = re.search(r'([a-f0-9])\1\1\1\1', hashes[n])
                if q:
                    quints[q.group()[0]][n] = hashes[n]

            # For each index in triples[k], check for any index in quints[k] in the next 1000 ints
            for k in quints:
                qvals = quints[k]
                tvals = triples[k]
                for q in qvals:
                    for t in tvals:
                        if q in range(t + 1, t + 1001):
                            keys[t] = tvals[t]

            index += 5000

        return sorted(list(keys.keys()))[63]

    return {'part1': find_keys(gen_hash), 'part2': find_keys(stretch_hash)}


def day13(goal=(39, 31), seed=1350):

    # Part 1: Given a map of a space defined by the function below, what is the shortest path from (1,1) to (31, 39)? You may not move diagonally.

    # Part 2: How many locations (including (1, 1)) can you reach in 50 steps?

    # Generating fn:
    # - Find x*x + 3*x + 2*x*y + y + y*y.
    # - Add your puzzle input.
    # - Find the binary representation of that sum; count the number of bits that are 1.
    # - If the number of bits that are 1 is even, it's an open space.
    # - If the number of bits that are 1 is odd, it's a wall.

    def g(q):
        def f(x, y):
            v = bin(x * x + 3 * x + 2 * x * y + y + y * y + q)
            return v.count('1') % 2
        return f

    h = g(seed)
    maze = np.array([[h(x, y) for x in range(60)] for y in range(60)])

    # Solution: Keep a list of the farthest locations you can reach in d steps, and a list of locations you've already visited.

    # Note: since numpy arrays are indexed as (row, column), goal must be given as (y, x)
    frontier = [(1, 1)]
    visited = set(frontier)
    points = 0
    d = 0

    # TODO this is nearly identical to day24, refactor?
    def pathfind(border):
        nonlocal d, visited, points

        # Part 2: how many points can you reach in 50 steps?
        if d == 50:
            points = len(visited)

        # For each current location, return the number of steps d if you've reached the goal; otherwise, accumulate a list of possible next steps
        newborder = []
        for p in border:
            if p == goal:
                return d
            else:
                newborder.extend(nextstep(p))

        # Increment the number of steps d, add any new locations you've reached to visited, and deduplicate the next steps in newborder
        d += 1
        visited = visited | set(newborder)
        return list(set(newborder))

    # Given a point, return the adjacent points that are open (0), not a wall (-1) and haven't already been visited
    def nextstep(point):
        x, y = point
        around = [a for a in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                  if (maze[a] == 0 and a not in visited and -1 not in a)]

        return around

    while not isinstance(frontier, int):
        frontier = pathfind(frontier)

    return {'part1': frontier, 'part2': points}


def day12(commands=None):

    # Part 1: You are given a set of assembly instructions, operating on 4 registers initialized to 0. What value does register a hold when the instructions terminate?

    # Part 2: What value does register a hold if register c is initialized to 1?

    p1 = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    p2 = {'a': 0, 'b': 0, 'c': 1, 'd': 0}

    # Commands:
    # 'cpy x y' copies x (either an integer or the value of a register) into register y.
    # 'inc x' increases the value of register x by one.
    # 'dec x' decreases the value of register x by one.
    # 'jnz x y' jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.

    if not commands:
        commands = input('day12.txt')

    # Instructions are followed in order from the beginning until no more remain; use i to track progress through the list
    def assemble(reg):
        i = 0

        while i < len(commands):
            c = commands[i].split(' ')
            if c[0] == 'cpy':
                if c[1] in reg.keys():
                    reg[c[2]] = reg[c[1]]
                else:
                    reg[c[2]] = int(c[1])
                i += 1
            if c[0] == 'inc':
                reg[c[1]] += 1
                i += 1
            if c[0] == 'dec':
                reg[c[1]] -= 1
                i += 1
            if c[0] == 'jnz':
                if c[1] in reg.keys():
                    if not reg[c[1]] == 0:
                        i += int(c[2])
                    else:
                        i += 1
                elif not int(c[1]) == 0:
                    i += int(c[2])
                else:
                    i += 1

        return reg['a']

    return {'part1': assemble(p1), 'part2': assemble(p2)}


def day11(floors=None):

    # Problem: You are located on the 1st floor of a building containing various microchips and generators. How many moves will it take to transport all the chips and generators to the 4th floor, without frying any of the microchips?

    # Rules:
    # - At all times, each floor can only contain all generators, all microchips, nothing, or a combination such that all microchips are with their corresponding generators. A generator may hang out without its microchip.
    # - The elevator only moves one floor at a time.
    # - The elevator will only move at least one and no more than two generators or microchips.

    # Solution: represent state as a list containing an int for the elevator location and a list for each floor of the building.
    # for best results, sort the initial state

    # F3:
    # F2: PG, PM, RG, RM
    # F1: UM, SM
    # F0: TG, TM, UG, SG, (EM, EG, DM, DG)

    # Part 1 elements: elements: thulium (T), plutonium (U), strontium (S), promethium (P), ruthenium (R)
    p1 = [[0,
           ["SG", "TG", "TM", "UG"],
           ["SM", "UM"],
           ["PG", "PM", "RG", "RM"],
           []]]

    # Part 2 elements: as above, plus elerium (E), dilithium (D) on floor 0
    p2 = [[0,
           ["DG", "DM", "EG", "EM", "SG", "TG", "TM", "UG"],
           ["SM", "UM"],
           ["PG", "PM", "RG", "RM"],
           []]]

    # Given a list of 4 floors, confirm that it follows the rules for chips and generators
    # TODO this could be more efficient, I think (or is the slowdown elsewhere?)
    def validate(state):
        checks = []
        for floor in state:
            if isinstance(floor, int) or len(floor) <= 1:
                checks.append(True)
            else:
                for a, b in itertools.combinations(floor, 2):
                    if a[-1] == "M" and b[-1] == "G" and a[0] + "G" not in floor:
                        checks.append(False)
                    if b[-1] == "M" and a[-1] == "G" and b[0] + "G" not in floor:
                        checks.append(False)

        return False not in checks

    # Given a floor, return a list of lists containing its contents taken 1 or 2 at a time
    def taketwo(x):
        y = list(map(list, itertools.combinations(x, 2)))
        for i in x:
            y.append([i])

        return y

    # Given a list of 4 floors and a list of items to move from start to end, return the updated list of floors (sorted, so states can be compared)
    def move(state, item, start, end):
        y = copy.deepcopy(state)
        for x in item:
            y[start].remove(x)
        y[end].extend(item)

        for f in y:
            f.sort()

        return y

    # To find possible next moves, try moving every 1 or 2 items on the current floor to the floor directly above or below. If the result is a valid state, add it to the list
    def nextmoves(s):
        elevator = s[0]
        floors = s[1:]
        m = []
        lower = elevator - 1
        higher = elevator + 1
        options = taketwo(floors[elevator])

        if lower >= 0:
            for o in options:
                n = move(floors, o, elevator, lower)
                if validate(n):
                    m.append([lower] + n)

        if higher < 4:
            for o in options:
                n = move(floors, o, elevator, higher)
                if validate(n):
                    m.append([higher] + n)

        return m

    def pathfind(border):
        nonlocal moves, visited

        newborder = []
        for p in border:
            if len(p[-1]) == total:
                newborder = moves
                break
            else:
                for m in nextmoves(p):
                    if str(m) not in visited:
                        visited.add(str(m))
                        newborder.append(m)

        moves += 1
        return newborder

    def solve(floors):
        while not isinstance(floors, int):
            floors = pathfind(floors)
        return floors

    if not floors:
        return {'part1': solve(p1), 'part2': solve(p2)}
    else:
        return solve(floors)


def day10(commands=None):

    if not commands:
        commands = input('day10.txt')

    # Problem: You have instructions for a system of numbered bots that take in numbers, compare them, and deposit them into output bins. Bots don't take any action until they have two numbers to compare.

    # Solution: start by parsing the commands and populating a dict of bots, represented as dicts with fields for two values and the destination bins for each value; also a dict for each output bin, intially all set False

    def botnames():
        for c in commands:
            # 'bot 0 gives low to output 2 and high to output 0' ->
            x = c.split()

            # bots['bot0'] = {'low': False, 'high': False, 'lowdest': 'output2', 'highdest': 'output0'}}
            if x[0] == 'bot':
                bots[(x[0] + x[1])] = {'low': False, 'high': False, 'lowdest': x[5] + x[6], 'highdest': x[10] + x[11]}

            # bots['output2'] = {'value': False}
            if x[5] == 'output':
                bots[(x[5] + x[6])] = {'value': False}

            # bots['output0'] = {'value': False}
            if len(x) > 6 and x[10] == 'output':
                bots[(x[10] + x[11])] = {'value': False}

    def botvals():

        # Parse commands that assign values to various bots and bins

        for c in commands:
            x = c.split()

            if x[0] == 'value':
                deposit(bots[(x[4] + x[5])], int(x[1]))

    def deposit(bot, x):

        # Given a bot or bin, deposit the value in one of the bot's slots or the bin.

        # bins: just dump the value in
        if 'value' in bot:
            bot['value'] = x

        # bots: use the low slot if it's free, otherwise put the high and low values in the correct spots
        if 'low' in bot:
            if not bot['low']:
                bot['low'] = x
            elif x > bot['low']:
                bot['high'] = x
            elif x < bot['low']:
                bot['high'] = bot['low']
                bot['low'] = x

    def botrun():

        # If a bot has both values, send them to lowdest and highdest and reset them to False

        for b in bots.values():
            if ('low' in b) and b['low'] and b['high']:
                deposit(bots[b['lowdest']], b['low'])
                deposit(bots[b['highdest']], b['high'])
                b['low'] = False
                b['high'] = False

    # 250 runs turns out to be sufficient to reach steady state. Since botvals may have changed after botrun, keep it in the loop
    bots = {}
    botnames()
    for i in range(250):
        botvals()
        botrun()

    # Part 1: Which bot compares 61 to 17?

    bots_final = [x for x in iter(bots) if x.startswith('bot')]

    for x in bots_final:
        p1 = 0
        if bots[x]['low'] == 17 and bots[x]['high'] == 61:
            p1 = int(x.strip('bot'))
            break

    # Part 2: What is the product of the numbers in bins 0, 1, and 2?

    p2 = bots['output0']['value'] * bots['output1']['value'] * bots['output2']['value']

    return {'part1': p1, 'part2': p2}


def day9_part2(data=None):

    # Part 2: Turns out you need to expand markers within inserted text after all. What is the decompressed length of your file?

    # Solution: Switch from recursion to iteration.
    # TODO Can this be optimized?? Am I storing the expanded string or just its length? Can I batch process this somehow? or parallelize?
    # TODO timeit to confirm that this is RAM limited?

    def expand(s, d):
        i = 0
        while len(s) > 1:
            if s.startswith('('):
                x = s.partition(')')
                marker = x[0].strip('(').split('x')
                rlen = int(marker[0])
                rx = int(marker[1])
                repstr = x[2][0:rlen]
                s = repstr * rx + x[2][rlen:]
            else:
                x = s.partition('(')
                d += len(x[0])
                s = '(' + x[2]
            i += 1
            # Track progress during run
            if i % 100000 == 0:
                print(d, len(s))

        return d

    if not data:
        data = input('day9.txt')

    return expand(data[0], 0)


def day9_part1(data=None):

    # Part 1: You need to decompress a data file. Compression markers are contained in parentheses. (10x2) means to take the next 10 characters and insert them 2 times, then continue reading forward. Ignore whitespace and do not include the marker itself in the decompressed text to insert. However, parentheses and other special characters may appear in inserted text without denoting a compression marker. What is the length of your decompressed file?

    # Solution: Start at the beginning of the string. Find the first '('. Partition at the first ')'after that. Extract the rlen and rx from [0], and slice out s = [2][0:rlen]. Build up decompressed by adding rx*s. Recurse? on the string after the slice.

    def expand(s, d):
        if s.startswith('('):
            if len(s) == 1:
                return d
            else:
                x = s.partition(')')
                marker = x[0].strip('(').split('x')
                rlen = int(marker[0])
                rx = int(marker[1])
                repstr = x[2][0:rlen]
                d += len(repstr * rx)
                return expand(x[2][rlen:], d)
        else:
            x = s.partition('(')
            d += len(x[0])
            return expand('(' + x[2], d)

    if not data:
        data = input('day9.txt')

    return expand(data[0], 0)


def day8(ops=None):

    # Part 1: You are given a set of commands to execute on a screen 50 px wide by 6 px tall, which starts entirely off. How many pixels turn on?

    # Commands:
    # - 'rect AxB' turns on all of the pixels in a rectangle A px wide by B px tall at the top-left of the screen.
    # - 'rotate row y=A by B' shifts all of the pixels in row A (0 is the top row) right by B px. Pixels that would fall off the right end appear at the left end of the row.
    # - 'rotate column x=A by B' shifts all of the pixels in column A (0 is the left column) down by B px. Pixels that would fall off the bottom appear at the top of the column.

    # numpy handles arrays well, let's use it here
    # numpy indexes arrays as (# of rows, # of cols)
    screen = np.zeros((6, 50), dtype=int)

    # Given the dimensions of the rectangle as a string 'AxB', turn on those pixels
    def rect(r):
        r = r.split('x')
        screen[0:int(r[1]), 0:int(r[0])] = 1

    # Given the row/column index and shift amount, use numpy.roll to modify screen
    def rotate(rowcol, index, shift):
        i = int(index.split('=')[-1])
        if rowcol == "row":
            screen[i, :] = np.roll(screen[i, :], int(shift))
        if rowcol == "column":
            screen[:, i] = np.roll(screen[:, i], int(shift))

    if not ops:
        ops = input('day8.txt')

    for each in ops:
        r = each.split()
        if r[0] == "rect":
            rect(r[1])
        if r[0] == "rotate":
            rotate(r[1], r[2], r[4])

    # Part 2: The screen displays letters as capital letters 5 px wide. What code is displayed?

    # read straight off the terminal
    for x in range(0, screen.shape[1], 5):
        print(screen[:, x:x + 5])

    return np.sum(screen)


def day7_xyx(s):

    # Given a string, test each set of 3 consecutive characters for palindromes
    # Return a list for further testing

    trigrams = [s[i - 1:i + 1] for i in range(1, len(s) - 1) if (s[i - 1] == s[i + 1] and s[i] != s[i - 1])]

    return trigrams


def day7_matches(a, b):

    # Given two lists of strings, check each item of a for matchng any item in b
    # NOTE: this checks the reverse of x against y; maybe rename this or reverse before passing into the fn? or when generating trigrams?

    return True in [True for x in a for y in b if x[::-1] == y]


def day7_part2(ips=None):

    # Part 2: Strings are valid if they contain a 3 character palindrome (e.g. aba, sms) outside square brackets AND the corresponding inverse (e.g. sms -> msm) inside square brackets.

    if not ips:
        ips = input('day7.txt')

    count = 0

    for i in ips:
        outbs = []
        inbs = []

        # Split each string up by square brackets
        x = i.split(']')
        for y in x:
            if '[' in y:
                z = y.partition('[')
                # Collect valid trigrams found outside square brackets
                outbs.extend(day7_xyx(z[0]))
                # Ditto, inside square brackets
                inbs.extend(day7_xyx(z[2]))
            # what to do if '[' isn't found (last segment)
            else:
                outbs.extend(day7_xyx(y))

        if day7_matches(outbs, inbs):
            count += 1

    return count


def day7_abba(s):

    # Given a string, test each set of 4 consecutive characters for palindromes
    # Return True if any 4 are valid, otherwise False

    tf = [(s[i] == s[i + 1]) and (s[i - 1] == s[i + 2]) and (s[i] != s[i - 1]) for i in range(1, len(s) - 2)]

    return True in tf


def day7_part1(ips=None):

    # Part 1: Strings are valid if they contain a 4 character palindrome (e.g. abba, smms), unless the palindrome is inside square brackets or the characters are all the same (e.g. nnnn). How many of the given strings are valid?

    if not ips:
        ips = input('day7.txt')

    count = 0

    for i in ips:
        outbs = []
        inbs = []

        # Split each string up by square brackets
        x = i.split(']')
        for y in x:
            if '[' in y:
                z = y.partition('[')
                if day7_abba(z[0]):
                    outbs.append(True)
                if day7_abba(z[2]):
                    inbs.append(True)
            # Check the last segment too
            elif day7_abba(y):
                outbs.append(True)

        if True in outbs and True not in inbs:
            count += 1

    return count


def day6(messages=None):

    # Problem: Given a list of strings, find the most common and the least common character in each column.

    if not messages:
        messages = input('day6.txt')

    hwords = [y for x in messages for y in x.split()]
    # Reformat from rows to columns
    vwords = zip(*hwords)

    final = {'part1': '', 'part2': ''}
    for word in vwords:
        word = ''.join(word)
        counts = [(l, word.count(l)) for l in word]
        counts.sort(key=lambda l: l[1])
        final['part1'] += counts[-1][0]
        final['part2'] += counts[0][0]

    return final


def day5_part2(doorid='abbhdwsy'):

    # Problem: You are looking for an 8 character password. To find each character, determine the md5 hash of your input with an index that starts at 0 and increases each time. If the hexadecimal representation of the md5 result begins with 5 zeroes, the 7th digit is added to the password in the position given by the 6th digit. Only the first character found for each position is used, discard the rest.

    i: int = 0
    password: List[str] = ['_'] * 8

    # Run this loop until the password has changed from symbols to alphanumerics
    while not ''.join(password).isalnum():
        m = hashlib.md5()
        m.update((doorid + str(i)).encode())
        if m.hexdigest()[:5] == '00000' and m.hexdigest()[5].isdigit():
            position = int(m.hexdigest()[5])
            if position < 8 and password[position] == '_':
                password[position] = m.hexdigest()[6]
        i += 1

    return ''.join(password)


def day5_part1(doorid='abbhdwsy'):

    # Problem: You are looking for an 8 character password. To find each character, determine the md5 hash of your input with an index that starts at 0 and increases each time. If the hexadecimal representation of the md5 result begins with 5 zeroes, the 6th digit is appended to the password.

    i: int = 0
    password: str = ''

    # Run this loop until the password has changed from symbols to alphanumerics
    while len(password) < 8:
        m = hashlib.md5()
        m.update((doorid + str(i)).encode())
        if m.hexdigest()[:5] == '00000':
            password += m.hexdigest()[5]
        i += 1

    return password


def day4(rooms=None):

    # Part 1: You are given a list of rooms formatted as a name (lowercase letters separated by dashes) followed by a dash, a sector ID, and a checksum in square brackets. A room name is valid if the checksum is the five most common letters in the encrypted name, in order, with ties broken by alphabetization. What is the sum of the sector IDs for all the valid rooms?

    if not rooms:
        rooms = input('day4.txt')

    # Start by parsing out each room name
    r = [y for x in rooms for y in x.split()]
    idsum = 0
    p2 = 0

    for x in r:
        # Split each room into the [checksum], the sector ID, and the name, stripping out dashes
        parts = x.partition('[')
        checksum = parts[2].strip(']')
        rest = parts[0].rsplit('-', 1)
        sectorid = rest[1]
        name = rest[0].replace('-', '')

        # Alphabetize and deduplicate name into one string
        t = ''.join(sorted(set(name)))

        # Make a list of how often each letter appears in name
        counts = [(l, name.count(l)) for l in t]
        counts.sort(key=lambda l: l[1], reverse=True)

        # Take the 5 most common letters to compare to the checksum
        letters = ''.join([x[0] for x in counts[:5]])

        if letters == checksum:
            idsum += int(sectorid)

            ptext = []
            # string constant holding the alphabet
            a = string.ascii_lowercase

            for each in rest[0]:
                if each.isalpha():
                    # find the current position of the letter
                    cindex = a.index(each)
                    # shift each letter mod 26
                    ptext.append(a[(cindex + int(sectorid)) % 26])
                else:
                    # convert dashes to spaces
                    ptext.append(' ')

            realname = ''.join(ptext)

            # Part 2: in which room is the north pole?
            if 'north' in realname:
                p2 = int(sectorid)
            else:
                pass

    return {'part1': idsum, 'part2': p2}


def day3_check(triplet: List[int]) -> bool:

    # A helper function to check if a list of 3 integers makes a closed triangle.

    c = max(triplet)
    triplet.remove(c)
    a, b = triplet

    if a + b > c:
        return True
    else:
        return False


def day3(triangles=None):

    if not triangles:
        triangles = input('day3.txt')

    # Problem: given a list of numbers, separate them into groups of 3. How many of these groups could be the sides of a triangle (a + b > c)?

    htri: List[List[int]] = [list(map(int, x.split())) for x in triangles]

    # Part 2: Separate the numbers into groups by going down columns, not across rows, then check for triangles

    i = range(0, len(htri), 3)
    vtri: List[List[int]] = [list(y) for x in i for y in zip(htri[x], htri[x + 1], htri[x + 2])]

    # because day3_check modifies its input, don't run it until htri and vtri are both populated
    p1: int = len([x for x in htri if day3_check(x)])
    p2: int = len([x for x in vtri if day3_check(x)])

    return {'part1': p1, 'part2': p2}


def day2_solve(keys, keypad, location):
    keycode = ''

    for k in keys:
        for direction in k:
            next = copy.deepcopy(location)
            if direction == "U":
                next[1] += 1
            if direction == "D":
                next[1] -= 1
            if direction == "R":
                next[0] += 1
            if direction == "L":
                next[0] -= 1

            # Only make a move if it's an existing key!
            if str(next) in keypad:
                location = copy.deepcopy(next)

        # After each set of directions has been processed, add the current key to the keycode
        keycode += keypad[str(location)]

    return keycode


def day2(keys=None):

    if not keys:
        keys = input('day2.txt')

    # Part 1: Starting from key 5 of a 9-digit keypad, follow the given directions (Up, Down, Left, Right) to find each digit of a passcode. Skip any direction that leads off the edge of the keypad.

    # Keypad
    # 1 2 3
    # 4 5 6
    # 7 8 9

    # Solution: Consider the keypad as a coordinate grid, and start at key 5
    keypad_p1 = {'[-1, 1]': '1', '[0, 1]': '2', '[1, 1]': '3',
                 '[-1, 0]': '4', '[0, 0]': '5', '[1, 0]': '6',
                 '[-1, -1]': '7', '[0, -1]': '8', '[1, -1]': '9'
                 }

    origin_p1 = [0, 0]

    # Part 2: Solve as before, on a 13-digit keypad, starting at key 5 (coordinates (-2, 0)).

    # Keypad
    #        1
    #    2   3   4
    # 5  6   7   8   9
    #    A   B   C
    #        D

    keypad_p2 = {'[0, 2]': '1',
                 '[-1, 1]': '2', '[0, 1]': '3', '[1, 1]': '4',
                 '[-2, 0]': '5', '[-1, 0]': '6', '[0, 0]': '7', '[1, 0]': '8', '[2, 0]': '9',
                 '[-1, -1]': 'A', '[0, -1]': 'B', '[1, -1]': 'C',
                 '[0, -2]': 'D'
                 }

    origin_p2 = [-2, 0]

    return {'part1': day2_solve(keys, keypad_p1, origin_p1), 'part2': day2_solve(keys, keypad_p2, origin_p2)}


def day1(path=None):
    # Part 1: You are given a series of directions indicating a direction to turn and a number of blocks of travel on a grid. How many blocks away from the origin do you end up? Count total blocks as x + y, not as the crow flies.

    if not path:
        path = input('day1.txt')
    path: List[str] = path[0].split(', ')

    # Start at the origin facing direction North = 0 and keep a list of points visited.
    facing: int = 0
    coordinates: List[List[int]] = [[0, 0]]

    # Starting at the last known coordinate, break the direction into a turn and a distance, and update the location accordingly
    for step in path:
        nextstep: List[int] = coordinates[-1][:]
        turn: str = step[0]
        steps: int = int(step[1:])

        if turn == "R":
            facing += 1
        else:
            facing -= 1

        d: int = facing % 4

        while steps > 0:
            if d == 0:
                nextstep[1] += 1
            if d == 1:
                nextstep[0] += 1
            if d == 2:
                nextstep[1] -= 1
            if d == 3:
                nextstep[0] -= 1

            coordinates.append(nextstep[:])
            steps -= 1

    results = {'final': sum(map(abs, coordinates[-1]))}

    # Part 2: How many blocks away is the first location you visit twice?

    # Solution: Check your handy list for points that appear more than once
    doubles: List[List[int]] = list(filter(lambda point: coordinates.count(point) >= 2, coordinates))

    if len(doubles) > 0:
        results['HQ'] = sum(map(abs, doubles[0]))

    return results
