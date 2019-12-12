from aoc_2018_code import *

# def test_day7():
#     pass
#
#
# def test_day6():
#     pass
#
#


def test_day5():
    example = "dabAcCaCBAcCcaDA"

    assert day5(example) == {'part1': 10, 'part2': 4}
    # assert day5() == {'part1': 9462, 'part2': 4952}


def test_day4():
    # timeit 20 s
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
        '[1518-11-03 00:29] wakes up',
        '[1518-11-04 00:02] Guard #99 begins shift',
        '[1518-11-04 00:36] falls asleep',
        '[1518-11-04 00:46] wakes up',
        '[1518-11-05 00:03] Guard #99 begins shift',
        '[1518-11-05 00:45] falls asleep',
        '[1518-11-05 00:55] wakes up'
    ]

    assert day4(example) == {'part1': 240, 'part2': 4455}
    # assert day4() == {'part1': 39698, 'part2': 14920}


def test_day3():
    example = ["#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2"]

    assert day3(example) == {'part1': 4, "part2": 3}
    assert day3() == {'part1': 115348, "part2": 188}


def test_day2():
    example1 = ["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"]
    example2 = ["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"]

    assert day2(example1) == {'part1': 12, 'part2': 'abcd'}
    assert day2(example2) == {'part1': 0, 'part2': 'fgij'}
    assert day2() == {'part1': 6723, 'part2': 'prtkqyluiusocwvaezjmhmfgx'}


def test_day1():
    # Note: these test cases are only valid for part 1; they never return for part 2
    # assert day1([+1, +1, +1])['part1'] == 3
    # assert day1([-1, -2, -3])['part1'] == -6

    assert day1([+1, +1, -2]) == {'part1': 0, 'part2': 0}
    assert day1([+1, -1]) == {'part1': 0, 'part2': 0}
    assert day1([+3, +3, +4, -2, -4]) == {'part1': 4, 'part2': 10}
    assert day1([-6, +3, +8, +5, -6]) == {'part1': 4, 'part2': 5}
    assert day1([+7, +7, -2, -7, -4]) == {'part1': 1, 'part2': 14}
    assert day1([+1, -2, +3, +1]) == {'part1': 3, 'part2': 2}

    assert day1() == {'part1': 585, 'part2': 83173}
