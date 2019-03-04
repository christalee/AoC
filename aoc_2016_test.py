from aoc_2016_code import *

# TODO
# refactor solutions to eliminate repeated chunks
# refactor for elegance, clarity, and efficiency
# finish writing tests for all solutions
# write tests for nested fns? subproblems?


def test_day20():
    # TODO count unblocked IPs at the end of the range
    assert day20(['5-8', '0-2', '4-7']) == {'part1': 3, 'part2': 1}
    assert day20() == {'part1': 32259706, 'part2': 113}


def test_day19():
    assert day19(5) == 3
    # assert day19() == 1808357


def test_day18():
    assert day18(3, ['..^^.']) == 6
    assert day18(10, ['.^^.^.^^^^']) == 38
    assert day18(40) == 1951
    assert day18(400000) == 20002936


def test_day17():
    assert day17('ihgpwlah') == 'DDRRRD'
    assert day17('kglvqrro') == 'DDUDRLRRUDRD'
    assert day17('ulqzkmiv') == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'
    assert day17() == 'RLDRUDRDDR'


def test_day16():
    assert day16(20, '10000') == '01100'
    assert day16(272) == '10100011010101011'
    assert day16(35651584) == '01010001101011001'


def test_day15():
    assert day15() == {'part1': 376777, 'part2': 3903937}


# def test_day14():
#     assert day14('abc') == {'part1': 22728, 'part2': 22551}
#     assert day14() == {'part1': 16106, 'part2': 22423}


def test_day13():
    # Example:
    # puzzle input = 10, walls are #, spaces are .
    # shortest route from (1,1) to (7,4) is 11 steps (marked as O)
    #   0123456789
    # 0 .#.####.##
    # 1 .O#..#...#
    # 2 #OOO.##...
    # 3 ###O#.###.
    # 4 .##OO#OO#.
    # 5 ..##OOO.#.
    # 6 #...##.###

    assert day13((4, 7), 10) == 11
    assert day13() == 92


def test_day12():
    example = ['cpy 41 a', 'inc a', 'inc a', 'dec a', 'jnz a 2', 'dec a']
    assert day12(example)['part1'] == 42
    # assert day12() == {'part1': 318077, 'part2': 9227731}


def test_day10():
    example = ['value 5 goes to bot 2',
               'bot 2 gives low to bot 1 and high to bot 0',
               'value 3 goes to bot 1',
               'bot 1 gives low to output 1 and high to bot 0',
               'bot 0 gives low to output 2 and high to output 0',
               'value 2 goes to bot 2']

    assert day10(example)['part2'] == 30
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
    example = ['eedadn', 'drvtee', 'eandsr', 'raavrd', 'atevrs', 'tsrnev', 'sdttsa', 'rasrtv', 'nssdts', 'ntnada', 'svetve', 'tesnvt', 'vntsnd', 'vrdear', 'dvrsen', 'enarar']

    assert day6(example) == {'part1': 'easter', 'part2': 'advent'}
    assert day6() == {'part1': 'agmwzecr', 'part2': 'owlaxqvq'}


# skip this, it takes forever to run
# def test_day5():
#     assert day5_part1('abc') == '18f47a30'
#     assert day5_part1() == '801b56a7'
#
#     assert day5_part2('abc') == '05ace8e3'
#     assert day5_part2() == '424a0197'


def test_day4():
    example = ['aaaaa-bbb-z-y-x-123[abxyz]', 'a-b-c-d-e-f-g-h-987[abcde]', 'not-a-real-room-404[oarel]', 'totally-real-room-200[decoy]']

    assert day4(example)['part1'] == 1514
    assert day4() == {'part1': 173787, 'part2': 548}


def test_day3():
    assert day3_check([5, 10, 25]) == False
    assert day3_check([25, 10, 25]) == True

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
