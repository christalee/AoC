from aoc_2020_code import *


def test_day5():
    assert day5() == {"part1": 980, "part2": 607}


def test_day4():
    test1 = "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd\nbyr:1937 iyr:2017 cid:147 hgt:183cm\n\niyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884\nhcl:#cfa07d byr:1929\n\nhcl:#ae17e1 iyr:2013\neyr:2024\necl:brn pid:760753108 byr:1931\nhgt:179cm\n\nhcl:#cfa07d eyr:2025 pid:166559648\niyr:2011 ecl:brn hgt:59in"

    test2 = "eyr:1972 cid:100\nhcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926\n\niyr:2019\nhcl:#602927 eyr:1967 hgt:170cm\necl:grn pid:012533040 byr:1946\n\nhcl:dab227 iyr:2012\necl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277\n\nhgt:59cm ecl:zzz\neyr:2038 hcl:74454a iyr:2023\npid:3556412378 byr:2007"

    test3 = "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980\nhcl:#623a2f\n\neyr:2029 ecl:blu cid:129 byr:1989\niyr:2014 pid:896056539 hcl:#a97842 hgt:165cm\n\nhcl:#888785\nhgt:164cm byr:2001 iyr:2015 cid:88\npid:545766238 ecl:hzl\neyr:2022\n\niyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"

    assert day4(test1) == {"part1": 2, "part2": 0}
    assert day4(test2) == {"part1": 0, "part2": 0}
    assert day4(test3) == {"part1": 4, "part2": 4}
    assert day4() == {"part1": 239, "part2": 188}


def test_day3():
    test = ["..##.......",
            "#...#...#..",
            ".#....#..#.",
            "..#.#...#.#",
            ".#...##..#.",
            "..#.##.....",
            ".#.#.#....#",
            ".#........#",
            "#.##...#...",
            "#...##....#",
            ".#..#...#.#"]

    assert day3(test) == {'part1': 7, 'part2': 336}
    assert day3() == {"part1": 189, 'part2': 1718180100}


def test_day2():
    test = ["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"]
    assert day2(test) == {'part1': 2, 'part2': 1}
    assert day2() == {'part1': 582, 'part2': 729}


def test_day1():
    test = [1721, 979, 366, 299, 675, 1456]
    assert day1(test) == {'part1': 514579, 'part2': 241861950}
    assert day1() == {'part1': 468051, 'part2': 272611658}
