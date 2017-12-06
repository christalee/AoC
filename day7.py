# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 7
# http://adventofcode.com/2016/day/7

# Part 1: Strings are valid if they contain a 4 character palindrome (e.g. abba, smms), unless the palindrome is inside square brackets or the characters are all the same (e.g. nnnn). How many of the given strings are valid?

# Examples (make these tests?):
# abba[mnop]qrst is valid
# abcd[bddb]xyyx is invalid
# aaaa[qwer]tyui is invalid
# ioxxoj[asdfgh]zxcvbn is valid

addresses = open('day7_input', 'r')
count = 0

ips = [x.strip() for x in addresses]

# Given a string, test each set of 4 consecutive characters for palindromes
# Return True if any 4 are valid, otherwise False
def abba(s):
    tf = [(s[i] == s[i+1]) and (s[i-1] == s[i+2]) and (s[i] != s[i-1]) for i in range(1, len(s)-2)]
    return True in tf

for i in ips:
    outbs = []
    inbs = []

    # Split each string up by square brackets
    x = i.split(']')
    for y in x:
        if '[' in y:
            z = y.partition('[')
            if abba(z[0]):
                outbs.append(True)
            if abba(z[2]):
                inbs.append(True)
        # Check the last segment too
        elif abba(y):
            outbs.append(True)
    
    if True in outbs and True not in inbs:
        count += 1

print count

# Part 2: Strings are valid if they contain a 3 character palindrome (e.g. aba, sms) outside square brackets AND the corresponding inverse (e.g. sms -> msm) inside square brackets. 

# Examples: 
# aba[bab]xyz is valid
# xyx[xyx]xyx is invalid
# aaa[rur]uru is valid
# zazbz[bzb]cdb is valid

# Given a string, test each set of 3 consecutive characters for palindromes
# Return a list for further testing
def xyx(s):
    trigrams = [s[i-1:i+1] for i in range(1, len(s)-1) if (s[i-1] == s[i+1] and s[i] != s[i-1])]
    return trigrams

# Given two lists of strings, check each item of a for matchng any item in b
# NOTE: this checks the reverse of x against y; maybe rename this or reverse before passing into the fn? or when generating trigrams?

def matches(a, b):
    return True in [True for x in a for y in b if x[::-1] == y]

count = 0

for i in ips:
    outbs = []
    inbs = []
    
    # Split each string up by square brackets
    x = i.split(']')
    for y in x:
        if '[' in y:
            z = y.partition('[')
            # Collect valid trigrams found outside square brackets
            outbs.extend(xyx(z[0]))
            # Ditto, inside square brackets
            inbs.extend(xyx(z[2]))
        #what to do if '[' isn't found (last segment)
        else:
            outbs.extend(xyx(y))

    if matches(outbs, inbs):
        count += 1
        
print count