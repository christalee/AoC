# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 9
# http://adventofcode.com/2016/day/9

# Part 1: You need to decompress a file containing compressed data. Compression markers are contained in parentheses. (10x2) means to take the next 10 characters and insert them 2 times, then continue reading forward. Ignore whitespace and do not include the marker itself in the decompressed text to insert. However, parentheses and other special characters may appear in inserted text without denoting a compression marker. What is the length of your decompressed file?

# Examples:
# ADVENT -> ADVENT with length 6.
# A(1x5)BC -> ABBBBBC with length 7.
# (3x3)XYZ -> XYZXYZXYZ with length 9.
# A(2x2)BCD(2x2)EFG -> ABCBCDEFEFG with length 11.
# (6x1)(1x3)A -> (1x3)A with length 6.
# X(8x2)(3x3)ABCY -> X(3x3)ABC(3x3)ABCY with length 18.

compressed = open('day9_input', 'r')
data = []
decompressed = 0

for each in compressed:
    data.append(each.strip())

# Start at the beginning of the string. Find the first '('. Partition at the first ')'after that. Extract the rlen and rx from [0], and slice out s = [2][0:rlen]. Build up uncompressed by adding rx*s. Recurse? on the string after the slice.

def expand(s, d):
    if s.startswith('('):
        if len(s) == 1:
            return d
        else:
            x = s.partition(')')
            marker = x[0].strip('(').split('x')
            rlen = int(marker[0])
            rx = int(marker[1])
            repstr = x[2][0:rlen]
#            d += repstr*rx
            return expand(repstr*rx + x[2][rlen:], d)
    else:
        x = s.partition('(')
        d += len(x[0])
        return expand('(' + x[2], d)

# Part 2: Turns out you need to expand markers within inserted text after all. What is the decompressed length of your file?

# Examples:
# (3x3)XYZ -> XYZXYZXYZ
# X(8x2)(3x3)ABCY -> X(3x3)ABC(3x3)ABCY -> XABCABCABCABCABCABCY
# (27x12)(20x12)(13x14)(7x10)(1x12)A -> A repeated 241920 times
# (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445 characters long.

# Switch from recursion to iteration. Can this be optimized??

def expand2(s, d):
    i = 0
    while len(s) > 1:
        if s.startswith('('):
            x = s.partition(')')
            marker = x[0].strip('(').split('x')
            rlen = int(marker[0])
            rx = int(marker[1])
            repstr = x[2][0:rlen]
            s = repstr*rx + x[2][rlen:]
        else:
            x = s.partition('(')
            d += len(x[0])
            s = '(' + x[2]
        i += 1
        if i % 10000 == 0:
            print d, len(s)
    
    return d, i
    
print expand2(data[0], decompressed)