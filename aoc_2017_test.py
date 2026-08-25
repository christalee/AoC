from aoc_2017_code import *

def test_day25():
    test = [
        "Begin in state A.",
        "Perform a diagnostic checksum after 6 steps.",
        "",
        "In state A:",
        "If the current value is 0:",
            "- Write the value 1.",
            "- Move one slot to the right.",
            "- Continue with state B.",
        "If the current value is 1:",
            "- Write the value 0.",
            "- Move one slot to the left.",
            "- Continue with state B.",
        "",
        "In state B:",
        "If the current value is 0:",
            "- Write the value 1.",
            "- Move one slot to the left.",
            "- Continue with state A.",
        "If the current value is 1:",
            "- Write the value 1.",
            "- Move one slot to the right.",
            "- Continue with state A."
            ]
    assert day25(test) == 3
    assert day25() == 3362


def test_day24():
    test = [
        '0/2',
        '2/2',
        '2/3',
        '3/4',
        '3/5',
        '0/1',
        '10/1',
        '9/10'
        ]
    assert day24(test) == {'part1': 31, 'part2': 19}
    assert day24() == {'part1': 1859, 'part2': 1799}


# Property-based testing for the loop functions in Jupyter Notebook
# Could be added to this test suite with a little tweaking
# %%ipytest

# @given(st.integers(-10, 10), st.integers(-10, 10), st.integers(-10, 10), st.integers(-10, 10), st.integers(-10, 10))
# def test_loop_11_19(b, d, e, f, g):
#     assume(d != 0)
#     assume(b > e)
#     assume(g != 0)
#     assert loop_11_19_a(b, d, e, f, g) == loop_11_19_b(b, d, e, f, g)

# @given(st.integers(0, 10), st.integers(1, 11), st.integers(0, 10), st.integers(-10, 10), st.integers(-10, 10))
# def test_loop_10_23(b, d, e, f, g):
#     assume(b > d)
#     assume(g != 0)
#     assert loop_10_23_a(b, d, e, f, g) == loop_10_23_b(b, d, e, f, g)

def test_day23():
    assert day23_part1() == 4225
    assert day23_compiled() == 905


def test_day22():
    test = [
        '..#',
        '#..',
        '...'
        ]
    assert day22_part1(test) == 5587
    assert day22_part1() == 5352

    assert day22_part2(test) == 2511944
    assert day22_part2() == 2511475


def test_day21():
    assert day21() == {'part1': 179, 'part2': 2766750}


def test_day20():
    test1 = [
        'p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>',
        'p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>'
    ]
    assert day20_part1(test1) == 0
    assert day20_part1() == 119

    test2 = [
        'p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>',
        'p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>',
        'p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>',
        'p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>'
    ]
    assert day20_part2(test2) == 1
    assert day20_part2() == 471


def test_day19():
    test = [
        "     |          ",
        "     |  +--+    ",
        "     A  |  C    ",
        " F---|----E|--+ ",
        "     |  |  |  D ",
        "     +B-+  +--+ ",
    ]
    assert day19(test) == {"part1": "ABCDEF", "part2": 38}
    assert day19() == {"part1": "QPRYCIOLU", "part2": 16162}


def test_day18():
    test = [
        "set a 1",
        "add a 2",
        "mul a a",
        "mod a 5",
        "snd a",
        "set a 0",
        "rcv a",
        "jgz a -1",
        "set a 1",
        "jgz a -2",
    ]
    assert day18_part1(test) == 4
    assert day18_part1() == 2951

    assert day18_part2() == 7366


def test_day17():
    # part 1
    assert day17(3, 2017, 2017) == 638
    assert day17(None, 2017, 2017) == 1971

    # part 2
    # assert day17() == 17202899


def test_day16():
    assert day16() == {'part1': 'doeaimlbnpjchfkg', 'part2': 'agndefjhibklmocp'}


def test_day15():
    pass
    # test = {'valueA': 65, 'valueB': 8921}
    # assert day15_part1(**test) == 588
    # assert day15_part1() == 567

    # assert day15_part2(**test) == 309
    # assert day15_part2() == 323


def test_day14():
    assert day14("flqrgnkx") == {"part1": 8108, "part2": 1242}
    assert day14() == {"part1": 8316, "part2": 1074}


def test_day13():
    test = ["0: 3", "1: 2", "4: 4", "6: 4"]
    assert day13(test) == {"part1": 24, "part2": 10}
    assert day13() == {"part1": 1580, "part2": 3943252}


def test_day12():
    test = [
        "0 <-> 2",
        "1 <-> 1",
        "2 <-> 0, 3, 4",
        "3 <-> 2, 4",
        "4 <-> 2, 3, 6",
        "5 <-> 6",
        "6 <-> 4, 5",
    ]
    assert day12(test) == {"part1": 6, "part2": 2}
    assert day12() == {"part1": 283, "part2": 195}


def test_day11():
    assert day11("ne,ne,ne".split(",")) == {"part1": 3, "part2": 3}
    assert day11("ne,ne,sw,sw".split(",")) == {"part1": 0, "part2": 2}
    assert day11("ne,ne,s,s".split(",")) == {"part1": 2, "part2": 2}
    assert day11("se,sw,se,sw,sw".split(",")) == {"part1": 3, "part2": 3}
    assert day11() == {"part1": 834, "part2": 1569}


def test_day10():
    assert day10_part1([3, 4, 1, 5], 5) == 12
    assert day10_part1() == 40132

    # assert day10_part2('') == 'a2582a3a0e66e6e86e3812dcb672a272'
    assert day10_part2("AoC 2017") == "33efeb34ea91902bb2f59c9920caa6cd"
    assert day10_part2("1,2,3") == "3efbe78a8d82f29979031a4aa0b16a9d"
    assert day10_part2("1,2,4") == "63960835bcdc130f0b66d7ff4f6a5a8e"
    assert day10_part2() == "35b028fe2c958793f7d5a61d07a008c8"


def test_day9():
    assert day9("{<>}") == {"part1": 1, "part2": 0}
    assert day9("{<random characters>}") == {"part1": 1, "part2": 17}
    assert day9("{<<<<>}") == {"part1": 1, "part2": 3}
    assert day9("{<{!>}>}") == {"part1": 1, "part2": 2}
    assert day9("{<!!>}") == {"part1": 1, "part2": 0}
    assert day9("{<!!!>>}") == {"part1": 1, "part2": 0}
    assert day9('{<{o"i!a,<{i<a>}') == {"part1": 1, "part2": 10}
    assert day9("{{{}}}") == {"part1": 6, "part2": 0}
    assert day9("{{},{}}") == {"part1": 5, "part2": 0}
    assert day9("{{{},{},{{}}}}") == {"part1": 16, "part2": 0}
    assert day9("{<a>,<a>,<a>,<a>}") == {"part1": 1, "part2": 4}
    assert day9("{{<ab>},{<ab>},{<ab>},{<ab>}}") == {"part1": 9, "part2": 8}
    assert day9("{{<!!>},{<!!>},{<!!>},{<!!>}}") == {"part1": 9, "part2": 0}
    assert day9("{{<a!>},{<a!>},{<a!>},{<ab>}}") == {"part1": 3, "part2": 17}
    assert day9() == {"part1": 8337, "part2": 4330}


def test_day8():
    test = [
        "b inc 5 if a > 1",
        "a inc 1 if b < 5",
        "c dec -10 if a >= 1",
        "c inc -20 if c == 10",
    ]
    assert day8(test) == {"part1": 1, "part2": 10}
    assert day8() == {"part1": 2971, "part2": 4254}


def test_day7():
    test = [
        "pbga (66)",
        "xhth (57)",
        "ebii (61)",
        "havc (66)",
        "ktlj (57)",
        "fwft (72) -> ktlj, cntj, xhth",
        "qoyq (66)",
        "padx (45) -> pbga, havc, qoyq",
        "tknk (41) -> ugml, padx, fwft",
        "jptl (61)",
        "ugml (68) -> gyxo, ebii, jptl",
        "gyxo (61)",
        "cntj (57)",
    ]
    assert day7(test) == {"part1": "tknk", "part2": 60}
    assert day7() == {"part1": "rqwgj", "part2": 333}


def test_day6():
    assert day6([0, 2, 7, 0]) == {"part1": 5, "part2": 4}
    assert day6() == {"part1": 3156, "part2": 1610}


def test_day5():
    assert day5_part1([0, 3, 0, 1, -3]) == 5
    assert day5_part1() == 387096

    assert day5_part2([0, 3, 0, 1, -3]) == 10
    assert day5_part2() == 28040648


def test_day4():
    assert day4_part1(["aa bb cc dd ee", "aa bb cc dd aa", "aa bb cc dd aaa"]) == 2
    assert day4_part1() == 451

    assert (
        day4_part2(
            [
                "abcde fghij",
                "abcde xyz ecdab",
                "a ab abc abd abf abj",
                "iiii oiii ooii oooi oooo",
                "oiii ioii iioi iiio",
            ]
        )
        == 3
    )
    assert day4_part2() == 223


def test_day3():
    assert day3_part1(1) == 0
    assert day3_part1(1024) == 31
    assert day3_part1() == 480

    assert day3_part2(500) == 747
    assert day3_part2() == 349975


def test_day2():
    test = [[5, 9, 2, 8], [9, 4, 7, 3], [3, 8, 6, 5]]
    assert day2(test) == {"part1": 18, "part2": 9}
    assert day2() == {"part1": 45972, "part2": 326}


def test_day1():
    assert day1("1122") == {"part1": 3, "part2": 0}
    assert day1("123425") == {"part1": 0, "part2": 4}
    assert day1("123123") == {"part1": 0, "part2": 12}
    assert day1("91212129") == {"part1": 9, "part2": 6}
    assert day1() == {"part1": 1150, "part2": 1064}
