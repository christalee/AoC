from aoc_2016_code import *


def test_day3():
    assert day3_part1(['5 10 25']) == 0
    assert day3_part1(['25 10 25']) == 1
    assert day3_part1() == 983

    assert day3_part2() == 1836


def test_day2():
    assert day2_part1(['ULL', 'RRDDD', 'LURDL', 'UUUUD']) == '1985'
    assert day2_part1() == '98575'

    assert day2_part2(['ULL', 'RRDDD', 'LURDL', 'UUUUD']) == '5DB3'
    assert day2_part2() == 'CD8D4'


def test_day1():
    assert day1(['R2, L3'])['final'] == 5
    assert day1(['R2, R2, R2'])['final'] == 2
    assert day1(['R5, L5, R5, R3'])['final'] == 12
    assert day1(['R8, R4, R4, R8'])['HQ'] == 4

    assert day1() == {'final': 291, 'HQ': 159}
