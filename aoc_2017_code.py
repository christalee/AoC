# Christalee Bieber, 2020
# cbieber@alum.mit.edu

# Advent of Code 2017
# http://adventofcode.com/2017/

import decimal
import re
import math
from typing import List, Optional, Dict, Tuple, Union, Set, TypedDict, Literal
from dataclasses import dataclass
from collections import deque, defaultdict

import numpy as np


def input(filename: str) -> List[str]:
    with open("input_2017/" + filename, "r") as f:
        data = [x.strip() for x in f]

    return data


def day25_rules_re(
    state: str, lines: List[str], rules: Dict[str, Dict[str, Dict[str, str]]]
) -> Dict[str, Dict[str, Dict[str, str]]]:
    value_re = re.search(r"^If the current value is (.):$", lines[0])
    write_re = re.search(r"^- Write the value (.)\.$", lines[1])
    move_re = re.search(r"^- Move one slot to the (.*)\.$", lines[2])
    next_re = re.search(r"^- Continue with state (.)\.$", lines[3])
    if value_re and write_re and move_re and next_re:
        rules[state][value_re.group(1)] = {
            "write": write_re.group(1),
            "move": move_re.group(1),
            "next": next_re.group(1),
        }

    return rules


def day25_step(
    instructions: Dict[str, Dict[str, str]], tape: List[int], state: str, position: int
) -> Tuple[List[int], str, int]:
    todo = instructions[str(tape[position])]
    tape[position] = int(todo["write"])
    if todo["move"] == "right":
        position += 1
    elif todo["move"] == "left":
        position -= 1
    state = todo["next"]

    return tape, state, position


def day25_augment(tape: List[int], position: int) -> Tuple[List[int], int]:
    extra = [0 for x in range(1000)]
    position += 1000
    return extra + tape + extra, position


def day25(blueprint: List[str] = None) -> int:
    if not blueprint:
        blueprint = input("day25.txt")

    n_re = re.search(
        r"^Perform a diagnostic checksum after (.*) steps\.$", blueprint[1]
    )
    if n_re:
        n = int(n_re.group(1))
    else:
        n = 0

    rules: Dict[str, Dict[str, Dict[str, str]]] = {}
    for i in range(3, len(blueprint), 10):
        line = blueprint[i]
        state_re = re.search(r"^In state (.):$", line)
        if state_re:
            state = state_re.group(1)
            rules[state] = {}
            rules = day25_rules_re(state, blueprint[i + 1 : i + 5], rules)
            rules = day25_rules_re(state, blueprint[i + 5 : i + 9], rules)

    tape = [0 for x in range(1000)]
    state = "A"
    position = len(tape) // 2

    for _ in range(n):
        if position == 0 or position == len(tape) - 1:
            tape, position = day25_augment(tape, position)
        instructions = rules[state]
        tape, state, position = day25_step(instructions, tape, state, position)

    return sum(tape)


@dataclass(frozen=True)
class Part:
    start: int
    end: int

    def __repr__(self):
        return f"{self.start}/{self.end}"


def day24_bridge_repr(bridge_tuple: Tuple[int], part: Part) -> Tuple[int]:
    if part.start == bridge_tuple[-1]:
        return (*bridge_tuple, *[part.start, part.end])
    elif part.end == bridge_tuple[-1]:
        return (*bridge_tuple, *[part.end, part.start])
    else:
        print("invalid bridge: ", bridge_tuple, part)
        return ()


def day24_find_connections(part_end: int, available_parts: Set[Part]) -> List[Part]:
    return list(
        filter(lambda x: x.start == part_end or x.end == part_end, available_parts)
    )


def day24(parts: List[str] = None) -> Dict[str, int]:
    if not parts:
        parts = input("day24.txt")

    parts_list: Set[Part] = set()
    for p in parts:
        start, end = p.split("/")
        parts_list.add(Part(start=int(start), end=int(end)))

    bridges: Dict[Tuple[int], Set[Part]] = {}
    bridge_starts = day24_find_connections(0, parts_list)
    for b in bridge_starts:
        bridges[day24_bridge_repr((0,), b)] = set([b])

    bridges_to_explore = bridges.copy()
    while True:
        next_bridges = {}
        for b, v in bridges_to_explore.items():
            next_parts = day24_find_connections(b[-1], parts_list - v)
            for p in next_parts:
                new_bridge = bridges_to_explore[b].copy()
                new_bridge.add(p)
                next_bridges[day24_bridge_repr(b, p)] = new_bridge

        if len(next_bridges) == 0:
            break
        bridges |= next_bridges
        bridges_to_explore = next_bridges

    part1 = sorted(bridges.keys(), key=lambda x: sum(x), reverse=True)
    bridges_by_length = sorted(bridges.keys(), key=lambda x: len(x), reverse=True)
    part2 = sorted(
        list(filter(lambda x: len(x) == len(bridges_by_length[0]), bridges.keys())),
        key=lambda x: sum(x),
        reverse=True,
    )

    return {"part1": sum(part1[0]), "part2": sum(part2[0])}


def day23_loop_11_19(b, d, e, f, g):
    # original implementation (used for testing)
    # while g != 0:  # 19
    #     g = (d * e) - b  # 11, 12, 13
    #     if g == 0:  # 14
    #         f = 0  # 15
    #     e += 1  # 16
    #     g = e - b  # 17, 18

    # return b, d, e, f, g

    # e ranges from integers e to b
    # also b / d has to be an integer -> b % d == 0
    # check if d * e - b crosses 0 in either direction
    start = (d * e) - b
    end = (d * b) - b
    if b % d == 0 and ((start < 0 and end > 0) or (start > 0 and end < 0)):
        f = 0
    return b, d, b, f, 0


def day23_loop_10_23(b, d, e, f, g):
    # original implementation (used for testing)
    # while g != 0:  # 23
    #     e = 2  # 10
    #     b, d, e, f, g = loop_11_19(b, d, e, f, g)
    #     d += 1  # 20
    #     g = d - b  # 21, 22

    # return b, d, e, f, g

    # only check values of d where b % d == 0
    # to set f in loop_11_19
    while b % d != 0:
        d += 1
    for x in range(d, b, d):
        b, d, e, f, g = day23_loop_11_19(b, x, 2, f, g)
    b, d, e, f, g = day23_loop_11_19(b, b - 1, 2, f, g)

    return b, b, e, f, 0


def day23_compiled() -> int:
    a = 1  # init
    b = 67  # 0
    c = b  # 1
    d = 0  # init
    e = 0  # init
    f = 0  # init
    g = 0  # init
    h = 0  # init
    # a = 1 and never gets reassigned, so the else branch is never reached
    if a != 0:  # 2 / skip 3
        b = (b * 100) + 100000  # 4, 5
        c = b + 17000  # 6, 7
        f = 1  # 8
        d = 2  # 9
        e = 2  # 10
        g = (d * e) - b  # 11, 12, 13
        if g == 0:  # 14
            f = 0  # 15
        e += 1  # 16
        g = e - b  # 17, 18
        b, d, e, f, g = day23_loop_11_19(b, d, e, f, g)
        d += 1  # 20
        g = d - b  # 21, 22
        b, d, e, f, g = day23_loop_10_23(b, d, e, f, g)
        if f == 0:  # 24
            h += 1  # 25
        g = b - c  # 26, 27
        while g != 0:  # 28 / skip 29
            b += 17  # 30
            f = 1  # 8
            d = 2  # 9
            e = 2  # 10
            g = (d * e) - b  # 11, 12, 13
            if g == 0:  # 14
                f = 0  # 15
            e += 1  # 16
            g = e - b  # 17, 18
            b, d, e, f, g = day23_loop_11_19(b, d, e, f, g)
            d += 1  # 20
            g = d - b  # 21, 22
            b, d, e, f, g = day23_loop_10_23(b, d, e, f, g)
            if f == 0:  # 24
                h += 1
            g = b - c  # 26, 27
        return h  # 29
    else:
        return h


# DO NOT RUN THIS!
# def day23_part2(instructions: List[str] = None) -> int:
#     if not instructions:
#         instructions = input("day23.txt")

#     registers: Dict[str, int] = {x: 0 for x in 'bcdefgh'}
#     registers['a'] = 1
#     i = 0
#     while i >= 0 and i < len(instructions):
#         tokens = instructions[i].split()
#         if tokens[0] == "set":
#             registers[tokens[1]] = day18_parse_value(registers, tokens[2])
#         if tokens[0] == "sub":
#             registers[tokens[1]] -= day18_parse_value(registers, tokens[2])
#         if tokens[0] == "mul":
#             registers[tokens[1]] *= day18_parse_value(registers, tokens[2])
#         if tokens[0] == "jnz":
#             t1 = day18_parse_value(registers, tokens[1])
#             if t1 != 0:
#                 i += day18_parse_value(registers, tokens[2]) - 1

#         i += 1

#     return registers['h']


def day23_part1(instructions: List[str] = None) -> int:
    if not instructions:
        instructions = input("day23.txt")

    registers: Dict[str, int] = {x: 0 for x in "abcdefgh"}
    i = 0
    mul_count = 0
    while i >= 0 and i < len(instructions):
        tokens = instructions[i].split()
        if tokens[0] == "set":
            registers[tokens[1]] = day18_parse_value(registers, tokens[2])
        if tokens[0] == "sub":
            registers[tokens[1]] -= day18_parse_value(registers, tokens[2])
        if tokens[0] == "mul":
            registers[tokens[1]] *= day18_parse_value(registers, tokens[2])
            mul_count += 1
        if tokens[0] == "jnz":
            t1 = day18_parse_value(registers, tokens[1])
            if t1 != 0:
                i += day18_parse_value(registers, tokens[2]) - 1

        i += 1

    return mul_count


def day22_augment(maze):
    size = len(maze)
    new_maze = []
    empty = ["." for x in range(size + 2)]
    new_maze.append(empty)
    for row in maze:
        new_row = ["."] + row + ["."]
        new_maze.append(new_row)
    new_maze.append(empty)

    return new_maze


def day22_turn(direction, delta):
    directions = "URDL"  # turn right => return n + 1, turn left => return n - 1
    i = directions.index(direction)
    if delta == "R":
        return directions[(i + 1) % 4]
    elif delta == "L":
        return directions[i - 1]
    elif delta == "180":
        return directions[i - 2]


def day22_move(position, direction):
    x, y = position
    if direction == "U":
        return [x, y - 1]
    if direction == "D":
        return [x, y + 1]
    if direction == "R":
        return [x + 1, y]
    if direction == "L":
        return [x - 1, y]


def day22_part2(field: List[str] = None) -> int:
    if not field:
        field = input("day22.txt")

    f = list(map(list, field))
    position = [len(f) // 2, len(f) // 2]
    direction = "U"
    infected = 0

    for _ in range(10_000_000):
        x, y = position
        if x == 0 or y == 0 or x == len(m) - 1 or y == len(m) - 1:
            m = day22_augment(m)
            x += 1
            y += 1
            position = [x, y]
        curr = m[y][x]
        if curr == ".":
            direction = day22_turn(direction, "L")
            m[y][x] = "W"
        elif curr == "W":
            m[y][x] = "#"
            infected += 1
        elif curr == "#":
            direction = day22_turn(direction, "R")
            m[y][x] = "F"
        elif curr == "F":
            direction = day22_turn(direction, "180")
            m[y][x] = "."
        position = day22_move(position, direction)

    return infected


def day22_part1(field: List[str] = None) -> int:
    if not field:
        field = input("day22.txt")

    f = list(map(list, field))
    position = [len(f) // 2, len(f) // 2]
    direction = "U"
    infected = 0

    for _ in range(10000):
        x, y = position
        if x == 0 or y == 0 or x == len(f) - 1 or y == len(f) - 1:
            f = day22_augment(f)
            x += 1
            y += 1
            position = [x, y]
        curr = f[y][x]
        if curr == ".":
            direction = day22_turn(direction, "L")
            f[y][x] = "#"
            infected += 1
        elif curr == "#":
            direction = day22_turn(direction, "R")
            f[y][x] = "."
        position = day22_move(position, direction)

    return infected


def day21_sum_hashes(pattern):
    total = 0
    for row in pattern:
        for char in row:
            if char == "#":
                total += 1
    return total


def day21_rotate_flip(pattern):
    flipped = [np.flip(pattern), np.flipud(pattern), np.fliplr(pattern)]
    rotated = [np.rot90(f, k) for k in range(4) for f in flipped]
    return rotated


def day21_take_by_n(pattern, size, n):
    blocks = []
    rows = np.split(pattern, size // n)
    for row in rows:
        blocks.append(np.split(row, size // n, axis=1))
    return blocks


def day21_coalesce(pattern, size):
    new_y = len(pattern)
    new_x = len(pattern[0])
    new_size = int(math.sqrt(new_y * new_x))
    new_pattern = []
    if size % 2 == 0:  # has been converted to 3x3 blocks
        new_block_size = 3
    elif size % 3 == 0:  # has been converted to 4x4 blocks
        new_block_size = 4
    x_limit = new_y // new_size
    for y in range(0, new_y, new_size):
        for x in range(y, y + new_block_size):
            new_row = []
            for z in range(x_limit):
                new_row.extend(pattern[x + new_block_size * z])
            new_pattern.append(new_row)
    return new_pattern


def day21_loop(rules, pattern, n):
    for i in range(n):
        size = len(pattern)
        new_pattern = []
        if size % 2 == 0:
            blocks = day21_take_by_n(np.array(pattern), size, 2)
        elif size % 3 == 0:
            blocks = day21_take_by_n(np.array(pattern), size, 3)
        else:
            print("size not divisible by 2 or 3")
        for row in blocks:
            new_row = []
            for b in row:
                new_row.extend(rules[tuple(map(tuple, b.tolist()))])
            new_pattern.extend(new_row)

        pattern = day21_coalesce(new_pattern, size)

    return day21_sum_hashes(pattern)


def day21(book: List[str] = None) -> Dict[str, int]:
    if not book:
        book = input("day21.txt")

    pattern = [".#.", "..#", "###"]
    split_pattern = [list(y) for y in pattern]

    rules = {}
    for rule in book:
        a, b = rule.split(" => ")
        k = list(map(list, a.split("/")))
        v = list(map(list, b.split("/")))
        variants = day21_rotate_flip(k)
        for x in variants:
            rules[tuple(map(tuple, x.tolist()))] = v

    part1 = day21_loop(rules, split_pattern, 5)
    part2 = day21_loop(rules, split_pattern, 18)

    return {"part1": part1, "part2": part2}


Vectors = TypedDict("Vectors", {"pos": List[int], "vel": List[int], "acc": List[int]})


def day20_accelerate(vel: List[int], acc: List[int]) -> List[int]:
    vel[0] += acc[0]
    vel[1] += acc[1]
    vel[2] += acc[2]
    return vel


def day20_move(pos: List[int], vel: List[int]) -> List[int]:
    pos[0] += vel[0]
    pos[1] += vel[1]
    pos[2] += vel[2]
    return pos


def day20_collisions(particles):
    updated = particles.copy()
    for k, v in particles.items():
        for j, w in particles.items():
            if k != j and v["pos"] == w["pos"]:
                if k in updated:
                    del updated[k]
                if j in updated:
                    del updated[j]
    return updated


def day20_part2(particles: List[str] = None) -> int:
    if not particles:
        particles = input("day20.txt")

    particlesd: Dict[int, Vectors] = {}
    for i in range(len(particles)):
        p, v, a = particles[i].split(", ")
        pos = list(map(int, p.strip("p=<> ").split(",")))
        vel = list(map(int, v.strip("v=<> ").split(",")))
        acc = list(map(int, a.strip("a=<> ").split(",")))
        particlesd[i] = {"pos": pos, "vel": vel, "acc": acc}

    for _ in range(500):  # chosen for how long it took to reach part1
        for p in particlesd.values():
            p["vel"] = day20_accelerate(p["vel"], p["acc"])
            p["pos"] = day20_move(p["pos"], p["vel"])
        particlesd = day20_collisions(particlesd)

    return len(particlesd)


# Loop used to measure "steady state" after determining the answer as below
# while True:
#     min_dist = math.inf
#     min_dist_name = -1
#     for k, p in particles.items():
#         p['vel'] = accelerate(p['vel'], p['acc'])
#         p['pos'] = move(p['pos'], p['vel'])
#         dist = sum(map(abs, p['pos']))
#         if dist < min_dist:
#             min_dist = dist
#             min_dist_name = k
#     closest.append(min_dist_name)
#     particles = collisions(particles)
#     if len(closest) > 100 and len(set(closest[-100:])) == 1 and closest[-1] == 119:
#         break


def day20_part1(particles: List[str] = None) -> int:
    if not particles:
        particles = input("day20.txt")

    particlesd = {}
    for i in range(len(particles)):
        p, v, a = particles[i].split(", ")
        pos = list(map(int, p.strip("p=<> ").split(",")))
        vel = list(map(int, v.strip("v=<> ").split(",")))
        acc = list(map(int, a.strip("a=<> ").split(",")))
        particlesd[i] = {"pos": pos, "vel": vel, "acc": acc}

    sorted_by_acc = sorted(
        particlesd, key=lambda x: sum(map(abs, particlesd[x]["acc"]))
    )
    return sorted_by_acc[0]


def day19_find_next(point: Tuple[int, int], direction: str, x_size: int, y_size: int):
    x, y = point
    if direction == "U":
        if y - 1 >= 0:
            return (x, y - 1)
    elif direction == "D":
        if y + 1 < y_size:
            return (x, y + 1)
    elif direction == "R":
        if x + 1 < x_size:
            return (x + 1, y)
    elif direction == "L":
        if x - 1 >= 0:
            return (x - 1, y)
    return (False, False)


def day19(maze: List[str] = None) -> Dict[str, Union[str, int]]:
    if not maze:
        with open("input_2017/day19.txt", "r") as f:
            for line in f:
                maze.append(line.strip("\n"))

    direction = "D"
    pos = (maze[0].index("|"), 0)
    opposite = {"U": "D", "D": "U", "R": "L", "L": "R"}
    y_size = len(maze)
    x_size = len(maze[0])

    letters = ""
    steps = 1  # we count the initial step as step 1
    while True:
        x_nxt, y_nxt = day19_find_next(pos, direction, x_size, y_size)
        if x_nxt and y_nxt:
            symbol = maze[y_nxt][x_nxt]
        else:
            symbol = " "
        if symbol.isalpha():
            letters += symbol
        elif symbol == "+":
            for d in "UDLR":
                x_around, y_around = day19_find_next((x_nxt, y_nxt), d, x_size, y_size)
                if x_around and y_around:
                    around = maze[y_around][x_around]
                else:
                    continue
                if d != opposite[direction] and around != " ":
                    if around.isalpha():
                        letters += around
                    direction = d
                    steps += 1  # to account for the corner itself
                    x_nxt, y_nxt = x_around, y_around
        elif symbol == " ":
            break
        steps += 1
        pos = (x_nxt, y_nxt)

    return {"part1": letters, "part2": steps}


Program = TypedDict(
    "Program",
    {
        "registers": Dict[str, int],
        "our_queue": List[int],
        "their_queue": List[int],
        "sent": int,
        "blocked": bool,
        "i": int,
    },
)


def day18_parse_value(registers: Dict[str, int], token: str) -> int:
    if token.isalpha():
        return registers[token]
    else:
        return int(token)


def day18_run(
    instructions: List[str],
    program: Program,
):
    tokens = instructions[program["i"]].split()
    registers = program["registers"]
    if tokens[0] == "set":
        registers[tokens[1]] = day18_parse_value(registers, tokens[2])
    if tokens[0] == "add":
        registers[tokens[1]] += day18_parse_value(registers, tokens[2])
    if tokens[0] == "mul":
        registers[tokens[1]] *= day18_parse_value(registers, tokens[2])
    if tokens[0] == "mod":
        registers[tokens[1]] %= day18_parse_value(registers, tokens[2])
    if tokens[0] == "rcv":
        if len(program["our_queue"]) > 0:
            registers[tokens[1]] = program["our_queue"].pop(0)
            program["blocked"] = False
        else:
            # stay on this instruction, don't advance until there's a value
            program["i"] -= 1
            program["blocked"] = True
    if tokens[0] == "jgz":
        t1 = day18_parse_value(registers, tokens[1])
        if t1 > 0:
            program["i"] += day18_parse_value(registers, tokens[2]) - 1
    if tokens[0] == "snd":
        t1 = day18_parse_value(registers, tokens[1])
        program["their_queue"].append(t1)
        program["sent"] += 1


def day18_part2(instructions: List[str] = None) -> int:
    if not instructions:
        instructions = input("day18.txt")

    q0: List[int] = []
    q1: List[int] = []
    p0: Program = {
        "registers": defaultdict(int, [("p", 0)]),
        "our_queue": q0,
        "their_queue": q1,
        "sent": 0,
        "blocked": False,
        "i": 0,
    }
    p1: Program = {
        "registers": defaultdict(int, [("p", 1)]),
        "our_queue": q1,
        "their_queue": q0,
        "sent": 0,
        "blocked": False,
        "i": 0,
    }
    while True:
        day18_run(instructions, p0)
        day18_run(instructions, p1)
        if len(q0) == 0 and len(q1) == 0 and p0["blocked"] and p1["blocked"]:
            break
        p0["i"] += 1
        p1["i"] += 1

    return p1["sent"]


def day18_part1(instructions: List[str] = None) -> int:
    if not instructions:
        instructions = input("day18.txt")

    registers: Dict[str, int] = defaultdict(int)
    last_played = 0
    i = 0
    while i >= 0 and i < len(instructions):
        tokens = instructions[i].split()
        if tokens[0] == "set":
            registers[tokens[1]] = day18_parse_value(registers, tokens[2])
        if tokens[0] == "add":
            registers[tokens[1]] += day18_parse_value(registers, tokens[2])
        if tokens[0] == "mul":
            registers[tokens[1]] *= day18_parse_value(registers, tokens[2])
        if tokens[0] == "mod":
            registers[tokens[1]] %= day18_parse_value(registers, tokens[2])
        if tokens[0] == "rcv":
            t1 = day18_parse_value(registers, tokens[1])
            if t1 > 0:
                return last_played
        if tokens[0] == "jgz":
            t1 = day18_parse_value(registers, tokens[1])
            if t1 > 0:
                i += day18_parse_value(registers, tokens[2]) - 1
        if tokens[0] == "snd":
            last_played = day18_parse_value(registers, tokens[1])

        i += 1

    return 0


def day17(n: int = None, reps: int = 50_000_000, target: int = 0):
    if not n:
        n = 303

    buffer = deque([0])
    for i in range(1, reps + 1):
        offset = (n % i) + 1
        buffer.rotate(-offset)
        buffer.appendleft(i)

    return buffer[buffer.index(target) + 1]


class Move_S(TypedDict):
    type: Literal['s']
    value: int


class Move_X(TypedDict):
    type: Literal['x']
    value: List[int]


class Move_P(TypedDict):
    type: Literal['p']
    value: List[str]


Move = Move_S | Move_X | Move_P


def day16_groove(line: List[str], moves: List[Move]) -> List[str]:
    for move in moves:
        if move['type'] == 's':
            l = move['value']
            line = line[-l:] + line[:-l]
        elif move['type'] == 'x':
            ia, ib = move['value']
            a = line[ia]
            b = line[ib]
            line[ia] = b
            line[ib] = a
        elif move['type'] == 'p':
            a, b = move['value']
            ia = line.index(a)
            ib = line.index(b)
            line[ia] = b
            line[ib] = a

    return line


def day16(dance: List[str] = None) -> Dict[str, str]:
    if not dance:
        dance = input('day16.txt')[0].split(',')

    moves: List[Move] = []
    for move in dance:
        move_dict: Move = {}
        if move.startswith('s'):
            move_dict = Move_S(type='s', value=int(move.removeprefix('s')))
            # move_dict['type'] = 's'
            # move_dict['value'] = int(move.removeprefix('s'))
        elif move.startswith('x'):
            move_dict = Move_X(type='x', value=list(map(int, move.removeprefix('x').split('/'))))
            # move_dict['type'] = 'x'
            # move_dict['value'] = list(map(int, move.removeprefix('x').split('/')))
        elif move.startswith('p'):
            move_dict = Move_P(type='p', value=move.removeprefix('p').split('/'))
            # move_dict['type'] = 'p'
            # move_dict['value'] = move.removeprefix('p').split('/')
        moves.append(move_dict)

    line = list('abcdefghijklmnop')

    part1 = ''.join(day16_groove(line, moves))

    # Turns out the permutation is cyclic (but why so short?)
    x = 0
    for i in range(1000):
        line = day16_groove(line, moves)
        if line == list('abcdefghijklmnop'):
            x = i
            break

    for i in range(1_000_000_000 % (x + 1)):
        line = day16_groove(line, moves)

    part2 = ''.join(line)

    return {'part1': part1, 'part2': part2}


def day15_rem1(value: int, factor: int, divisor: int) -> int:
    return (value * factor) % divisor


def day15_rem2(value: int, factor: int, divisor: int, multiple: int) -> int:
    while True:
        value = day15_rem1(value, factor, divisor)
        if value % multiple == 0:
            break

    return value


def day15_part1(n: int = 40_000_000, valueA: int = 512, valueB: int = 191) -> int:
    factorA = 16807
    factorB = 48271
    divisor = 2147483647
    score = 0
    bitmask = 0b1111111111111111  # returns lowest 16 bits of the int
    for _ in range(n):
        valueA = day15_rem1(valueA, factorA, divisor)
        valueB = day15_rem1(valueB, factorB, divisor)
        if valueA & bitmask == valueB & bitmask:
            score += 1

    return score


def day15_part2(n: int = 5_000_000, valueA: int = 512, valueB: int = 191) -> int:
    factorA = 16807
    factorB = 48271
    multipleA = 4
    multipleB = 8
    divisor = 2147483647
    score = 0
    bitmask = 0b1111111111111111  # returns lowest 16 bits of the int
    for _ in range(n):
        valueA = day15_rem2(valueA, factorA, divisor, multipleA)
        valueB = day15_rem2(valueB, factorB, divisor, multipleB)
        if valueA & bitmask == valueB & bitmask:
            score += 1

    return score


# island is a set of points, not a list
def day14_find_island(island: Set[Tuple[int, int]], memory: List[List[int]]):
    n = []
    new_island = island.copy()
    for point in island:
        n += day14_find_neighbors(point)
    cells = {x: memory[x[1]][x[0]] for x in n}
    for k, v in cells.items():
        if v == 1:
            new_island.add(k)
    if len(new_island) == len(island):
        return island
    else:
        return day14_find_island(new_island, memory)


# find vertical/horizontal neighbors, not diagonals
def day14_find_neighbors(
    point: Tuple[int, int], size: int = 128
) -> List[Tuple[int, int]]:
    x, y = point
    n = []
    if x - 1 >= 0:
        n.append((x - 1, y))
    if y - 1 >= 0:
        n.append((x, y - 1))
    if x + 1 < size:
        n.append((x + 1, y))
    if y + 1 < size:
        n.append((x, y + 1))

    return n


def day14_hex_to_bin(n: str) -> str:
    b = bin(int(n, 16)).removeprefix("0b")
    while len(b) < 4:
        b = "0" + b

    return b


def day14(key: str = "ljoxqyyw") -> Dict[str, int]:
    memory = []
    used = 0
    for x in range(128):
        s = f"{key}-{x}"
        h = day10_part2(s)
        row = ""
        for char in h:
            row += day14_hex_to_bin(char)
        symbols = list(map(int, list(row)))
        used += sum(symbols)
        memory.append(symbols)

    islands: List[Set[Tuple[int, int]]] = []
    for y in range(len(memory)):
        for x in range(len(memory[y])):
            curr = memory[y][x]
            if curr == 1:
                point = (x, y)
                for isle in islands:
                    if point in isle:
                        break
                else:
                    islands.append(day14_find_island(set([point]), memory))

    return {"part1": used, "part2": len(islands)}


def day13_advance_fw(
    delay: int, gauntlet: List[List[Optional[int]]], break_early: bool
) -> Union[List[int], bool]:
    pos = []
    for i, wall in enumerate(gauntlet):
        offset = (delay + i) % len(wall)
        w = wall[offset]
        if w == 0 and break_early:
            return False
        pos.append(w)

    return pos


def day13(walls: Optional[List[str]] = None) -> Dict[str, int]:
    if not walls:
        walls = input("day13.txt")

    fw_depth = int(walls[-1].split(": ")[0]) + 1
    gauntlet: List[List[Optional[int]]] = [[None] for x in range(fw_depth)]
    for w in walls:
        d, r = w.split(": ")
        gauntlet[int(d)] = list(range(int(r) - 1)) + list(range(int(r) - 1, 0, -1))

    delay = 0
    part1 = 0
    pos0 = day13_advance_fw(delay, gauntlet, False)
    for i in range(fw_depth):
        if pos0[i] == 0:
            part1 += i * (max(gauntlet[i]) + 1)

    while True:
        # pessimistic O(position_cycle)
        # (N for the firewall to circulate back to initial state)
        position = day13_advance_fw(delay, gauntlet, True)
        if position:
            break
        delay += 1

    return {"part1": part1, "part2": delay}


def day12_find_group(node: int, conns: List[Tuple[int, int]]) -> Set[int]:
    init = set([node])
    while True:  # runs n times, where n = 2000 at worst
        new_group = init.copy()
        for c in conns:  # len(conns) = 3805 * n
            end1, end2 = c
            if end1 in new_group:
                continue
            elif end2 in new_group:
                new_group.add(end1)
        if len(new_group) == len(init):
            break
        else:
            init = new_group

    return init


def day12(pipes: List[str] = None) -> Dict[str, int]:
    if not pipes:
        pipes = input("day12.txt")

    conns = []
    for p in pipes:
        p1, p2 = p.split(" <-> ")
        end1 = int(p1)
        end2 = list(map(int, p2.split(", ")))
        for e in end2:
            conns.append((end1, e))

    groups = [day12_find_group(x, conns) for x in range(len(pipes))]
    results = set()
    for g in groups:
        results.add(tuple(sorted(g)))

    return {"part1": len(groups[0]), "part2": len(results)}


def day11_hex_distance(location: List[float]) -> int:
    return int(abs(location[0]) + abs(location[1]))


def day11(steps: List[str] = None) -> Dict[str, int]:
    if not steps:
        steps = input("day11.txt")[0].split(",")

    position: List[Union[int, float]] = [0, 0]
    max_pos = 0
    for s in steps:
        if s == "n":
            position[1] += 1
        if s == "s":
            position[1] -= 1
        if s == "ne":
            position[0] += 0.5
            position[1] += 0.5
        if s == "sw":
            position[0] -= 0.5
            position[1] -= 0.5
        if s == "nw":
            position[0] += 0.5
            position[1] -= 0.5
        if s == "se":
            position[0] -= 0.5
            position[1] += 0.5
        max_pos = max(max_pos, day11_hex_distance(position))

    return {"part1": day11_hex_distance(position), "part2": max_pos}


def day10_knot(
    lengths: List[int], loop_len: int, loop: List[int], skip: int, curr: int
) -> Tuple[List[int], int, int]:

    for l in lengths:
        if curr + l >= loop_len:
            remainder = (curr + l) % loop_len
            section = loop[curr:curr + l - remainder] + loop[:remainder]
        else:
            section = loop[curr:curr + l]
        section = section[::-1]
        for i in range(l):
            if curr + i >= loop_len:
                pos = (curr + i) % loop_len
                loop[pos] = section[i]
            else:
                loop[curr + i] = section[i]
        curr += l + skip
        curr = curr % loop_len
        skip += 1

    return loop, skip, curr


def day10_part2(inp: Union[List[str], str] = "", loop_len: int = 256) -> str:
    if not inp:
        with open("input_2017/day10.txt", "r") as f:
            inp = list(f.readline().strip())

    lengths = []
    for l in inp:
        lengths.append(ord(l))
    lengths += [17, 31, 73, 47, 23]

    loop = list(range(loop_len))
    skip = 0
    curr = 0

    for x in range(64):
        loop, skip, curr = day10_knot(lengths, loop_len, loop, skip, curr)

    dense_hash = []
    for x in range(0, len(loop), 16):
        r = loop[x:x + 16]
        result = 0
        for elem in r:
            result = result ^ elem
        dense_hash.append(result)

    part2 = ""
    for elem in dense_hash:
        h = hex(elem).removeprefix("0x")
        if len(h) < 2:
            h = "0" + h
        part2 += h

    return part2


def day10_part1(lengths: List[int] = None, loop_len: int = 256) -> int:
    if not lengths:
        with open("input_2017/day10.txt", "r") as f:
            lengths = list(map(int, f.readline().split(",")))

    loop = list(range(loop_len))
    skip = 0
    curr = 0

    result, _, _ = day10_knot(lengths, loop_len, loop, skip, curr)

    return result[0] * result[1]


def day9(stream: str = None) -> Dict[str, int]:
    if not stream:
        with open("input_2017/day9.txt", "r") as input:
            stream = input.readline().strip()

    garbage = False
    i = 0
    group_total = 0
    score = 0
    garbage_total = 0
    while i < len(stream):
        char = stream[i]
        if char == "!":
            i += 1
        elif char == "<":
            if not garbage:
                garbage = True
            else:
                garbage_total += 1
        elif char == ">":
            garbage = False
        elif char == "{" and not garbage:
            score += 1
        elif char == "}" and not garbage:
            group_total += score
            score -= 1

        if garbage and char not in ["<", ">", "!"]:
            garbage_total += 1
        i += 1

    return {"part1": group_total, "part2": garbage_total}


def day8_inc_dec(registers: Dict[str, int], reg: str, op: str, amt: int):
    if op == "inc":
        registers[reg] += amt
    elif op == "dec":
        registers[reg] -= amt
    else:
        print("unknown register op")


def day8(instructions: List[str] = None) -> Dict[str, int]:
    if not instructions:
        instructions = input("day8.txt")

    registers = {}
    global_max = 0

    for i in instructions:
        # first, parse instructions and populate registers
        cmd, cnd = i.split(" if ")
        cmd_reg, cmd_op, cmd_amt = cmd.split()
        if cmd_reg not in registers:
            registers[cmd_reg] = 0

        cnd_reg, cnd_op, cnd_amt = cnd.split()
        if cnd_reg not in registers:
            registers[cnd_reg] = 0

        # then start processing instructions
        if cnd_op == ">" and registers[cnd_reg] > int(cnd_amt):
            day8_inc_dec(registers, cmd_reg, cmd_op, int(cmd_amt))
        elif cnd_op == "<" and registers[cnd_reg] < int(cnd_amt):
            day8_inc_dec(registers, cmd_reg, cmd_op, int(cmd_amt))
        elif cnd_op == ">=" and registers[cnd_reg] >= int(cnd_amt):
            day8_inc_dec(registers, cmd_reg, cmd_op, int(cmd_amt))
        elif cnd_op == "<=" and registers[cnd_reg] <= int(cnd_amt):
            day8_inc_dec(registers, cmd_reg, cmd_op, int(cmd_amt))
        elif cnd_op == "==" and registers[cnd_reg] == int(cnd_amt):
            day8_inc_dec(registers, cmd_reg, cmd_op, int(cmd_amt))
        elif cnd_op == "!=" and registers[cnd_reg] != int(cnd_amt):
            day8_inc_dec(registers, cmd_reg, cmd_op, int(cmd_amt))
        else:
            print("unknown condition op")
        global_max = max(global_max, max(registers.values()))

    return {"part1": max(registers.values()), "part2": global_max}


@dataclass
class Node:
    name: str
    weight: int
    parent: Optional[Node]
    children: Optional[List[Node]]


def day7_get_weights(node: Node) -> int:
    if node.children:
        return sum(day7_get_weights(x) for x in node.children) + node.weight
    else:
        return node.weight


def day7_check_weights(node: Node) -> Union[bool, Dict[str, int]]:
    results = {}
    if node.children:
        for x in node.children:
            results[x.name] = day7_get_weights(x)

        weights = results.values()
        min_weight = min(weights)
        max_weight = max(weights)
        if min_weight != max_weight:
            return results

    return False


def day7(relations: List[str] = None) -> Dict[str, Union[str, int]]:
    if not relations:
        relations = input("day7.txt")

    tree = []
    # populate tree with unconnected nodes
    with_children = r"^(\w+) \((\d+)\) -> (.*)$"
    wout_children = r"^(\w+) \((\d+)\)$"
    for r in relations:
        if "->" in r:
            m = re.search(with_children, r)
            if m:
                name, weight, children = m.group(1, 2, 3)
                children = children.split(", ")
        else:
            m = re.search(wout_children, r)
            if m:
                name, weight = m.group(1, 2)
                children = None
        new_node = Node(name=name, weight=int(weight), parent=None, children=children)
        tree.append(new_node)

    # populate parents, based on membership in children (list of strings)
    for node in tree:
        parent = list(
            filter(lambda x: node.name in x.children if x.children else False, tree)
        )
        if len(parent) > 0:
            node.parent = parent[0]
        else:
            node.parent = None

    # populate children separately to avoid mutating lists of strings to
    # lists of Nodes during parent loop
    for node in tree:
        children = list(
            filter(lambda x: x.name in node.children if node.children else False, tree)
        )
        node.children = children

    part1 = list(filter(lambda node: node.parent == None, tree))[0].name

    aberrant_weight = math.inf
    aberrant_name = ""
    offset = 0
    for node in tree:
        # result is a dict holding nodes at the same level (children of a
        # specific node) and their weights
        # e.g. {'nwpmqu': 7041, 'owayyaw': 7041, 'idfyy': 7049}
        # in this case 'idfyy' is the aberrant one, by 8 units
        result = day7_check_weights(node)
        if result:
            # we are looking for the highest disc in the stack with an aberrant weight
            # the highest disc will have the lowest weight
            # its parents will also be aberrant in their weights
            # but that weight will be higher
            aberrant_weight = min(aberrant_weight, max(result.values()))
            # this could be calculated once but instead we will do it for each result
            offset = max(result.values()) - min(result.values())
            # once we find the aberrant_weight, update the name of the answer
            for k, v in result.items():
                if v == aberrant_weight:
                    aberrant_name = k

    # then simply filter and calculate what the weight should be to balance
    aberrant_node = list(filter(lambda node: node.name == aberrant_name, tree))[0]
    part2 = aberrant_node.weight - offset

    return {"part1": part1, "part2": part2}


def day6_reallocate(memory: List[int]) -> Tuple[List[int], int]:
    seen = []
    banks = len(memory)
    while tuple(memory) not in seen:
        seen.append(tuple(memory))
        blocks = max(memory)
        blocks_index = (memory.index(blocks) + 1) % banks
        memory[blocks_index - 1] = 0
        while blocks > 0:
            memory[blocks_index] += 1
            blocks_index = (blocks_index + 1) % banks
            blocks -= 1
    return memory, len(seen)


def day6(memory: List[int] = None) -> Dict[str, int]:
    if not memory:
        with open("input_2017/day6.txt", "r") as input:
            memory = list(map(int, input.readline().split()))

    memory, part1 = day6_reallocate(memory)
    memory, part2 = day6_reallocate(memory)

    return {"part1": part1, "part2": part2}


def day5_part2(jumps: List[int] = None) -> int:
    if not jumps:
        with open("input_2017/day5.txt", "r") as input:
            jumps = list(map(int, input))

    pos = 0
    steps = 0
    while pos < len(jumps):
        jump_len = jumps[pos]
        if jump_len >= 3:
            jumps[pos] -= 1
        else:
            jumps[pos] += 1
        pos = pos + jump_len
        steps += 1
    return steps


def day5_part1(jumps: List[int] = None) -> int:
    if not jumps:
        with open("input_2017/day5.txt", "r") as input:
            jumps = list(map(int, input))
    pos = 0
    steps = 0
    while pos < len(jumps):
        jump_len = jumps[pos]
        jumps[pos] += 1
        pos = pos + jump_len
        steps += 1
    return steps


def day4_part2(phrases: List[str] = None) -> int:
    if not phrases:
        phrases = input("day4.txt")

    p2 = 0
    for p in phrases:
        p2_valid = True
        tokens = p.split(" ")
        q = list(map("".join, map(sorted, tokens)))
        for word in q:
            r = q[:]
            r.remove(word)
            if word in r:
                p2_valid = False
                break
        if p2_valid:
            p2 += 1

    return p2


def day4_part1(phrases: List[str] = None) -> int:
    if not phrases:
        phrases = input("day4.txt")

    p1 = 0
    for p in phrases:
        p1_valid = True
        tokens = p.split(" ")
        for word in tokens:
            q = tokens[:]
            q.remove(word)
            if word in q:
                p1_valid = False
                break
        if p1_valid:
            p1 += 1

    return p1


def day3_part2(n: int = None) -> int:
    if not n:
        n = 347991

    s = np.full((100, 100), ".", dtype="U16")
    pos = (50, 50)
    s[pos] = 1
    count = 1
    d = "R"
    directions = ["R", "U", "L", "D", "R"]

    def move(p, d):
        if d == "R":
            new = (p[0], p[1] + 1)
        if d == "U":
            new = (p[0] - 1, p[1])
        if d == "L":
            new = (p[0], p[1] - 1)
        if d == "D":
            new = (p[0] + 1, p[1])

        return new

    def neighbors(point, maze):
        n = []
        for x in [point[0] - 1, point[0], point[0] + 1]:
            for y in [point[1] - 1, point[1], point[1] + 1]:
                if x >= 0 and x < maze.shape[0] and y >= 0 and y < maze.shape[1]:
                    n.append(maze[(x, y)])
                else:
                    n.append(".")
        n.remove(maze[point])

        return n

    while count < n:
        pos = move(pos, d)
        next_d = directions[directions.index(d) + 1]
        step = move(pos, next_d)
        if s[step] == ".":
            d = next_d

        ns = neighbors(pos, s)
        while "." in ns:
            ns.remove(".")
        count = sum(list(map(int, ns)))
        s[pos] = count

    return count


def day3_part1(n: int = None) -> int:
    if not n:
        n = 347991

    with decimal.localcontext() as ctx:
        ctx.rounding = decimal.ROUND_HALF_UP

        l = 0
        s = 1
        while s <= n:
            l += 1
            s += l * 2
        if s - n >= l:
            center = s - l - decimal.Decimal(l / 2).to_integral_value()
            side = 2 * l - 1
        else:
            center = s - decimal.Decimal(l / 2).to_integral_value()
            side = 2 * l

        rounds = (side - 1) / 4
        r = decimal.Decimal(rounds).to_integral_value(rounding=decimal.ROUND_CEILING)
        d = abs(n - center) + r

    return int(d)


def day2(sheet: List[List[int]] = None) -> Dict[str, int]:
    if not sheet:
        s = input("day2.txt")
        sheet: List[List[int]] = []
        for line in s:
            sheet.append(list(map(int, line.split("\t"))))

    p1 = 0
    p2 = 0

    for row in sheet:
        p1 += max(row) - min(row)
        for a in row:
            for b in row:
                if a % b == 0 and int(a / b) != 1:
                    p2 += int(a / b)

    return {"part1": p1, "part2": p2}


def day1(captcha: str = None) -> Dict[str, int]:
    if not captcha:
        captcha = input("day1.txt")[0]

    p1 = 0
    p2 = 0
    x = int(len(captcha) / 2)

    for i, d in enumerate(captcha):
        if d == captcha[i - 1]:
            p1 += int(d)
        if d == captcha[i - x]:
            p2 += int(d)

    return {"part1": p1, "part2": p2}
