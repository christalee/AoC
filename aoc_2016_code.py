# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016
# http://adventofcode.com/2016/


import copy
import hashlib
import pprint
import re
import string
from typing import Dict, List, Optional, Union

import numpy as np


def input(filename: str):
    with open('input_2016/' + filename, 'r') as input:
        data = [x.strip() for x in input]

    return data


def day20(blocked=None):
    if not blocked:
        blocked = input('day20.txt')
    blocked = [list(map(int, x.split('-'))) for x in blocked]
    blocked.sort()

    lowest = blocked[0][1] + 1
    allowed = []
    for x, y in blocked:
        if x > lowest:
            allowed.extend(range(lowest, x))
        if y > lowest:
            lowest = y + 1

    return {'part1': allowed[0], 'part2': len(allowed)}


def day19(size=3001330):
    elves = list(range(size))
    while len(elves) > 1:
        for i, e in enumerate(elves):
            elves.pop((i + 1) % len(elves))

    return elves[0] + 1


def day18(size, row=None):

    # Problem: You face a room with 40 rows of tiles, some of which are safe (.) and some are traps (^). Given the layout of the first row, you can determine the layout of the next row by following the rules below.

    # Rules:
    # For each tile, look at the tile in the prior row and the two adjacent to that tile. Call these tiles the left, center, and right tiles. A new tile is a trap if:
    #   - The left and center tiles are traps, but the right tile is not.
    #   - The center and right tiles are traps, but the left tile is not.
    #   - Only the left tile is a trap.
    #   - Only the right tile is a trap.
    # The wall (end of each row) counts as safe; any tile that is not a trap per these rules is safe.

    # Part 1: How many safe tiles are in this room?
    if not row:
        row = input('day18.txt')

    def traps(row):
        newrow = ''
        for x in range(len(row)):
            c = row[x]
            if x == 0:
                l = '.'
            else:
                l = row[x - 1]

            if x == len(row) - 1:
                r = '.'
            else:
                r = row[x + 1]

            if (l == c == '^' and r == '.') or (c == r == '^' and l == '.') or (l == c == '.' and r == '^') or (c == r == '.' and l == '^'):
                newrow += '^'
            else:
                newrow += '.'

        return newrow

    maze = row
    for x in range(size - 1):
        maze.append(traps(maze[-1]))
    count = 0
    for r in maze:
        count += r.count('.')

    return count


def day17(seed='yjjvjgan'):
    path = ''
    location = [0, 0]
    pathlist = {path: location}

    def pathfind(pathlist):
        newpaths = {}
        for (path, location) in pathlist.items():
            if location == [3, 3]:
                newpaths = path
                break
            else:
                m = hashlib.md5()
                m.update((seed + path).encode())
                doors = [x in 'bcdef' for x in m.hexdigest().lower()[0:4]]
                options = [d[0] for d in list(zip('UDLR', doors)) if d[1]]

                for o in options:
                    q = copy.deepcopy(location)
                    if o == "U":
                        if q[1] == 0:
                            pass
                        else:
                            q[1] -= 1
                    if o == "D":
                        if q[1] == 3:
                            pass
                        else:
                            q[1] += 1
                    if o == "R":
                        if q[0] == 3:
                            pass
                        else:
                            q[0] += 1
                    if o == "L":
                        if q[0] == 0:
                            pass
                        else:
                            q[0] -= 1

                    p = path + o
                    newpaths[p] = q

        return newpaths

    while not isinstance(pathlist, str):
        pathlist = pathfind(pathlist)

    return pathlist


def day16(disk: int, seed: Optional[str] = None):

    if not seed:
        seed = '11100010111110100'

    # Problem: you need to generate random data to fill a disk and calculate its checksum. Given an initial seed value, you generate data this way:

    # Call the data you have at this point "a".
    # Make a copy of "a"; call this copy "b".
    # Reverse the order of the characters in "b".
    # In "b", replace all instances of 0 with 1 and all 1s with 0.
    # The resulting data is "a", then a single 0, then "b".

    def datagen(a):
        b = a[::-1]
        b = b.translate(str.maketrans('01', '10'))
        return a + '0' + b

    # Repeat until you have enough data to fill the disk; discard any extra data.
    while len(seed) < disk:
        seed = datagen(seed)
    seed = seed[0:disk]

    # Once you have enough, calculate the checksum this way:

    # Break the data into pairs.
    # If the pair is two identical digits (11 or 00), the checksum digit is 1. If not (01 or 10), it's 0.
    # The result should be half the length of the initial data. If the length of the checksum is even, calculate its checksum.
    # Repeat until you have a checksum with an odd length.

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

    def gen_hash(y):
        m = hashlib.md5()
        m.update(y.encode())

        return m.hexdigest().lower()

    def stretch_hash(y):
        for i in range(2017):
            m = hashlib.md5()
            m.update(y.encode())
            y = m.hexdigest().lower()

        return m.hexdigest().lower()

    def find_keys(hashfn):
        keys = {}
        hashes = {}
        quints = {k: {} for k in '0123456789abcdef'}
        triples = {k: {} for k in '0123456789abcdef'}
        index = 0

        while len(keys) < 64:
            for x in range(index, index + 5000):
                y = salt + str(x)
                hashes[x] = hashfn(y)

            for n in hashes:
                t = re.search(r'([a-f0-9])\1\1', hashes[n])
                if t:
                    triples[t.group()[0]][n] = hashes[n]

                q = re.search(r'([a-f0-9])\1\1\1\1', hashes[n])
                if q:
                    quints[q.group()[0]][n] = hashes[n]

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

    # Generating fn:
    # Find x*x + 3*x + 2*x*y + y + y*y.
    # Add your puzzle input.
    # Find the binary representation of that sum; count the number of bits that are 1.
    # If the number of bits that are 1 is even, it's an open space.
    # If the number of bits that are 1 is odd, it's a wall.

    def g(q):
        def f(x, y):
            v = bin(x * x + 3 * x + 2 * x * y + y + y * y + q)
            return v.count('1') % 2
        return f

    # since numpy arrays are indexed as (row, column), goal must be given as (y, x)
    position = (1, 1)
    paths = [['start', position]]
    h = g(seed)
    maze = np.array([[h(x, y) for x in range(60)] for y in range(60)])

    def pathfind(pathlist):
        newpaths = []
        for p in pathlist:
            if p[-1] == goal:
                newpaths = len(p) - 2
                break
            else:
                newpaths.extend(nextstep(p))

        return newpaths

    def nextstep(steps):
        x, y = steps[-1]
        around = [a for a in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                  if (maze[a] == 0 and a not in steps and -1 not in a)]
        options = []
        for n in around:
            q = copy.deepcopy(steps)
            q.append(n)
            options.append(q)

        return options

    # TODO refactor this to use a real while loop
    while not isinstance(paths, int):
        paths = pathfind(paths)

    return paths


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


def day11():
    # Rules:
    # 1. You and the elevator begin on F1.
    # 2. At all times, each floor (+ elevator) can only contain all generators, all microchips, nothing, or a combination such that all microchips are with their generators. (A generator may hang out without its microchip.)
    # 3. The elevator only moves one floor at a time.
    # 4. The elevator will only move at least one and no more than two generators or microchips.
    # 5. The goal is to get all microchips and generators (10) to F4.

    # Strategy
    # 0. Write a fn to evaluate if moves are valid.
    # 1. state = [all floors + elevator] -> store in a list? after each move, or a dictionary where each state is a key?
    # 2. Increment count carefully everytime a move is successfully made
    # 3. Store each state in a tuple with its move count
    # 4. For each state, increment the count, then locate the elevator, then check for valid moves among the elevator cargo and its floor -> one floor up or down.
    # 5. Also write a move function to get things in and out of the elevator -> appended to the correct floor.
    # 6. If a move is valid, execute it (make copies?). If the final state is not already in the dict of states, add it along with its count.
    # 7. Do I need to sort things before I put them in the dict so they compare properly? what a headache.

    # represent state as a list with 4 elements, representing each floor of the building.
    # elements: thulium (Tm), plutonium (Pu), strontium (Sr), promethium (Pr), ruthenium (Ru)
    # F4:
    # F3: PrG, PrM, RuG, RuM
    # F2: PuM, SrM
    # F1: TmG, TmM, PuG, SrG, E

    state = [[["Tm.G", "Tm.M", "Pu.G", "Sr.G"],
              ["Pu.M", "Sr.M"],
              ["Pr.G", "Pr.M", "Ru.G", "Ru.M"],
              [""]]]
    elevator = 0
    moves = 0
    paths = {str(state): moves}

    def onetwo(x):
        y = [([a, b] if (not a == b) and (a < b) else [a]) for a in x for b in x]
        return y

    # next moves: find the elevator, take 1 or 2 items to the adjacent floors
    # takes a state s [from the previous m], and returns a list of states m
    def nextmoves(s):
        m = []
        e = s[-1]
        lowdest = e - 1
        highdest = e + 1

        for item in onetwo(s[e]):
            if lowdest > 0:
                y = copy.deepcopy(s)
                for x in item:
                    y[e].remove(x)
                y[lowdest].extend(item)
                m.append(y.append(lowdest))

            if highdest < 5:
                y = copy.deepcopy(s)
                for x in item:
                    y[e].remove(x)
                y[highdest].extend(item)
                m.append(y.append(highdest))
        return m

    def isvalid(s):
        e = s.pop()
        for a in s[e][:]:
            a = a.partition(".")
            if a[2] == "M":
                pass

    # Code below here needs to be rewritten
    #
    # # For a given state, determine whether it violates any of the rules above, returning True or False accordingly. (Create a list of T/F tests and make sure all are T? Or is that clumsy?)
    # # invalid moves: anything that leaves a microchip without its corresponding generator
    # def isValid(s):
    #     location = s['E']
    #
    #     # the floor is empty
    #     if len(s[location]) == 0:
    #         return True
    #
    #     for x in s[location]:
    #         element = x[0]
    #         component = x[1]
    #         tx = []
    #         for y in s[location]:
    #             ty = []
    #             if element == y[0]:
    #                 ty.append[True]
    #         # Need to revisit all this logic: is this the best way to track what combinations are ok?
    #         if t == [True, True]:
    #             return True
    #         else:
    #             return False
    #
    #
    #
    # while len(state['F4']) < 10:
    #     # generate a list of possible next states
    #     n = nextStates(state)
    #     # add valid states + move count to statedict
    #     for each in n:
    #         if isValid(each):
    #             if str(each) not in statedict:
    #                 statedict[str(each)] = count
    #             # TODO need to figure out how to represent states as keys; maybe write a function for it?
    #
    #     count += 1
    #     # recurse on all valid states? what does count do on recursion?
    #
    # # at the end, print the first state where all items are on F4? use that to look up its count in the dictionary? or just print count directly?
    # print statedict
    # print count


def day11_test():

    # store each item as a dictionary? label floors with strings or in variables?
    # F1 = {'TmG': {'element': 'Tm', 'type': 'G'}, }

    state = {
        4: [],
        3: [('Pr', 'G'), ('Pr', 'M'), ('Ru', 'G'), ('Ru', 'M')],
        2: [('Pu', 'M'), ('Sr', 'M')],
        1: [('Tm', 'G'), ('Tm', 'M'), ('Pu', 'G'), ('Sr', 'G')],
        'E': 1
    }

    # change this to be just lists?
    state = {
        '4': [],
        '3': [('Li', 'G')],
        '2': [('H', 'G')],
        '1': [('H', 'M'), ('Li', 'M')],
        'E': [2]
    }

    moves = 0

    statedict = {str(state): moves}

    # given a state s, returns a list of reachable states ms
    def nextmoves(s):
        ms = []
        for each in s:
            location = each['E'][0]
            up = location + 1
            down = location - 1
        # Elevator can move 1 or 2 items in location, to either of the nextlocations.
            x = copy.deepcopy(s)
            x[str(location)].remove()
            for item in things:
                pass
                # currently only moves 1 item. How to move two? "choose any two?"
                #        moveUp = transfer(s, item, str(location + 1))
                #        moveDown = transfer(s, item, str(location -1))
                #        moves.extend([moveUp, moveDown])
        return ms

    # don't need this?
    def transfer(s, item, floor):
        # need to make copies, not modify s itself
        for each in s:
            if item in s[each]:
                s[each].remove(item)
        s[floor].append(item)
        return s

    def isValid(s):
        location = str(s['E'][0])

        # the floor is empty
        if len(s[location]) == 0:
            return True

        for x in s[location]:
            element = x[0]
            component = x[1]
            tx = []
            for y in s[location]:
                ty = []
                if element == y[0]:
                    ty.append[True]
            # Need to revisit all this logic: is this the best way to track what combinations are ok?
            if t == [True, True]:
                return True
            else:
                return False


def river():

    # represent state as a list with 2 elements, representing each side of the river. Items: Boat, Chicken, Fox, Wheat (alphabetical)
    state = [[["B", "C", "F", "W"], [""]]]
    moves = 0
    paths = {str(state): moves}

    # next moves: from the side containing B, can take 0 or 1 item to the other side
    # invalid moves: anything that leaves the C with the W, or the F with the C

    def nextmoves(s):
        # takes a state s, and returns a list of states m
        m = []
        for each in s:
            if "B" in each:
                origin = s.index(each)
                destination = origin - 1
                # first, just move the boat without anything in it
                x = copy.deepcopy(s)
                x[origin].remove("B")
                x[origin].sort()
                x[destination].append("B")
                x[destination].sort()
                m.append(x)

                # next, move each item on the boat's original side to the other side
                # note: you already moved the boat, so you don't have to do it again
                for i in x[origin]:
                    y = copy.deepcopy(x)
                    y[origin].remove(i)
                    y[origin].sort()
                    y[destination].append(i)
                    y[destination].sort()
                    m.append(y)
        return m

    def isvalid(s):
        # takes a state s, returns whether it is a permissible state or not
        for each in s:
            if ("B" not in each) and ("C" in each) and (("W" in each) or ("F" in each)):
                return False
            else:
                return True

    # given a list of states s, generate all the possible next moves
    # if each next move is valid and it's not already in the path dict, add it along with the # of moves
    # repeat using the items of the path dict with value moves + 1

    # keep a list version of the state in s (pass it in as a parameter?) and put a string version into paths

    def iterstate(ss, p, m):
        while True:
            ts = []
            m += 1
            if ss == []:
                return p
            for x in ss:
                for y in nextmoves(x):
                    if y == [[""], ["B", "C", "F", "W"]]:
                        return y, m
                    if isvalid(y) and (str(y) not in p):
                        ts.append(y)
                        p[str(y)] = m
            ss = ts

    return iterstate(state, paths, moves)


def day10(commands=None):

    if not commands:
        commands = input('day10.txt')

    # Part 1: You have instructions for a system of numbered bots that take in numbers, compare them, and deposit them into output bins. Bots don't take any action until they have two numbers to compare. Which bot compares 61 to 17?

    # For each command, I need to parse whether it's an input value or a bot output. How should I represent bots and output bins? Will it work to parse out all the input values and then run all the bot outputs? Or do I have to run through the list (recursively?) checking for bots that have 2 values and activating them?

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
        for c in commands:
            x = c.split()

            # populate each bot with its initial values
            if x[0] == 'value':
                deposit(bots[(x[4] + x[5])], int(x[1]))

    # Given a bot or bin, deposit the number in one of the bot's slots or the bin.
    def deposit(bot, x):
        if 'value' in bot:
            bot['value'] = x
        if 'low' in bot:
            if not bot['low']:
                bot['low'] = x
            elif x > bot['low']:
                bot['high'] = x
            elif x < bot['low']:
                bot['high'] = bot['low']
                bot['low'] = x

    # If a bot has both values, compare & send them to lowdest and highdest and reset them to False (?)
    def botrun():
        for b in bots.values():
            if ('low' in b) and b['low'] and b['high']:
                deposit(bots[b['lowdest']], b['low'])
                deposit(bots[b['highdest']], b['high'])
                b['low'] = False
                b['high'] = False

    # 250 runs turns out to be sufficient to reach steady state.
    bots = {}
    botnames()
    for i in range(250):
        botvals()
        botrun()

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

    # Switch from recursion to iteration.
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

    # Start at the beginning of the string. Find the first '('. Partition at the first ')'after that. Extract the rlen and rx from [0], and slice out s = [2][0:rlen]. Build up decompressed by adding rx*s. Recurse? on the string after the slice.

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

    # 'rect AxB' turns on all of the pixels in a rectangle A px wide by B px tall at the top-left of the screen.

    # 'rotate row y=A by B' shifts all of the pixels in row A (0 is the top row) right by B px. Pixels that would fall off the right end appear at the left end of the row.

    # 'rotate column x=A by B' shifts all of the pixels in column A (0 is the left column) down by B px. Pixels that would fall off the bottom appear at the top of the column.

    # numpy handles arrays well, let's use it here
    # numpy arrays index as (# of rows, # of cols)
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


def day7_part2(ips=None):
    # Part 2: Strings are valid if they contain a 3 character palindrome (e.g. aba, sms) outside square brackets AND the corresponding inverse (e.g. sms -> msm) inside square brackets.

    # Given a string, test each set of 3 consecutive characters for palindromes
    # Return a list for further testing
    def xyx(s):
        trigrams = [s[i - 1:i + 1] for i in range(1, len(s) - 1) if (s[i - 1] == s[i + 1] and s[i] != s[i - 1])]
        return trigrams

    # Given two lists of strings, check each item of a for matchng any item in b
    # NOTE: this checks the reverse of x against y; maybe rename this or reverse before passing into the fn? or when generating trigrams?

    def matches(a, b):
        return True in [True for x in a for y in b if x[::-1] == y]

    count = 0
    if not ips:
        ips = input('day7.txt')
    for i in ips:
        outbs = []
        inbs = []

        # Split each string up by square brackets
        x = i.split(']')
        for y in x:
            if '[' in y:
                z = y.partition('[')
                # Collect valid trigrams found outside square brackets
                outbs.extend(xyx(z[0]))
                # Ditto, inside square brackets
                inbs.extend(xyx(z[2]))
            # what to do if '[' isn't found (last segment)
            else:
                outbs.extend(xyx(y))

        if matches(outbs, inbs):
            count += 1

    return count


def day7_part1(ips=None):
    # Part 1: Strings are valid if they contain a 4 character palindrome (e.g. abba, smms), unless the palindrome is inside square brackets or the characters are all the same (e.g. nnnn). How many of the given strings are valid?

    # Given a string, test each set of 4 consecutive characters for palindromes
    # Return True if any 4 are valid, otherwise False
    def abba(s):
        tf = [(s[i] == s[i + 1]) and (s[i - 1] == s[i + 2]) and (s[i] != s[i - 1]) for i in range(1, len(s) - 2)]
        return True in tf

    count = 0
    if not ips:
        ips = input('day7.txt')
    for i in ips:
        outbs = []
        inbs = []

        # Split each string up by square brackets
        x = i.split(']')
        for y in x:
            if '[' in y:
                z = y.partition('[')
                if abba(z[0]):
                    outbs.append(True)
                if abba(z[2]):
                    inbs.append(True)
            # Check the last segment too
            elif abba(y):
                outbs.append(True)

        if True in outbs and True not in inbs:
            count += 1

    return count


def day6(messages=None):

    # Problem: Given a list of strings, find the most common character in each column.

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


def day5_part2(doorid: str = 'abbhdwsy') -> str:

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


def day5_part1(doorid: str = 'abbhdwsy') -> str:

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


def day4(rooms: Optional[List[str]] = None) -> Dict[str, int]:

    # Part 1: You are given a list of rooms formatted as a name (lowercase letters separated by dashes) followed by a dash, a sector ID, and a checksum in square brackets. A room name is valid if the checksum is the five most common letters in the encrypted name, in order, with ties broken by alphabetization. What is the sum of the sector IDs for all the valid rooms?

    if not rooms:
        rooms = input('day4.txt')
    # Start with each room name in a list of strings
    r = [y for x in rooms for y in x.split()]

    idsum = 0
    p2 = 0
    for x in r:
        # Split each name into the [checksum], the sector ID, and the name, stripping out dashes
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
            if 'north' in realname:
                p2 = int(sectorid)
            else:
                pass

    return {'part1': idsum, 'part2': p2}


def day3_check(triplet: List[int]) -> bool:
    c = max(triplet)
    triplet.remove(c)
    a, b = triplet
    if a + b > c:
        return True
    else:
        return False


def day3(triangles=None) -> Dict[str, int]:

    # Problem: given a list of numbers, separate them into groups of 3. How many of these groups could be the sides of a triangle (a + b > c)?
    if not triangles:
        triangles = input('day3.txt')
    htri: List[List[int]] = [list(map(int, x.split())) for x in triangles]

    # Part 2: Separate the numbers into groups of 3 down columns, not across rows, then check for triangles
    i = range(0, len(htri), 3)
    vtri: List[List[int]] = [list(y) for x in i for y in zip(htri[x], htri[x + 1], htri[x + 2])]

    # because day3_check modifies its input, don't run it until htri and vtri are both populated
    p1: int = len([x for x in htri if day3_check(x)])
    p2: int = len([x for x in vtri if day3_check(x)])

    return {'part1': p1, 'part2': p2}


def day2_part2(keys=None):

    # Problem: Starting from the 5 of a 13-digit keypad, follow the given directions (Up, Down, Left, Right) to find each digit of a passcode. Skip any direction that leads off the edge of the keypad.

    # Keypad
    #        1
    #    2   3   4
    # 5  6   7   8   9
    #    A   B   C
    #        D

    if not keys:
        keys = input('day2.txt')

    # Consider the keypad as a coordinate grid, and start at key 5
    keypad = {'[0, 2]': '1',
              '[-1, 1]': '2', '[0, 1]': '3', '[1, 1]': '4',
              '[-2, 0]': '5', '[-1, 0]': '6', '[0, 0]': '7', '[1, 0]': '8', '[2, 0]': '9',
              '[-1, -1]': 'A', '[0, -1]': 'B', '[1, -1]': 'C',
              '[0, -2]': 'D'
              }
    coordinates = [-2, 0]

    # Two cases to handle movement on the interior and the edges. I'm pretty sure there's a more elegant way to do this.
    keycode = ''
    for each in keys:
        for direction in each:
            s = abs(coordinates[0]) + abs(coordinates[1])
            if s < 2:
                if direction == "U":
                    coordinates[1] += 1
                if direction == "D":
                    coordinates[1] -= 1
                if direction == "R":
                    coordinates[0] += 1
                if direction == "L":
                    coordinates[0] -= 1
            if s == 2:
                if direction == "U" and coordinates[1] in [-1, -2]:
                    coordinates[1] += 1
                if direction == "D" and coordinates[1] in [1, 2]:
                    coordinates[1] -= 1
                if direction == "R" and coordinates[0] in [-1, -2]:
                    coordinates[0] += 1
                if direction == "L" and coordinates[0] in [1, 2]:
                    coordinates[0] -= 1
        keycode += keypad[str(coordinates)]

    return keycode


def day2_part1(keys=None):

    # Problem: Starting from the 5 of a 9-digit keypad, follow the given directions (Up, Down, Left, Right) to find each digit of a passcode. Skip any direction that leads off the edge of the keypad.

    # Keypad
    # 1 2 3
    # 4 5 6
    # 7 8 9

    if not keys:
        keys = input('day2.txt')

    # Consider the keypad as a coordinate grid, and start at key 5
    keypad = {
        '[-1, 1]': '1', '[0, 1]': '2', '[1, 1]': '3',
        '[-1, 0]': '4', '[0, 0]': '5', '[1, 0]': '6',
        '[-1, -1]': '7', '[0, -1]': '8', '[1, -1]': '9'
    }
    coordinates = [0, 0]

    # Two cases to handle movement on the interior and the edges. I'm pretty sure there's a more elegant way to do this.
    keycode = ''
    for each in keys:
        for direction in each:
            if direction == "U":
                if coordinates[1] == 1:
                    pass
                else:
                    coordinates[1] += 1
            if direction == "D":
                if coordinates[1] == -1:
                    pass
                else:
                    coordinates[1] -= 1
            if direction == "R":
                if coordinates[0] == 1:
                    pass
                else:
                    coordinates[0] += 1
            if direction == "L":
                if coordinates[0] == -1:
                    pass
                else:
                    coordinates[0] -= 1
        keycode += keypad[str(coordinates)]

    return keycode


def day1(path: Optional[str] = None) -> Dict[str, int]:
    # Part 1: You are given a series of directions indicating a direction to turn and a number of blocks of travel on a grid. How many blocks away from the origin do you end up? Count total blocks as x + y, not as the crow flies.

    if not path:
        path = input('day1.txt')
    path: List[str] = path[0].split(', ')

    # Start at the origin facing direction North = 0.
    # var coordinates holds a list of points visited.
    facing: int = 0
    coordinates: List[List[int]] = [[0, 0]]

    # Processing each direction
    for step in path:
        # start at the last known coordinate
        nextstep: List[int] = coordinates[-1][:]
        # break the direction into a turn and a distance
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

    # Part 2: How many blocks away is the first location you visit twice?
    doubles: List[List[int]] = list(filter(lambda point: coordinates.count(point) >= 2, coordinates))

    results = {}
    results['final'] = sum(map(abs, coordinates[-1]))
    if len(doubles) > 0:
        results['HQ'] = sum(map(abs, doubles[0]))
    return results
