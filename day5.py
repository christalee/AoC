# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 5
# http://adventofcode.com/2016/day/5

# Problem: You are looking for an 8 character password. To find each character, determine the md5 hash of your input with an index that starts at 0 and increases each time. If the hexadecimal representation of the md5 result begins with 5 zeroes, the 7th digit is added to the password in the position given by the 6th digit. Only the first character found for each position is used, discard the rest.

import hashlib

doorid = 'abbhdwsy'
i = 0
password = ['_'] * 8

# Run this loop until the password has changed from symbols to alphanumerics
while not ''.join(password).isalnum():
    m = hashlib.md5()
    m.update(doorid + str(i))
    if m.hexdigest()[:5] == '00000' and m.hexdigest()[5].isdigit():
        position = int(m.hexdigest()[5])
        if position < 8 and password[position] == '_':
            password[position] = m.hexdigest()[6]
    i += 1

print ''.join(password)
