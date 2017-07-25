# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 4
# http://adventofcode.com/2016/day/4

# Part 1: You are given a list of rooms formatted as a name (lowercase letters separated by dashes) followed by a dash, a sector ID, and a checksum in square brackets. A room name is valid if the checksum is the five most common letters in the encrypted name, in order, with ties broken by alphabetization. What is the sum of the sector IDs for all the valid rooms?

# Examples (make these tests?):
# aaaaa-bbb-z-y-x-123[abxyz] is valid
# a-b-c-d-e-f-g-h-987[abcde] is valid
# not-a-real-room-404[oarel] is valid
# totally-real-room-200[decoy] is invalid


import string

rooms = open('day4_input', 'r')

r = []
idsum = 0
realnames = []

# Start with each room name in a list of strings
for each in rooms:
    r.append(each.strip())

for x in r:
    # Split each name into the [checksum], the sector ID, and the name, stripping out dashes
    parts = x.partition('[')
    checksum = parts[2].strip(']')
    rest = parts[0].rsplit('-', 1)
    sectorid = rest[1]
    name = rest[0].replace('-', '')
    t = ''.join(sorted(set(name)))      # Alphabetize and deduplicate name into one string
    
    # Make a list of how often each letter appears in name
    counts = []
    for l in t:
        counts.append((l, name.count(l)))
    counts.sort(key=lambda l: l[1], reverse=True)
    letters = ''.join([x[0] for x in counts[:5]])   # Take the 5 most common letters to compare to the checksum

# Part 2: Decrypt each room name by shifting each letter forward by the sector ID. Dashes become spaces. What is the sector ID of the room containing North Pole objects?

    if letters == checksum:
        ptext = []
        a = string.ascii_lowercase                              # string constant holding the alphabet
        for each in rest[0]:
            if each.isalpha():
                cindex = a.index(each)                          # find the current position of the letter
                ptext.append(a[(cindex + int(sectorid)) % 26])  # shift each letter mod 26
            else:
                ptext.append(' ')                               # convert dashes to spaces
                
        realname = ''.join(ptext)
        if 'north' in realname:
            print realname, sectorid