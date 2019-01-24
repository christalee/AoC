from aoc_2015_code import *


def test_day10():
    assert day10(1, '1') == '11'
    assert day10(1, '11') == '21'
    assert day10(1, '21') == '1211'
    assert day10(1, '1211') == '111221'
    assert day10(2, '1') == '21'
    assert day10(5, '1') == '312211'


def test_day9():
    test = ['London to Dublin = 464',
            'London to Belfast = 518',
            'Dublin to Belfast = 141']
    assert day9(test) == (605, 982)


def test_day8():
    with open('day8_test.txt', 'r') as input:
        test = input.read().split()
    assert day8_part1(test) == 12
    assert day8_part2(test) == 19


def test_day7():
    assert day7(['123 -> x']) == {'x': 123}
    assert day7(['123 -> x', '456 -> y']) == {'x': 123, 'y': 456}
    assert day7(['123 -> x', '456 -> y', 'x AND y -> d']
                ) == {'x': 123, 'y': 456, 'd': 72}
    assert day7(['123 -> x', '456 -> y', 'x AND y -> d', 'x OR y -> e']
                ) == {'x': 123, 'y': 456, 'd': 72, 'e': 507}
    assert day7(['123 -> x', '456 -> y', 'x AND y -> d', 'x OR y -> e',
                 'x LSHIFT 2 -> f']) == {'x': 123, 'y': 456, 'd': 72, 'e': 507, 'f': 492}
    assert day7(['123 -> x', '456 -> y', 'x AND y -> d', 'x OR y -> e', 'x LSHIFT 2 -> f',
                 'y RSHIFT 2 -> g']) == {'x': 123, 'y': 456, 'd': 72, 'e': 507, 'f': 492, 'g': 114}
    assert day7(['123 -> x', '456 -> y', 'x AND y -> d', 'x OR y -> e', 'x LSHIFT 2 -> f', 'y RSHIFT 2 -> g',
                 'NOT x -> h']) == {'x': 123, 'y': 456, 'd': 72, 'e': 507, 'f': 492, 'g': 114, 'h': 65412}
    assert day7(['123 -> x', '456 -> y', 'x AND y -> d', 'x OR y -> e', 'x LSHIFT 2 -> f', 'y RSHIFT 2 -> g',
                 'NOT x -> h', 'NOT y -> i']) == {'x': 123, 'y': 456, 'd': 72, 'e': 507, 'f': 492, 'g': 114, 'h': 65412, 'i': 65079}


def test_day6():
    assert day6_part1(['turn on 0,0 through 999,999']) == 1000000
    assert day6_part1(['toggle 0,0 through 999,0']) == 1000
    assert day6_part1(['turn off 499,499 through 500,500']) == 0
    assert day6_part1(['turn on 499,499 through 500,500']) == 4
    assert day6_part1(['turn on 0,499 through 999,500',
                       'toggle 499,499 through 500,500']) == 1996

    assert day6_part2(['turn on 0,0 through 0,0']) == 1
    assert day6_part2(['toggle 0,0 through 999,999']) == 2000000


def test_day5():
    assert day5_part1(['ugknbfddgicrmopn']) == 1
    assert day5_part1(['aaa']) == 1
    assert day5_part1(['jchzalrnumimnmhp']) == 0
    assert day5_part1(['haegwjzuvuyypxyu']) == 0
    assert day5_part1(['dvszwmarrgswjxmb']) == 0

    assert day5_part2(['qjhvhtzxzqqjkmpb']) == 1
    assert day5_part2(['xxyxx']) == 1
    assert day5_part2(['uurcxstgmygtbstg']) == 0
    assert day5_part2(['ieodomkazucvgmuy']) == 0


def test_day4():
    assert day4('abcdef') == 609043
    assert day4('pqrstuv') == 1048970


def test_day3():
    assert day3('^v') == 3
    assert day3('^>v<') == 3
    assert day3('^v^v^v^v^v') == 11


def test_day2():
    assert day2(['2x3x4']) == {'paper': 58, 'ribbon': 34}
    assert day2(['1x1x10']) == {'paper': 43, 'ribbon': 14}


def test_day1():
    assert day1('(())')['floor'] == 0
    assert day1('()()')['floor'] == 0
    assert day1('(((')['floor'] == 3
    assert day1('(()(()(')['floor'] == 3
    assert day1('))(((((')['floor'] == 3
    assert day1('())')['floor'] == -1
    assert day1('))(')['floor'] == -1
    assert day1(')))')['floor'] == -3
    assert day1(')())())')['floor'] == -3

    assert day1(')')['basement'][0] == 1
    assert day1('()())')['basement'][0] == 5
