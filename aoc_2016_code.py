# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016
# http://adventofcode.com/2016/


def day1(input=False):
    # Part 1: You are given a series of directions indicating a direction to turn and a number of blocks of travel on a grid. How many blocks away from the origin do you end up? Count total blocks as x + y, not as the crow flies.

    if not input:
        input = open('day1.txt').read()

    # Given a string, convert to a list
    path = input.split(", ")

    # Start at the origin facing direction North = 0.
    # var coordinates holds a list of points visited.
    facing = 0
    coordinates = [[0, 0]]

    # Processing each direction
    for each in path:
        nextstep = coordinates[-1][:]   # start at the last known coordinate
        turn = each[0]                  # break the direction into a turn and a distance
        steps = int(each[1:])
        if turn == "R":
            facing += 1
        else:
            facing -= 1

        d = facing % 4
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

    #print("final location: " + str(coordinates[-1]))

    # Part 2: How many blocks away is the first location you visit twice?

    doubles = filter(lambda point: coordinates.count(point) >= 2, coordinates)

    #print("HQ location: " + str(doubles[0]))
    return {'final': str(coordinates[-1]), 'HQ': str(doubles[0])}

# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 10
# http://adventofcode.com/2016/day/10

def day10():
    # Part 1: You have instructions for a system of numbered bots that take in numbers, compare them, and deposit them into output bins. Bots don't take any action until they have two numbers to compare. Which bot compares 61 to 17?

    # Example:
    # value 5 goes to bot 2
    # bot 2 gives low to bot 1 and high to bot 0
    # value 3 goes to bot 1
    # bot 1 gives low to output 1 and high to bot 0
    # bot 0 gives low to output 2 and high to output 0
    # value 2 goes to bot 2

    # Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a value-2 chip and a value-5 chip.
    # Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and its higher one (5) to bot 0.
    # Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and gives the value-3 chip to bot 0.
    # Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in output 0.


    instructions = open('day10_input', 'r')
    commands = [x.strip() for x in instructions]
    bots = {}
    outputs = {}

    # Brainstorming
    # For each command, I need to parse whether it's a input value or a bot output. How should I represent bots and output bins? Maybe a list, ('bot 92', 'low', 'high'). Will it work to parse out all the input values and then run all the bot outputs? Or do I have to run through the list (recursively?) checking for bots that have 2 values and activating them?
    # When I'm done, how will I know which bot I'm looking for? How will I know I'm done?

    # Refactor this all into multiple functions and then one main loop that calls them in succession?

    def botlist():
        for c in commands:
            x = c.split()

            # Define each bot as a dictionary with two values, initialized False, and destinations for its high and low values
            if x[0] == 'bot':
                bots[(x[0]+x[1])] = {'v0': False, 'v1': False, 'lowdest': x[5]+x[6], 'highdest': x[10]+x[11]}
            # As you parse commands, also create dictionaries for each output bin
            if x[5] == 'output':
                bots[(x[5]+x[6])] = {'value': False}
            if len(x) > 6 and x[10] == 'output':
                bots[(x[10]+x[11])] = {'value': False}

    # Next, populate each bot with its initial values
    # Can this be merged with the previous function??
    def valrun():
        for c in commands:
            x = c.split()
            if x[0] == 'value':
                bcompare(bots[(x[4]+x[5])], int(x[1]))

    # Given a bot or bin, deposit the number in one of the bot's slots or the bin.
    def bcompare(bot, x):
        if 'value' in bot.keys():
            bot['value'] = x
        elif bot['v0']:
            bot['v1'] = x
        else:
            bot['v0'] = x

    # If a bot has both values, compare & send them to lowdest and highdest and reset them to False
    def botrun():
        for k, b in bots.iteritems():
            if ('v0' in b.keys()) and b['v0'] and b['v1']:
                bcompare(bots[b['lowdest']], min(b['v0'], b['v1']))
                bcompare(bots[b['highdest']], max(b['v0'], b['v1']))
                b['v0'] = False
                b['v1'] = False

    # 500 runs turns out to be sufficient to reach steady state.
    botlist()
    valrun()
    for i in range(500):
        botrun()

    # Part 2: What is the product of the numbers in bins 0, 1, and 2?

    r = bots['output0']['value'] * bots['output1']['value'] * bots['output2']['value']
    print r

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

    import copy
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
        y = [([a,b] if (not a == b) and (a < b) else [a]) for a in x for b in x]
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
            if a[2] == "M" and

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
    import copy

    # store each item as a dictionary? label floors with strings or in variables?
    # F1 = {'TmG': {'element': 'Tm', 'type': 'G'}, }

    state = {
        4: [],
        3: [('Pr','G'), ('Pr','M'), ('Ru','G'), ('Ru','M')],
        2: [('Pu','M'), ('Sr','M')],
        1: [('Tm','G'), ('Tm','M'), ('Pu','G'), ('Sr','G')],
        'E': 1
    }

    # change this to be just lists?
    state = {
        '4': [],
        '3': [('Li','G')],
        '2': [('H','G')],
        '1': [('H','M'), ('Li','M')],
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


def day12():

    # Part 1: You are given a set of assembly instructions, operating on 4 registers initialized to 0. What value does register a hold when the instructions terminate?

    # Part 2: What value does register a hold if register c is initialized to 1?

    # Commands:
    # 'cpy x y' copies x (either an integer or the value of a register) into register y.
    # 'inc x' increases the value of register x by one.
    # 'dec x' decreases the value of register x by one.
    # 'jnz x y' jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.

    instructions = open('day12_input', 'r')
    commands = [x.strip() for x in instructions]

    reg = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
    i = 0

    # Instructions are followed in order from the beginning until no more remain; use i to track progress through the list
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

    print reg


def day13():

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


def day14():

    # Problem: You are looking for 64 one-time pad keys. To find each key, determine the md5 hash of your input salt with an index that starts at 0 and increases each time. A key is valid if the lowercase hexadecimal representation of the md5 result contains 3 characters in a row AND a hash containing the same characters 5 times in a row occurs in the next 1000 hashes.

    import hashlib, pprint

    salt = 'zpqevtbw'
    hashes = {}
    keys = {}
    h = '0123456789abcdef'

    for x in range(500000):
        m = hashlib.md5()
        m.update(salt + str(x))
        hashes[x] = m.hexdigest().lower()

    while len(keys) < 64:
        for i in range(len(hashes) - 1000):
            for j in range(i+1, i+1001):
                for x in h:
                    if x*3 in hashes[i] and x*5 in hashes[j]:
                        keys[i] = [hashes[i], hashes[j], j]
                        break

    pprint.pprint(keys)


def day15():

    # Problem: You have a machine of disks which rotate every second. You want to release a capsule at the top at the right time to pass through to the bottom. Each disk is 1s apart. Given the initial positions and number of positions on each disk, at what time should you release the capsule?

    # Disc #1 has 13 positions; at time=0, it is at position 1.
    # Disc #2 has 19 positions; at time=0, it is at position 10.
    # Disc #3 has 3 positions; at time=0, it is at position 2.
    # Disc #4 has 7 positions; at time=0, it is at position 1.
    # Disc #5 has 5 positions; at time=0, it is at position 3.
    # Disc #6 has 17 positions; at time=0, it is at position 5.
    # Disc #7 has 11 positions; at time=0, it is at position 1.

    # Track global time t. Code each disk's position mod the time. Update each position each reads 0 at the correct time.

    t = 0

    def check(time):
        while True:
            d1 = (1 + time + 1) % 13
            d2 = (10 + time + 2) % 19
            d3 = (2 + time + 3) % 3
            d4 = (1 + time + 4) % 7
            d5 = (3 + time + 5) % 5
            d6 = (5 + time + 6) % 17
            d7 = (0 + time + 7) % 11

            if d1 == d2 == d3 == d4 == d5 == d6 == d7 == 0:
                print time
                break

            if time % 10000 == 0:
                print time, d1, d2, d3, d4, d5, d6, d7

            time += 1

    check(t)


def day16():

    # Problem: you need to generate random data to fill a disk and calculate its checksum. Given an initial seed value, you generate data this way:
        #
        # Call the data you have at this point "a".
        # Make a copy of "a"; call this copy "b".
        # Reverse the order of the characters in "b".
        # In "b", replace all instances of 0 with 1 and all 1s with 0.
        # The resulting data is "a", then a single 0, then "b".

    disk = 35651584
    seed = '11100010111110100'

    binswap = {'0': '1', '1': '0'}

    def datagen(a):
        b = a[::-1]
        b = b.translate(str.maketrans(binswap))
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
        pairs = [a[x] + a[x+1] for x in range(0, len(a), 2)]
        check = ''
        for each in pairs:
            if each[0] == each[1]:
                check += '1'
            else:
                check += '0'
        if len(check) % 2 == 0:
            checksum(check)
        else:
            print(check, len(check))

    checksum(seed)


def day17():

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


def day18():

    # Problem: You face a room with 40 rows of tiles, some of which are safe (.) and some are traps (^). Given the layout of the first row, you can determine the layout of the next row by following the rules below.

    # Rules:
    # For each tile, look at the tile in the prior row and the two adjacent to that tile. Call these tiles the left, center, and right tiles. A new tile is a trap if:
    #   - The left and center tiles are traps, but the right tile is not.
    #   - The center and right tiles are traps, but the left tile is not.
    #   - Only the left tile is a trap.
    #   - Only the right tile is a trap.
    # The wall (end of each row) counts as safe; any tile that is not a trap per these rules is safe.

    # Part 1: How many safe tiles are in this room?
    pass


def day2():

    # Problem: Starting from the 5 of a 13-digit keypad, follow the given directions (Up, Down, Left, Right) to find each digit of a passcode. Skip any direction that leads off the edge of the keypad.

    # Keypad layout
    #       1
    #   2   3   4
    #5  6   7   8   9
    #   A   B   C
    #       D


    keys = "DULUDRDDDRLUDURUUULRRRURDRDULRUDDUDRULUDDUDRLDULRRLRDRUDUUULUUDLRURDUDDDDRDLLLLULRDLDRDLRLULRUURDDUULUDLRURRDDRDDRDDLDRDLLUURDRUULRRURURRDLRLLLUDULULULULUDRLLRUDUURLDRLRLRDRRDRLLLDURRDULDURDDRLURRDURLRRRLDLLLDRUUURLRDLDLLLLRDURRLDLULRLDDLDLURLRRDDRUDDUULRURRUDLRDLDUURDDDDRLRURUDULUDLRRLLLLLRDRURLLDLDULUUDLUDDDRLLDRRUDLLURRUUDDRRLLRRLDDDURLDRDRLURRRRDRRRDDUDULULDURRUUURRRDULUUUDDRULDRLLRDLDURLURRLLRUUUULRDURLLDDRLLDLRLRULUUDRURUDLLURUDDRDURLRDRRRDURLDDRDRLRLLURULUUULUDDDULDLRDDDRDLLRRLDRDULLUUUDLDDLDDDLLLLLLLDUDURURDURDRUURRRDDRDUDLULDURDUDURDDDRULDURURURRLURLURLUURLULDLLRUULURDDRLRDDLRDLRRR, LUURLRUDRRUDLLDLUDDURULURLUUDUUDDRLUULRDUDDUULDUUDRURDDRRDRLULLRDRDLRLLUURRUULRLDRULUDLDUUDDDRDDLRDLULDRLDUULDLRDLLLDLDLRDUULUDURRULLRLDUDRLLLULUUUULUUDUUURRRDULLUURUDRRLDURRUULDRDULDUDRDUUULUUDDRLUDRLDLDRUUURDLDUDRUDUURLLRRLRLLRRLDULDDULUDUUURULDDUDUDRURRDLULRUDDURDLDLLRRRLDRLULLLRUULDUDLUUDURRLLLRLUDURRDDLDRDDDLURDLDRRUDUDLUDULULRUUUDLUURLLRLDDLURULDURDLRRDDDDURLDDLLDDULLLRLDLDULDUUDDRLDUURDDLDLUUDULRRLRLUURURUURLRLURUURLDRUURLLRDDUUUDULUDDDRDRLDRDRRLRLDULLRRUDLURULULRDRURURLULDUDLRURLRDDRULDDLRD, LUDRULUULRRDDDDRRDUURUDDRLDDLDRDURRURULRDLDLDUUDRRDUUDUDLLLRRLDUDDRLDDLRRLRDRLUDLULUDDUUDULDUUULUDLDDURLDURUDLDRUUDRLRRLDLDDULDUUDDLDDLLURDRLRUURDDRUDDUDLDRRLRUDRUULRRRLRULULURDLRRURDRLRULDDDRDUULLURUUUURUDDLRRRRRDURLULDLUULUDRRUDUDRRDDRURDURLRLUDDLDLRRULUDLDDRLDDLDDDLLLLRDLLUULDDLULDLDRDDUDLURUDLDLDDRRUUDDDLRLLLDRRDDDUURDUDURUURRDRLLDUDLDUULLDLDLLUULLRRULDLDRURLDULDRUURDURRURDLRDLLLDRRUDRUUDRURLUDDRURLDURRDLUUDLUUDULLLDDDDRRDLLLDLURULDDRDLUUURRDRRUUDDUL, DUUULDUDDDURLLULDDLLUDURLLLURULULURUURDRURLRULLLLDRDDULRRDRRLLLRDDDUULLRRURRULLDDURRRLRDDLULDULLDUDLURRDLDDLURDLRLLDRURLLRLLRRRDRRRURURUUDDLLDDLDDDLRLURUUUULRDLUDDDURLLDDRLDRRLLUDUUULRLLDRRRLRUUDLDUULRLUDRULLLLDUDLLUUDDRUURLURUDRDDDLRURUDRLULLULUUDLDURDULRRDRLDURUULRDRRRDRDRRLRLRDDUULLRDLDURDDDULURRLULDDURDURDDUDURDLLUUULUDULRDDLDRDRUDLLUURDLRDURURULURULLDRLLRRULDLULULDLULRURLRRLUDLLLRLUDLURLULDULDRLLLDLDDDDRDRLRRLRDULUUDULDDLDURDLLLDDDDLLUURRDURLDLUDDLULRUUUDDRRLDLLLRDLLDRRRDDLULLURDDRRRRLDLRLLLRL, LULLRRDURRLDUUDRRURLURURRRLRDRUULUULURLLURRDRULRDURDDDDUULLLLDUULDLULURDRLDLULULDRLLDLLRLRULURUDRUUDULRULLLUDRULUDRLLUDLDRRDRUUURURLRDURDRLRDDDURLURRDLRUUUDUURULULDLUULRDLRRRDRDRLLLDLRRDRLLDDULDRUDRRLULLRDLDUDDULRDDLULRURULRLLLULDLLLLRDLDRURUDUURURLDRLUULLDUDULUDDDULUDLRUDDUDLULLUULUUURULURRULRDDURDDLURLRRDRDLDULRLRDRRRULRDDDRLLDDDDRRRRDRDLULUURDURULDLRDULDUDLDURUDLUDLUDDDUDURDURDDURLLRUDUURRRUDRRRRULLLLDDDLUULLUULRRRULDLURDLULRULDRLR".split(", ")

    # Consider the keypad as a coordinate grid, and start at key 5
    coordinates = [-2, 0]

    # Two cases to handle movement on the interior and the edges. I'm pretty sure there's a more elegant way to do this.
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
        print coordinates


def day3():

    # Problem: given a list of numbers, separate them into groups of 3 (down columns, not across rows). How many of these groups could be the sides of a triangle (a + b > c)?
    triangles = open('day3_input', 'r')
    count = 0
    i = 0

    # Turn the input string into a list of numbers
    htri = [x.split() for x in triangles]

    # Group those numbers into sets of 3
    i = range(0, len(htri), 3)
    vtri = [y for x in i for y in zip(htri[x], htri[x+1], htri[x+2])]

    # Check each ordering of each group for valid triangle lengths
    for x in vtri:
        t = [int(each) for each in x]
        a, b, c = t

        if (a == max(t) and (b + c > a)) or (b == max(t) and (c + a > b)) or (c == max(t) and (a + b > c)):
            count += 1

    print count


def day4():

    # Part 1: You are given a list of rooms formatted as a name (lowercase letters separated by dashes) followed by a dash, a sector ID, and a checksum in square brackets. A room name is valid if the checksum is the five most common letters in the encrypted name, in order, with ties broken by alphabetization. What is the sum of the sector IDs for all the valid rooms?

    # Examples (make these tests?):
    # aaaaa-bbb-z-y-x-123[abxyz] is valid
    # a-b-c-d-e-f-g-h-987[abcde] is valid
    # not-a-real-room-404[oarel] is valid
    # totally-real-room-200[decoy] is invalid


    import string

    rooms = open('day4_input', 'r')

    idsum = 0
    realnames = []

    # Start with each room name in a list of strings
    r = [y for x in rooms for y in x.split()]

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

    # Part 2: Decrypt each room name by shifting each letter forward by the sector ID. Dashes become spaces. What is the sector ID of the room containing North Pole objects?

        if letters == checksum:
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
                print realname, sectorid


def day5():

    # Problem: You are looking for an 8 character password. To find each character, determine the md5 hash of your input with an index that starts at 0 and increases each time. If the hexadecimal representation of the md5 result begins with 5 zeroes, the 7th digit is added to the password in the position given by the 6th digit. Only the first character found for each position is used, discard the rest.

    import hashlib

    doorid = 'abbhdwsy'
    i = 0
    password = ['_'] * 8

    # Run this loop until the password has changed from symbols to alphanumerics
    while not ''.join(password).isalnum():
        m = hashlib.md5()
        m.update(doorid + str(i))
        if m.hexdigest()[:5] == '00000' and m.hexdigest()[5].isdigit():
            position = int(m.hexdigest()[5])
            if position < 8 and password[position] == '_':
                password[position] = m.hexdigest()[6]
        i += 1

    print ''.join(password)


def day6():

    # Problem: Given a list of strings, find the least common character in each column.

    messages = open('day6_input', 'r')
    final = ''

    hwords = [y for x in messages for y in x.split()]

    # Reformat from rows to columns
    vwords = zip(*hwords)

    for word in vwords:
        word = ''.join(word)
        counts = [(l, word.count(l)) for l in word]
        counts.sort(key=lambda l: l[1])
        final += counts[0][0]

    print final


def day7():

    # Part 1: Strings are valid if they contain a 4 character palindrome (e.g. abba, smms), unless the palindrome is inside square brackets or the characters are all the same (e.g. nnnn). How many of the given strings are valid?

    # Examples (make these tests?):
    # abba[mnop]qrst is valid
    # abcd[bddb]xyyx is invalid
    # aaaa[qwer]tyui is invalid
    # ioxxoj[asdfgh]zxcvbn is valid

    addresses = open('day7_input', 'r')
    count = 0

    ips = [x.strip() for x in addresses]

    # Given a string, test each set of 4 consecutive characters for palindromes
    # Return True if any 4 are valid, otherwise False
    def abba(s):
        tf = [(s[i] == s[i+1]) and (s[i-1] == s[i+2]) and (s[i] != s[i-1]) for i in range(1, len(s)-2)]
        return True in tf

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

    print count

    # Part 2: Strings are valid if they contain a 3 character palindrome (e.g. aba, sms) outside square brackets AND the corresponding inverse (e.g. sms -> msm) inside square brackets.

    # Examples:
    # aba[bab]xyz is valid
    # xyx[xyx]xyx is invalid
    # aaa[rur]uru is valid
    # zazbz[bzb]cdb is valid

    # Given a string, test each set of 3 consecutive characters for palindromes
    # Return a list for further testing
    def xyx(s):
        trigrams = [s[i-1:i+1] for i in range(1, len(s)-1) if (s[i-1] == s[i+1] and s[i] != s[i-1])]
        return trigrams

    # Given two lists of strings, check each item of a for matchng any item in b
    # NOTE: this checks the reverse of x against y; maybe rename this or reverse before passing into the fn? or when generating trigrams?

    def matches(a, b):
        return True in [True for x in a for y in b if x[::-1] == y]

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
                outbs.extend(xyx(z[0]))
                # Ditto, inside square brackets
                inbs.extend(xyx(z[2]))
            #what to do if '[' isn't found (last segment)
            else:
                outbs.extend(xyx(y))

        if matches(outbs, inbs):
            count += 1

    print count


def day8():

    # Part 1: You are given a set of commands to execute on a screen 50 px wide by 6 px tall, which starts entirely off. How many pixels turn on?

    # Commands:

    # 'rect AxB' turns on all of the pixels in a rectangle A px wide by B px tall at the top-left of the screen.

    # 'rotate row y=A by B' shifts all of the pixels in row A (0 is the top row) right by B px. Pixels that would fall off the right end appear at the left end of the row.

    # 'rotate column x=A by B' shifts all of the pixels in column A (0 is the left column) down by B px. Pixels that would fall off the bottom appear at the top of the column.

    # numpy handles arrays well, let's use it here
    import numpy as np

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

    instructions = open('day8_input', 'r')
    ops = [x.strip() for x in instructions]

    for each in ops:
        r = each.split()
        if r[0] == "rect":
            rect(r[1])
        if r[0] == "rotate":
            rotate(r[1], r[2], r[4])

    print np.sum(screen)

    # Part 2: The screen displays letters as capital letters 5 px wide. What code is displayed?

    # read straight off the terminal
    for x in range(0, screen.shape[1], 5):
        print screen[:, x:x+5]


def day9():

    # Part 1: You need to decompress a data file. Compression markers are contained in parentheses. (10x2) means to take the next 10 characters and insert them 2 times, then continue reading forward. Ignore whitespace and do not include the marker itself in the decompressed text to insert. However, parentheses and other special characters may appear in inserted text without denoting a compression marker. What is the length of your decompressed file?

    # Examples:
    # ADVENT -> ADVENT with length 6.
    # A(1x5)BC -> ABBBBBC with length 7.
    # (3x3)XYZ -> XYZXYZXYZ with length 9.
    # A(2x2)BCD(2x2)EFG -> ABCBCDEFEFG with length 11.
    # (6x1)(1x3)A -> (1x3)A with length 6.
    # X(8x2)(3x3)ABCY -> X(3x3)ABC(3x3)ABCY with length 18.

    compressed = open('day9_input', 'r')
    data = [x.strip() for x in compressed]
    decompressed = 0

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
                return expand(repstr*rx + x[2][rlen:], d)
        else:
            x = s.partition('(')
            d += len(x[0])
            return expand('(' + x[2], d)

    # print expand(data[0], decompressed)

    # Part 2: Turns out you need to expand markers within inserted text after all. What is the decompressed length of your file?

    # Examples:
    # (3x3)XYZ -> XYZXYZXYZ
    # X(8x2)(3x3)ABCY -> X(3x3)ABC(3x3)ABCY -> XABCABCABCABCABCABCY
    # (27x12)(20x12)(13x14)(7x10)(1x12)A -> A repeated 241920 times
    # (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445 characters long.

    # Switch from recursion to iteration. Can this be optimized??

    def expand2(s, d):
        i = 0
        while len(s) > 1:
            if s.startswith('('):
                x = s.partition(')')
                marker = x[0].strip('(').split('x')
                rlen = int(marker[0])
                rx = int(marker[1])
                repstr = x[2][0:rlen]
                s = repstr*rx + x[2][rlen:]
            else:
                x = s.partition('(')
                d += len(x[0])
                s = '(' + x[2]
            i += 1
            # Track progress during run
            if i % 100000 == 0:
                print d, len(s)

        return d, i

    print expand2(data[0], decompressed)

def river():
    import copy

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

    print iterstate(state, paths, moves)
