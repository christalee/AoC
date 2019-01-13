# Christalee Bieber, 2019
# cbieber@alum.mit.edu

# Advent of Code 2018
# http://adventofcode.com/2018/

from datetime import datetime, timedelta

import pandas as pd


def input(filename):
    with open(filename, 'r') as input:
        data = [x.strip() for x in input]

    return data


def day4(records=None):
    if not records:
        records = input('day4.txt')

    records.sort()
    history = {}

    for r in records:
        s = r.split()
        ts = datetime.strptime(' '.join([s[0], s[1]]).strip(
            '[]'), '%Y-%m-%d %H:%M') + timedelta(days=36500 * 5)
        day = pd.Timestamp(ts).round('D').date()
        if 'Guard' in r:
            history[day] = {'guard': s[3]}
            # also create an hour's worth of np.zero
            # use a pd.DataFrame instead of a dictionary
        if day in history:
            history[day][ts.minute] = ' '.join([s[2], s[3]])


def day1_part2(frequencies=None):
    if not frequencies:
        with open('day1.txt', 'r') as input:
            frequencies = [int(x.strip()) for x in input]

    freq = 0
    history = {0: True}
    i = 0

    while True:
        freq += frequencies[i]
        if freq in history:
            return freq
        if i == len(frequencies) - 1:
            i = 0
        else:
            history[freq] = True
            i += 1


def day1_part1(frequencies=None):
    if not frequencies:
        with open('day1.txt', 'r') as input:
            frequencies = [int(x.strip()) for x in input]

    return sum(frequencies)
