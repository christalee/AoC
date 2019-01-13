from aoc_2018_code import *


def test_day7():
    pass


def test_day6():
    pass


def test_day5():
    pass


def test_day4():
    example = [
        '[1518-11-01 00:00] Guard #10 begins shift',
        '[1518-11-01 00:05] falls asleep',
        '[1518-11-01 00:25] wakes up',
        '[1518-11-01 00:30] falls asleep',
        '[1518-11-01 00:55] wakes up',
        '[1518-11-01 23:58] Guard #99 begins shift',
        '[1518-11-02 00:40] falls asleep',
        '[1518-11-02 00:50] wakes up',
        '[1518-11-03 00:05] Guard #10 begins shift',
        '[1518-11-03 00:24] falls asleep',
        '[1518-11-03 00:29] wakes up'
        '[1518-11-04 00:02] Guard #99 begins shift',
        '[1518-11-04 00:36] falls asleep',
        '[1518-11-04 00:46] wakes up'
        '[1518-11-05 00:03] Guard #99 begins shift'
        '[1518-11-05 00:45] falls asleep'
        '[1518-11-05 00:55] wakes up]'
    ]

    # assert day4(example) == 240


def test_day3():
    pass


def test_day2():
    pass


def test_day1():
    assert day1_part1([+1, -2, +3, +1]) == 3
    assert day1_part1([+1, +1, +1]) == 3
    assert day1_part1([+1, +1, -2]) == 0
    assert day1_part1([-1, -2, -3]) == -6

    assert day1_part2([+1, -2, +3, +1]) == 2
    assert day1_part2([+1, -1]) == 0
    assert day1_part2([+3, +3, +4, -2, -4]) == 10
    assert day1_part2([-6, +3, +8, +5, -6]) == 5
    assert day1_part2([+7, +7, -2, -7, -4]) == 14
