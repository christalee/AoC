# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 12
# http://adventofcode.com/2016/day/12

# Part 1: You are given a set of assembly instructions, operating on 4 registers initialized to 0. What value does register a hold when the instructions terminate?

# Part 2: What value does register a hold if register c is initialized to 1?

# Commands:
# 'cpy x y' copies x (either an integer or the value of a register) into register y.
# 'inc x' increases the value of register x by one.
# 'dec x' decreases the value of register x by one.
# 'jnz x y' jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.

instructions = open('day12_input', 'r')
commands = [x.strip() for x in instructions]
        
reg = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
i = 0

# Instructions are followed in order from the beginning until no more remain; use i to track progress through the list
while i < len(commands):
    c = commands[i].split(' ')
    if c[0] == 'cpy':
        if c[1] in reg.keys():
            reg[c[2]] = reg[c[1]]
        else:
            reg[c[2]] = int(c[1])
        i += 1
    if c[0] == 'inc':
        reg[c[1]] += 1
        i += 1
    if c[0] == 'dec':
        reg[c[1]] -= 1
        i += 1
    if c[0] == 'jnz':
        if c[1] in reg.keys():
            if not reg[c[1]] == 0:
                i += int(c[2])
            else:
                i += 1
        elif not int(c[1]) == 0:
            i += int(c[2])
        else:
            i += 1

print reg