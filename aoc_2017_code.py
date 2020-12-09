# Christalee Bieber, 2020
# cbieber@alum.mit.edu

# Advent of Code 2017
# http://adventofcode.com/2017/

import decimal

import numpy as np


def input(filename):
    with open('input_2017/' + filename, 'r') as input:
        data = [x.strip() for x in input]

    return data


def day3_part2(n=None):
    if not n:
        n = 347991

    s = np.full((100, 100), ".", dtype="U16")
    pos = (50, 50)
    s[pos] = 1
    count = 1
    d = "R"
    directions = ["R", "U", "L", "D", "R"]

    def move(p, d):
        if d == "R":
            new = (p[0], p[1] + 1)
        if d == "U":
            new = (p[0] - 1, p[1])
        if d == "L":
            new = (p[0], p[1] - 1)
        if d == "D":
            new = (p[0] + 1, p[1])

        return new

    def neighbors(point, maze):
        n = []
        for x in [point[0] - 1, point[0], point[0] + 1]:
            for y in [point[1] - 1, point[1], point[1] + 1]:
                if x >= 0 and x < maze.shape[0] and y >= 0 and y < maze.shape[1]:
                    n.append(maze[(x, y)])
                else:
                    n.append('.')
        n.remove(maze[point])

        return n

    while count < n:
        pos = move(pos, d)
        next_d = directions[directions.index(d) + 1]
        step = move(pos, next_d)
        if s[step] == ".":
            d = next_d

    #     print(pos, d, step)
        ns = neighbors(pos, s)
        while "." in ns:
            ns.remove(".")
        count = sum(list(map(int, ns)))
        s[pos] = count

    return count


def day3_part1(n=None):
    if not n:
        n = 347991

    with decimal.localcontext() as ctx:
        ctx.rounding = decimal.ROUND_HALF_UP

        l = 0
        s = 1
        while s <= n:
            l += 1
            s += l * 2
        if s - n >= l:
            center = s - l - decimal.Decimal(l / 2).to_integral_value()
            side = 2 * l - 1
        else:
            center = s - decimal.Decimal(l / 2).to_integral_value()
            side = 2 * l

        rounds = (side - 1) / 4
        r = decimal.Decimal(rounds).to_integral_value(rounding=decimal.ROUND_CEILING)
        d = abs(n - center) + r

    return int(d)


def day2(sheet=None):
    if not sheet:
        s = input("day2.txt")
        sheet = []
        for row in s:
            sheet.append(list(map(int, row.split('\t'))))

    p1 = 0
    p2 = 0

    for row in sheet:
        p1 += max(row) - min(row)
        for a in row:
            for b in row:
                if a % b == 0 and int(a / b) != 1:
                    p2 += int(a / b)

    return {'part1': p1, 'part2': p2}


def day1(captcha=None):
    if not captcha:
        captcha = input("day1.txt")[0]

    p1 = 0
    p2 = 0
    x = int(len(captcha) / 2)

    for i, d in enumerate(captcha):
        if d == captcha[i - 1]:
            p1 += int(d)
        if d == captcha[i - x]:
            p2 += int(d)

    return {'part1': p1, 'part2': p2}
