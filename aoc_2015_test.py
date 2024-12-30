from aoc_2015_code import *

# TODO
# - write tests for all solutions
# - review problem statements for additional test cases
# - write tests for nested fns, subproblems
# - check runtimes for all tests and comment out the slowest


def test_day25():
    assert day25([10, 10], (0, 0)) == 20151125
    assert day25([10, 10], (1, 0)) == 31916031
    assert day25([10, 10], (0, 1)) == 18749137
    assert day25([10, 10], (2, 0)) == 16080970

    # assert day25([6500, 6500]) == 9132360

def test_day24():
    assert day24(3) == 11846773891
    assert day24(4) == 80393059

def test_day23():
    assert day23() == {'part1': 184, "part2": 231}


def test_day21():
    assert day21() == {"part1": 121, "part2": 201}


# def test_day20():
#     assert day20() == {"part1": 776160, "part2": 786240}


def test_day19():
    test = ["e => H",
            "e => O",
            "H => HO",
            "H => OH",
            "O => HH"]

    assert day19_part1(test, "HOH") == 4
    assert day19_part1(test, "HOHOHO") == 7
    assert day19_part1() == 576


def test_day18():
    test = [".#.#.#",
            "...##.",
            "#....#",
            "..#...",
            "#.#..#",
            "####.."]
    assert day18_part1(5, test) == 4
    # assert day18_part1(100) == 1061

    assert day18_part2(5, test) == 17
    # assert day18_part2(100) == 1006


def test_day17():
    assert day17(25, [20, 15, 10, 5, 5]) == {"part1": 4, "part2": 3}
    assert day17(150) == {"part1": 654, "part2": 57}


def test_day16():
    assert day16() == {"part1": 103, "part2": 405}


def test_day15():
    assert day15() == {"part1": 18965440, "part2": 15862900}


def test_day14():
    test = ["Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
            "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."]

    assert day14_part1(1000, test) == 1120
    assert day14_part1(2503) == 2660

    assert day14_part2(1000, test) == 689
    assert day14_part2(2503) == 1256


def test_day13():
    test = ["Alice would gain 54 happiness units by sitting next to Bob.",
            "Alice would lose 79 happiness units by sitting next to Carol.",
            "Alice would lose 2 happiness units by sitting next to David.",
            "Bob would gain 83 happiness units by sitting next to Alice.",
            "Bob would lose 7 happiness units by sitting next to Carol.",
            "Bob would lose 63 happiness units by sitting next to David.",
            "Carol would lose 62 happiness units by sitting next to Alice.",
            "Carol would gain 60 happiness units by sitting next to Bob.",
            "Carol would gain 55 happiness units by sitting next to David.",
            "David would gain 46 happiness units by sitting next to Alice.",
            "David would lose 7 happiness units by sitting next to Bob.",
            "David would gain 41 happiness units by sitting next to Carol."]

    assert day13_part1(test) == 330
    # assert day13_part1() == 664

    assert day13_part2(test) == 286
    # assert day13_part2() == 640


def test_day12():
    assert day12(['[1,2,3]']) == {"part1": 6, "part2": 6}
    assert day12(['[1,{"c":"red","b":2},3]']) == {"part1": 6, "part2": 4}
    assert day12(['[1,"red",5]']) == {"part1": 6, "part2": 6}
    assert day12(['[-1,{"a":1}]']) == {"part1": 0, "part2": 0}

    assert day12() == {"part1": 156366, "part2": 96852}


# def test_day11():
#     assert day11("abcdefgh") == "abcdffaa"
#     assert day11("ghijklmn") == "ghjaabcc"
    # assert day11("hepxcrrq") == "hepxxyzz"
    # assert day11(day11_alpha_inc(day11("hepxcrrq"))) == "heqaabcc"


def test_day10():
    assert day10(1, '1') == '11'
    assert day10(1, '11') == '21'
    assert day10(1, '21') == '1211'
    assert day10(1, '1211') == '111221'
    assert day10(2, '1') == '21'
    assert day10(5, '1') == '312211'

    assert len(day10(40,)) == 360154


def test_day9():
    test = ['London to Dublin = 464',
            'London to Belfast = 518',
            'Dublin to Belfast = 141']

    assert day9(test) == (605, 982)
    assert day9() == (251, 898)


def test_day8():
    with open('input_2015/day8_test.txt', 'r') as input:
        test = input.read().split()

    assert day8(test) == {'part1': 12, 'part2': 19}
    assert day8() == {'part1': 1371, 'part2': 2117}


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

    assert day7()['a'] == 14134


def test_day6():
    assert day6(['turn on 0,0 through 999,999']) == {"part1": 1000000, "part2": 1000000}
    assert day6(['toggle 0,0 through 999,0']) == {"part1": 1000, "part2": 2000}
    # assert day6_part1(['turn off 499,499 through 500,500']) == 0
    # assert day6_part1(['turn on 499,499 through 500,500']) == 4
    # assert day6_part1(['turn on 0,499 through 999,500',
    #                    'toggle 499,499 through 500,500']) == 1996
    assert day6() == {"part1": 377891, "part2": 14110788}

    # assert day6_part2(['turn on 0,0 through 0,0']) == 1


def test_day5():
    assert day5(['ugknbfddgicrmopn']) == {"part1": 1, "part2": 0}
    assert day5(['aaa']) == {"part1": 1, "part2": 0}
    assert day5(['qjhvhtzxzqqjkmpb']) == {"part1": 0, "part2": 1}
    assert day5(['xxyxx']) == {"part1": 0, "part2": 1}

    assert day5() == {"part1": 255, "part2": 55}


def test_day4():
    assert day4('abcdef') == 609043
    assert day4('pqrstuv') == 1048970

    assert day4() == 282749


def test_day3():
    assert day3_part1('>') == 2
    assert day3_part1('^>v<') == 4
    assert day3_part1('^v^v^v^v^v') == 2
    assert day3_part1() == 2081

    assert day3_part2('^v') == 3
    assert day3_part2('^>v<') == 3
    assert day3_part2('^v^v^v^v^v') == 11
    assert day3_part2() == 2341


def test_day2():
    assert day2(['2x3x4']) == {'paper': 58, 'ribbon': 34}
    assert day2(['1x1x10']) == {'paper': 43, 'ribbon': 14}

    assert day2() == {'paper': 1586300, 'ribbon': 3737498}


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

    assert day1(')')['basement'] == 1
    assert day1('()())')['basement'] == 5

    assert day1() == {'floor': 138, 'basement': 1771}
