# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 14
# http://adventofcode.com/2016/day/14

# Problem: You are looking for 64 one-time pad keys. To find each key, determine the md5 hash of your input salt with an index that starts at 0 and increases each time. A key is valid if the lowercase hexadecimal representation of the md5 result contains 3 characters in a row AND a hash containing the same characters 5 times in a row occurs in the next 1000 hashes.

import hashlib, pprint

salt = 'zpqevtbw'
hashes = {}
keys = {}
h = '0123456789abcdef'

for x in range(500000):
    m = hashlib.md5()
    m.update(salt + str(x))
    hashes[x] = m.hexdigest().lower()
        
while len(keys) < 64:
    for i in range(len(hashes) - 1000):
        for j in range(i+1, i+1001):
            for x in h:
                if x*3 in hashes[i] and x*5 in hashes[j]:
                    keys[i] = [hashes[i], hashes[j], j]
                    break

pprint.pprint(keys)