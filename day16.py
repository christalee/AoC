# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 16
# http://adventofcode.com/2016/day/16

# Problem: you need to generate random data to fill a disk and calculate its checksum. Given an initial seed value, you generate data this way:
    #
    # Call the data you have at this point "a".
    # Make a copy of "a"; call this copy "b".
    # Reverse the order of the characters in "b".
    # In "b", replace all instances of 0 with 1 and all 1s with 0.
    # The resulting data is "a", then a single 0, then "b".

disk = 35651584
seed = '11100010111110100'

binswap = {'0': '1', '1': '0'}

def datagen(a):
    b = a[::-1]
    b = b.translate(str.maketrans(binswap))
    return a + '0' + b

# Repeat until you have enough data to fill the disk; discard any extra data. 
while len(seed) < disk:
    seed = datagen(seed)

seed = seed[0:disk]

# Once you have enough, calculate the checksum this way:

# Break the data into pairs.
# If the pair is two identical digits (11 or 00), the checksum digit is 1. If not (01 or 10), it's 0. 
# The result should be half the length of the initial data. If the length of the checksum is even, calculate its checksum. 
# Repeat until you have a checksum with an odd length.

def checksum(a):
    pairs = [a[x] + a[x+1] for x in range(0, len(a), 2)]
    check = ''
    for each in pairs:
        if each[0] == each[1]:
            check += '1'
        else:
            check += '0'
    if len(check) % 2 == 0:
        checksum(check)
    else:
        print(check, len(check))
        
checksum(seed)