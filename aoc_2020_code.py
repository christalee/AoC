# Christalee Bieber, 2020
# cbieber@alum.mit.edu

# Advent of Code 2020
# http://adventofcode.com/2020/

import string

import numpy as np


def input(filename: str):
    with open('input_2020/' + filename, 'r') as input:
        data = [x.strip() for x in input]

    return data


def day5(passes=None):
    if not passes:
        passes = input("day5.txt")

    def search(char, rng):
        if char == "F" or char == "L":
            return list(range(min(rng), min(rng) + int(len(rng) / 2)))
        else:
            return list(range(max(rng) - int(len(rng) / 2) + 1, max(rng) + 1))

    def seat_find(bp):
        row = list(range(128))
        for char in bp[:-3]:
            row = search(char, row)

        seat = list(range(8))
        for char in bp[-3:]:
            seat = search(char, seat)

        return row[0] * 8 + seat[0]

    seat_ids = [seat_find(p) for p in passes]

    for i, v in enumerate(sorted(seat_ids)):
        if v != i + min(seat_ids):
            s = v - 1
            break
    return {"part1": max(seat_ids), "part2": s}


def day4(passports=None):
    if not passports:
        with open("day4.txt", 'r') as input:
            passports = input.read().strip()

    parsed = []
    for x in passports.split("\n\n"):
        y = x.replace("\n", " ").split(" ")
        ids = {}
        for field in y:
            k, v = field.split(":")
            ids[k] = v
        parsed.append(ids)

    p1 = 0
    p2 = 0
    fields = sorted(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    for p in parsed:
        if "cid" in p:
            del p["cid"]
        if sorted(p.keys()) == fields:
            p1 += 1

        valid = 0
        if "byr" in p and int(p["byr"]) >= 1920 and int(p["byr"]) <= 2002:
            valid += 1
        if "iyr" in p and int(p["iyr"]) >= 2010 and int(p["iyr"]) <= 2020:
            valid += 1
        if "eyr" in p and int(p["eyr"]) >= 2020 and int(p["eyr"]) <= 2030:
            valid += 1
        if "hgt" in p:
            if "cm" in p['hgt'] and int(p['hgt'][:-2]) >= 150 and int(p['hgt'][:-2]) <= 193:
                valid += 1
            if "in" in p['hgt'] and int(p['hgt'][:-2]) >= 59 and int(p['hgt'][:-2]) <= 76:
                valid += 1
        if "hcl" in p and p["hcl"].startswith("#") and len(p["hcl"]) == 7:
            v = True
            for char in p["hcl"][1:]:
                if char not in string.hexdigits:
                    v = False
            if v:
                valid += 1
        if "ecl" in p and p["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            valid += 1
        if "pid" in p and len(p["pid"]) == 9 and p["pid"].isdecimal():
            valid += 1
        if valid == 7:
            p2 += 1

    return {"part1": p1, "part2": p2}


def day3(trees=None):
    if not trees:
        trees = input('day3.txt')

    t = np.array(list(map(list, trees)))

    def track(angle):
        p = (0, 0)
        path = []

        while p[0] < (t.shape[0] - angle[0]):
            p = ((p[0] + angle[0]), (p[1] + angle[1]) % t.shape[1])
            path.append(t[p])

        return path.count("#")

    angles = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    prod = 1

    for a in angles:
        prod *= track(a)

    return {"part1": track((1, 3)), "part2": prod}


def day2(passwords=None):
    if not passwords:
        passwords = input("day2.txt")

    p1 = 0
    p2 = 0

    for line in passwords:
        [policy, pw] = line.split(": ")
        [rnge, char] = policy.split(" ")
        [low, high] = list(map(int, rnge.split("-")))

        c = pw.count(char)
        if c >= low and c <= high:
            p1 += 1

        v = False
        if pw[low - 1] == char or pw[high - 1] == char:
            v = True
        if pw[low - 1] == char and pw[high - 1] == char:
            v = False
        if v:
            p2 += 1

    return {'part1': p1, "part2": p2}


def day1(report=None):
    if not report:
        report = list(map(int, input('day1.txt')))

    p1 = 0
    p2 = 0

    for a in report:
        for b in report:
            if a + b == 2020:
                p1 = a * b
            for c in report:
                if a + b + c == 2020:
                    p2 = a * b * c

    return {"part1": p1, "part2": p2}
