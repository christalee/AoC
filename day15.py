# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 15
# http://adventofcode.com/2016/day/15

# Problem: You have a machine of disks which rotate every second. You want to release a capsule at the top at the right time to pass through to the bottom. Each disk is 1s apart. Given the initial positions and number of positions on each disk, at what time should you release the capsule?

# Disc #1 has 13 positions; at time=0, it is at position 1.
# Disc #2 has 19 positions; at time=0, it is at position 10.
# Disc #3 has 3 positions; at time=0, it is at position 2.
# Disc #4 has 7 positions; at time=0, it is at position 1.
# Disc #5 has 5 positions; at time=0, it is at position 3.
# Disc #6 has 17 positions; at time=0, it is at position 5.
# Disc #7 has 11 positions; at time=0, it is at position 1.

# Track global time t. Code each disk's position mod the time. Update each position each reads 0 at the correct time.

t = 0

def check(time):
    while True:
        d1 = (1 + time + 1) % 13
        d2 = (10 + time + 2) % 19
        d3 = (2 + time + 3) % 3
        d4 = (1 + time + 4) % 7
        d5 = (3 + time + 5) % 5
        d6 = (5 + time + 6) % 17
        d7 = (0 + time + 7) % 11
        
        if d1 == d2 == d3 == d4 == d5 == d6 == d7 == 0:
            print time
            break
        
        if time % 10000 == 0:
            print time, d1, d2, d3, d4, d5, d6, d7
        
        time += 1

check(t)