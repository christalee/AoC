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

idsum = 0
realnames = []

# Start with each room name in a list of strings
r = [y for x in rooms for y in x.split()]

for x in r:
    # Split each name into the [checksum], the sector ID, and the name, stripping out dashes
    parts = x.partition('[')
    checksum = parts[2].strip(']')
    rest = parts[0].rsplit('-', 1)
    sectorid = rest[1]
    name = rest[0].replace('-', '')
    
    # Alphabetize and deduplicate name into one string
    t = ''.join(sorted(set(name)))
    
    # Make a list of how often each letter appears in name
    counts = [(l, name.count(l)) for l in t]
    counts.sort(key=lambda l: l[1], reverse=True)
    
    # Take the 5 most common letters to compare to the checksum
    letters = ''.join([x[0] for x in counts[:5]])

# Part 2: Decrypt each room name by shifting each letter forward by the sector ID. Dashes become spaces. What is the sector ID of the room containing North Pole objects?

    if letters == checksum:
        ptext = []
        # string constant holding the alphabet
        a = string.ascii_lowercase
        
        for each in rest[0]:
            if each.isalpha():
                # find the current position of the letter
                cindex = a.index(each)
                # shift each letter mod 26
                ptext.append(a[(cindex + int(sectorid)) % 26])
            else:
                # convert dashes to spaces
                ptext.append(' ')
                
        realname = ''.join(ptext)
        if 'north' in realname:
            print realname, sectorid