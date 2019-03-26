# Christalee Bieber, 2019
# cbieber@alum.mit.edu

# Advent of Code 2018
# http://adventofcode.com/2018/

from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def input(filename):
    with open(filename, 'r') as input:
        data = [x.strip() for x in input]

    return data


def day4_part2(records=None):
    if not records:
        records = input('day4.txt')

    records.sort()
    history = pd.DataFrame(columns=['day', 'guard'])
    minutes = pd.DataFrame(np.zeros((1, 60), dtype=int), columns=np.arange(60))

    for r in records:
        s = r.split()
        ts = datetime.strptime(' '.join([s[0], s[1]]).strip(
            '[]'), '%Y-%m-%d %H:%M') + timedelta(days=36500 * 5)
        day = pd.Timestamp(ts).round('D').date()
        if 'Guard' in r:
            result = pd.concat(
                [pd.DataFrame([{'day': day, 'guard': s[3]}]), minutes], axis=1)
            history = pd.concat([history, result], sort=True)
        if 'falls asleep' in r:
            history.loc[history['day'] == day, list(range(ts.minute, 60))] = 1
        if 'wakes up' in r:
            history.loc[history['day'] == day, list(range(ts.minute, 60))] = 0

    history['total'] = history[np.arange(60)].sum(axis=1)

    # by_guards = history[['guard', 'total']].groupby('guard').sum()
    # g = by_guards.idxmax()[0]
    # guard_minutes = history.loc[history['guard'] == g, np.arange(60)].sum()
    # m = guard_minutes.idxmax()
    #
    # print('Part 1\nguard: ' + g + ', minute: ' + str(m))

    by_minutes = history[['guard', *np.arange(60)]].groupby('guard').sum()
    top_minute = by_minutes.max().idxmax()
    top_guard = by_minutes[[top_minute]].idxmax().item()

    return int(top_guard.strip('#')) * top_minute


def day4_part1(records=None):
    if not records:
        records = input('day4.txt')

    records.sort()
    history = pd.DataFrame(columns=['day', 'guard'])
    minutes = pd.DataFrame(np.zeros((1, 60), dtype=int), columns=np.arange(60))

    for r in records:
        s = r.split()
        ts = datetime.strptime(' '.join([s[0], s[1]]).strip(
            '[]'), '%Y-%m-%d %H:%M') + timedelta(days=36500 * 5)
        day = pd.Timestamp(ts).round('D').date()
        if 'Guard' in r:
            result = pd.concat(
                [pd.DataFrame([{'day': day, 'guard': s[3]}]), minutes], axis=1)
            history = pd.concat([history, result], sort=True)
        if 'falls asleep' in r:
            history.loc[history['day'] == day, list(range(ts.minute, 60))] = 1
        if 'wakes up' in r:
            history.loc[history['day'] == day, list(range(ts.minute, 60))] = 0

    history['total'] = history[np.arange(60)].sum(axis=1)

    by_guards = history[['guard', 'total']].groupby('guard').sum()
    g = by_guards.idxmax()[0]
    guard_minutes = history.loc[history['guard'] == g, np.arange(60)].sum()
    m = guard_minutes.idxmax()

    return int(g.strip('#')) * m

    # by_minutes = history[['guard', *np.arange(60)]].groupby('guard').sum()
    # top_minute = by_minutes.max().idxmax()
    # top_guard = by_minutes[[top_minute]].idxmax().item()
    #
    # print('Part 2\nguard: ' + top_guard + ', minute: ' + str(top_minute))


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
