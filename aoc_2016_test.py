from aoc_2016_code import *

# TODO
# refactor solutions to eliminate repeated chunks
# refactor for elegance, clarity, and efficiency
# finish writing tests for all solutions
# write tests for nested fns? subproblems?


def test_day10():
    test = ['value 5 goes to bot 2',
            'bot 2 gives low to bot 1 and high to bot 0',
            'value 3 goes to bot 1',
            'bot 1 gives low to output 1 and high to bot 0',
            'bot 0 gives low to output 2 and high to output 0',
            'value 2 goes to bot 2']

    assert day10(test)['part2'] == 30
    assert day10() == {'part1': 101, 'part2': 37789}


def test_day9():
    assert day9_part1(['ADVENT']) == 6
    assert day9_part1(['A(1x5)BC']) == 7
    assert day9_part1(['(3x3)XYZ']) == 9
    assert day9_part1(['A(2x2)BCD(2x2)EFG']) == 11
    assert day9_part1(['(6x1)(1x3)A']) == 6
    assert day9_part1(['X(8x2)(3x3)ABCY']) == 18
    assert day9_part1() == 150914

    assert day9_part2(['(3x3)XYZ']) == 9
    assert day9_part2(['X(8x2)(3x3)ABCY']) == 20
    assert day9_part2(['(27x12)(20x12)(13x14)(7x10)(1x12)A']) == 241920
    assert day9_part2(['(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN']) == 445
    # assert day9_part2() == 11052855125


def test_day8():
    assert day8(['rect 3x2']) == 6
    assert day8() == 123


def test_day7():
    assert day7_part1(['abba[mnop]qrst']) == 1
    assert day7_part1(['abcd[bddb]xyyx']) == 0
    assert day7_part1(['aaaa[qwer]tyui']) == 0
    assert day7_part1(['ioxxoj[asdfgh]zxcvbn']) == 1
    assert day7_part1() == 118

    assert day7_part2(['aba[bab]xyz']) == 1
    assert day7_part2(['xyx[xyx]xyx']) == 0
    assert day7_part2(['aaa[rur]uru']) == 1
    assert day7_part2(['zazbz[bzb]cdb']) == 1
    assert day7_part2() == 260


def test_day6():
    test = ['eedadn', 'drvtee', 'eandsr', 'raavrd', 'atevrs', 'tsrnev', 'sdttsa', 'rasrtv', 'nssdts', 'ntnada', 'svetve', 'tesnvt', 'vntsnd', 'vrdear', 'dvrsen', 'enarar']

    assert day6(test) == {'part1': 'easter', 'part2': 'advent'}
    assert day6() == {'part1': 'agmwzecr', 'part2': 'owlaxqvq'}


# skip this, it takes forever to run
# def test_day5():
#     assert day5_part1('abc') == '18f47a30'
#     assert day5_part1() == '801b56a7'
#
#     assert day5_part2('abc') == '05ace8e3'
#     assert day5_part2() == '424a0197'


def test_day4():
    assert day4(['aaaaa-bbb-z-y-x-123[abxyz]'])['part1'] == 123
    assert day4(['a-b-c-d-e-f-g-h-987[abcde]'])['part1'] == 987
    assert day4(['not-a-real-room-404[oarel]'])['part1'] == 404
    assert day4(['totally-real-room-200[decoy]'])['part1'] == 0

    assert day4() == {'part1': 173787, 'part2': 548}


def test_day3():
    assert day3(['5 10 25', '25 10 25', '25 10 25']) == {'part1': 2, 'part2': 3}
    assert day3() == {'part1': 983, 'part2': 1836}


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
