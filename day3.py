# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 3
# http://adventofcode.com/2016/day/3

# Problem: given a list of numbers, separate them into groups of 3 (down columns, not across rows). How many of these groups could be the sides of a triangle (a + b > c)?
triangles = open('day3_input', 'r')
count = 0
i = 0

# Turn the input string into a list of numbers
htri = [x.split() for x in triangles]

# Group those numbers into sets of 3
i = range(0, len(htri), 3)
vtri = [y for x in i for y in zip(htri[x], htri[x+1], htri[x+2])]

# Check each ordering of each group for valid triangle lengths
for x in vtri:
    t = [int(each) for each in x]
    a, b, c = t

    if (a == max(t) and (b + c > a)) or (b == max(t) and (c + a > b)) or (c == max(t) and (a + b > c)):
        count += 1
    
print count