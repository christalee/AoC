# Christalee Bieber, 2018
# cbieber@alum.mit.edu

# Advent of Code 2015
# http://adventofcode.com/2015/

import hashlib, re


def day5_part2(strings=False):
    if not strings:
        input = open('day5.txt', 'r')
        strings = [x.strip() for x in input]

    results = []

    for s in strings:
        nice = False
        if re.search(r'(\w)\w\1', s) and re.search(r'(\w{2}).*\1', s):
            nice = True

        results.append(nice)

    return results.count(True)


def day5_part1(strings=False):
    if not strings:
        input = open('day5.txt', 'r')
        strings = [x.strip() for x in input]

    results = []

    for s in strings:
        nice = False
        if re.search(r'([aeiou].*){3}', s) and re.search(r'(\w)\1', s):
            nice = True
        if re.search(r'(ab|cd|pq|xy)', s):
            nice = False

        results.append(nice)

    return results.count(True)


def day4(key='yzbqklnj'):
    i = 1
    found = False

    while not found:
        m = hashlib.md5()
        m.update(bytes(key + str(i), 'utf-8'))
        if m.hexdigest()[:5] == '00000':
            found = True
        i += 1

    return i - 1


def day3(arrows=False):
    if not arrows:
        arrows = open('day3.txt', 'r').read()

    santa = {'x': 0, 'y': 0}
    robot = {'x': 0, 'y': 0}
    presents = {str(list(santa.values())): 2}

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

def day2(box_list=False):
    if not box_list:
        input = open('day2.txt', 'r')
        box_list = [x.strip() for x in input]

    paper = 0
    ribbon = 0

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


def day1(parens=False):
    if not parens:
        parens = open('day1.txt', 'r').read()

    floor = 0
    basement = []

    for i, p in enumerate(parens):
        if p == '(':
            floor += 1
        if p == ')':
            floor -= 1
        if floor == -1:
            basement.append(i + 1)

    # floor = parens.count('(') - parens.count(')')
    return {'floor': floor, 'basement': basement}
