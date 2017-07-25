# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 6
# http://adventofcode.com/2016/day/6

# Problem: Given a list of strings, find the least common character in each column.

messages = open('day6_input', 'r')
hwords = []
final = ''

for each in messages:
    hwords.append(each.strip())

# Reformat from rows to columns
vwords = zip(*hwords)

for word in vwords:
    counts = []
    word = ''.join(word)
    for l in word:
        counts.append((l, word.count(l)))
    counts.sort(key=lambda l: l[1])
    final += counts[0][0]

print final