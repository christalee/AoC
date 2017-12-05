import copy

# represent state as a list with 2 elements, representing each side of the river. Items: Boat, Chicken, Fox, Wheat (alphabetical)
state = [[["B", "C", "F", "W"], [""]]]
moves = 0
paths = {str(state): moves}

# next moves: from the side containing B, can take 0 or 1 item to the other side
# invalid moves: anything that leaves the C with the W, or the F with the C

def nextmoves(s):
    # takes a state s, and returns a list of states m
    m = []
    for each in s:
        if "B" in each:
            origin = s.index(each)
            destination = origin - 1
            # first, just move the boat without anything in it
            x = copy.deepcopy(s)
            x[origin].remove("B")
            x[origin].sort()
            x[destination].append("B")
            x[destination].sort()
            m.append(x)
            
            # next, move each item on the boat's original side to the other side
            # note: you already moved the boat, so you don't have to do it again
            for i in x[origin]:
                y = copy.deepcopy(x)
                y[origin].remove(i)
                y[origin].sort()
                y[destination].append(i)
                y[destination].sort()
                m.append(y)
    return m
            
def isvalid(s):
    # takes a state s, returns whether it is a permissible state or not
    for each in s:
        if ("B" not in each) and ("C" in each) and (("W" in each) or ("F" in each)):
            return False
        else:
            return True

# given a list of states s, generate all the possible next moves
# if each next move is valid and it's not already in the path dict, add it along with the # of moves
# repeat using the items of the path dict with value moves + 1

# keep a list version of the state in s (pass it in as a parameter?) and put a string version into paths

def iterstate(ss, p, m):
    while True:
        ts = []
        m += 1
        if ss == []:
            return p
        for x in ss:
            for y in nextmoves(x):
                if y == [[""], ["B", "C", "F", "W"]]:
                    return y, m
                if isvalid(y) and (str(y) not in p):
                    ts.append(y)
                    p[str(y)] = m
        ss = ts

print iterstate(state, paths, moves)
