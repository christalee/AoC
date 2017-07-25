# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 3
# http://adventofcode.com/2016/day/3

# Problem: given a list of numbers, separate them into groups of 3 (down columns, not across rows). How many of these groups could be the sides of a triangle (a + b > c)?
triangles = open('day3_input', 'r')
count = 0
htri = []
vtri = []
i = 0

# Turn the input string into a list of numbers
for each in triangles:
    each = each.strip().split()
    htri.append(each)

# Group those numbers into sets of 3
while i < len(htri):
    vtri.append(zip(htri[i], htri[i+1], htri[i+2]))
    i += 3

# Check each ordering of each group for valid triangle lengths
for x in vtri:
    for each in x:
        a = int(each[0])
        b = int(each[1])
        c = int(each[2])
        t = [a, b, c]

        if (a == max(t) and (b + c > a)) or (b == max(t) and (c + a > b)) or (c == max(t) and (a + b > c)):
            count += 1
    
print count