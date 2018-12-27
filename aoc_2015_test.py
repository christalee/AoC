from aoc_2015_code import *


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
    assert day2(['2x3x4'])['paper'] == 58
    assert day2(['1x1x10'])['paper'] == 43

    assert day2(['2x3x4'])['ribbon'] == 34
    assert day2(['1x1x10'])['ribbon'] == 14


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
