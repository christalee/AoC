# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 6
# http://adventofcode.com/2016/day/6

# Problem: Given a list of strings, find the least common character in each column.

messages = open('day6_input', 'r')
final = ''

hwords = [y for x in messages for y in x.split()]

# Reformat from rows to columns
vwords = zip(*hwords)

for word in vwords:
    word = ''.join(word)
    counts = [(l, word.count(l)) for l in word]
    counts.sort(key=lambda l: l[1])
    final += counts[0][0]

print final