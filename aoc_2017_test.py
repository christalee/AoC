from aoc_2017_code import *


def test_day3():
    assert day3_part1(1) == 0
    assert day3_part1(1024) == 31
    assert day3_part1() == 480

    assert day3_part2(500) == 747
    assert day3_part2() == 349975


def test_day2():
    test = [[5, 9, 2, 8],
            [9, 4, 7, 3],
            [3, 8, 6, 5]]
    assert day2(test) == {"part1": 18, 'part2': 9}
    assert day2() == {'part1': 45972, 'part2': 326}


def test_day1():
    assert day1("1122") == {"part1": 3, 'part2': 0}
    assert day1('123425') == {'part1': 0, 'part2': 4}
    assert day1('123123') == {'part1': 0, 'part2': 12}
    assert day1("91212129") == {'part1': 9, 'part2': 6}
    assert day1() == {'part1': 1150, 'part2': 1064}
