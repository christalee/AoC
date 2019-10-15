# Christalee Bieber, 2019
# cbieber@alum.mit.edu

# Advent of Code 2018
# http://adventofcode.com/2018/

import string
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def input(filename):
    with open('input_2018/' + filename, 'r') as input:
        data = [x.strip() for x in input]

    return data


def day4(records=None):

    # Problem: You have a timestamped log showing when each guard came on duty, when they fall asleep, and when they wake up. You want to use this information to sneak past the guard tonight, after midnight.

    # Part 1: In the past month, which guard spent the most minutes asleep between midnight and 1am, and during which minute was he most often asleep? Give the guard ID x the minute chosen.

    # Part 2: Which guard is most frequently asleep on the same minute? Give the guard ID x the minute chosen.

    if not records:
        records = input('day4.txt')

    # Solution: Start by sorting and parsing the input into a DataFrame
    records.sort()
    history = pd.DataFrame()
    minutes = pd.DataFrame(np.zeros((1, 60), dtype=np.uint8), columns=np.arange(60))

    for r in records:
        s = r.split()

        # Parse the timestamps, and round to the next day as needed
        ts = datetime.strptime(' '.join([s[0], s[1]]).strip(
            '[]'), '%Y-%m-%d %H:%M') + timedelta(days=36500 * 5)
        day = pd.Timestamp(ts).round('D').date()

        # Create a row for each day, and indicate which minutes the guard is asleep
        if 'Guard' in r:
            result = pd.concat(
                [pd.DataFrame([{'day': day, 'guard': s[3]}]), minutes], axis=1)
            history = pd.concat([history, result], sort=True)
        if 'falls asleep' in r:
            history.loc[history['day'] == day, list(range(ts.minute, 60))] = np.uint8(1)
        if 'wakes up' in r:
            history.loc[history['day'] == day, list(range(ts.minute, 60))] = np.uint8(0)

    # Add a column with the total minutes asleep on each day
    history['total'] = history[np.arange(60)].sum(axis=1).astype('uint8')

    # Find the guard who sleeps the most minutes overall
    by_guards = history[['guard', 'total']].groupby('guard').sum()
    g = by_guards.idxmax()[0]

    # Find the minute in which that guard sleeps most often
    guard_minutes = history.loc[history['guard'] == g, np.arange(60)].sum()
    m = guard_minutes.idxmax()

    by_minutes = history[['guard', *np.arange(60)]].groupby('guard').sum()
    top_minute = by_minutes.max().idxmax()
    top_guard = by_minutes[[top_minute]].idxmax().item()

    return {'part1': int(g.strip('#')) * m, 'part2': int(top_guard.strip('#')) * top_minute}


def day2(boxes=None):

    # Part 1: Given a list of box names, count how many contain exactly 2 or exactly 3 of a single letter. What is the product of these counts?

    # Part 2: The two boxes you're looking for have the same name, with a single character difference. What letters do these boxes have in common?

    if not boxes:
        boxes = input('day2.txt')

    triples = []
    doubles = []
    common = ''

    for b in boxes:

        # Solution: collect names with exactly 2 or 3 of a character
        for l in string.ascii_lowercase:
            if b.count(l) == 3:
                triples.append(b)
            if b.count(l) == 2:
                doubles.append(b)

        # compare each box name against the others, counting up how many charactes differ
        for c in boxes:
            m = 0
            for i, j in enumerate(b):
                if j != c[i]:
                    m += 1
                    x = b.replace(j, '')

            # if they only differ by 1, that's your answer!
            if m == 1:
                common = x

    return {'part1': len(set(triples)) * len(set(doubles)), 'part2': common}


def day1(frequencies=None):

    # Part 1: Given a list of changes in transmitter frequency, what is the final frequency?

    # Part 2: What is the first frequency value that appears twice? Loop through the list until you find it.

    if not frequencies:
        frequencies = list(map(int, input('day1.txt')))

    freq = 0
    history = {freq}
    i = 0

    # TODO rewrite using itertools.cycle()
    while True:
        freq += frequencies[i]
        if freq in history:
            return {'part1': sum(frequencies), 'part2': freq}
        if i == len(frequencies) - 1:
            i = 0
        else:
            history.add(freq)
            i += 1
