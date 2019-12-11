from aoc_2019_code import *


def test_day4():
    assert day4() == {'part1': 1099, 'part2': 710}


def test_day3():
    assert day3(['R8,U5,L5,D3', 'U7,R6,D4,L4']) == {'part1': 6, 'part2': 30}
    assert day3(['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83']) == {'part1': 159, 'part2': 610}
    assert day3(['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']) == {'part1': 135, 'part2': 410}
    assert day3() == {'part1': 529, 'part2': 20386}


def test_day2():
    assert day2('1,9,10,3,2,3,11,0,99,30,40,50') == 3500
    assert day2('1,0,0,0,99') == 2
    # assert day2('2,3,0,3,99') == 2
    # assert day2('2,4,4,5,99,0') == 2
    assert day2('1,1,1,4,99,5,6,0,99') == 30
    assert day2(None, (12, 2)) == 3790645
    assert day2(None, (65, 77)) == 19690720
