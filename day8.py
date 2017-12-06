# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 8
# http://adventofcode.com/2016/day/8

# Part 1: You are given a set of commands to execute on a screen 50 px wide by 6 px tall, which starts entirely off. How many pixels turn on?

# Commands: 

# 'rect AxB' turns on all of the pixels in a rectangle A px wide by B px tall at the top-left of the screen.

# 'rotate row y=A by B' shifts all of the pixels in row A (0 is the top row) right by B px. Pixels that would fall off the right end appear at the left end of the row.

# 'rotate column x=A by B' shifts all of the pixels in column A (0 is the left column) down by B px. Pixels that would fall off the bottom appear at the top of the column.

# numpy handles arrays well, let's use it here
import numpy as np

# numpy arrays index as (# of rows, # of cols)
screen = np.zeros((6, 50), dtype=int)

# Given the dimensions of the rectangle as a string 'AxB', turn on those pixels
def rect(r):
    r = r.split('x')
    screen[0:int(r[1]), 0:int(r[0])] = 1

# Given the row/column index and shift amount, use numpy.roll to modify screen
def rotate(rowcol, index, shift):
    i = int(index.split('=')[-1])
    if rowcol == "row":
        screen[i, :] = np.roll(screen[i, :], int(shift))
    if rowcol == "column":
        screen[:, i] = np.roll(screen[:, i], int(shift))
    
instructions = open('day8_input', 'r')
ops = [x.strip() for x in instructions]

for each in ops:
    r = each.split()
    if r[0] == "rect":
        rect(r[1])
    if r[0] == "rotate":
        rotate(r[1], r[2], r[4])

print np.sum(screen)

# Part 2: The screen displays letters as capital letters 5 px wide. What code is displayed?

# read straight off the terminal
for x in range(0, screen.shape[1], 5):
    print screen[:, x:x+5]