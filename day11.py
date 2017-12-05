# Rules:
# 1. You and the elevator begin on F1.
# 2. At all times, each floor (+ elevator) can only contain all generators, all microchips, nothing, or a combination such that all microchips are with their generators. (A generator may hang out without its microchip.)
# 3. The elevator only moves one floor at a time.
# 4. The elevator will only move at least one and no more than two generators or microchips.
# 5. The goal is to get all microchips and generators (10) to F4.

# Strategy
# 0. Write a fn to evaluate if moves are valid.
# 1. state = [all floors + elevator] -> store in a list? after each move, or a dictionary where each state is a key?
# 2. Increment count carefully everytime a move is successfully made
# 3. Store each state in a tuple with its move count
# 4. For each state, increment the count, then locate the elevator, then check for valid moves among the elevator cargo and its floor -> one floor up or down.
# 5. Also write a move function to get things in and out of the elevator -> appended to the correct floor.
# 6. If a move is valid, execute it (make copies?). If the final state is not already in the dict of states, add it along with its count.
# 7. Do I need to sort things before I put them in the dict so they compare properly? what a headache.

import copy
# represent state as a list with 4 elements, representing each floor of the building.
# elements: thulium (Tm), plutonium (Pu), strontium (Sr), promethium (Pr), ruthenium (Ru)
# F4: 
# F3: PrG, PrM, RuG, RuM
# F2: PuM, SrM
# F1: TmG, TmM, PuG, SrG, E

state = [[["Tm.G", "Tm.M", "Pu.G", "Sr.G"], 
    ["Pu.M", "Sr.M"], 
    ["Pr.G", "Pr.M", "Ru.G", "Ru.M"], 
    [""]]]
elevator = 0
moves = 0
paths = {str(state): moves}


def onetwo(x):
    y = [([a,b] if (not a == b) and (a < b) else [a]) for a in x for b in x]
    return y

# next moves: find the elevator, take 1 or 2 items to the adjacent floors
# takes a state s [from the previous m], and returns a list of states m   
def nextmoves(s):
    m = []
    e = s[-1]
    lowdest = e - 1
    highdest = e + 1
    
    for item in onetwo(s[e]):
        if lowdest > 0:
            y = copy.deepcopy(s)
            for x in item:
                y[e].remove(x)
            y[lowdest].extend(item)
            m.append(y.append(lowdest))
                    
        if highdest < 5:
            y = copy.deepcopy(s)
            for x in item:
                y[e].remove(x)
            y[highdest].extend(item)
            m.append(y.append(highdest))
    return m


def isvalid(s):
    e = s.pop()
    for a in s[e][:]:
        a = a.partition(".")
        if a[2] == "M" and 

# Code below here needs to be rewritten
#
# # For a given state, determine whether it violates any of the rules above, returning True or False accordingly. (Create a list of T/F tests and make sure all are T? Or is that clumsy?)
# # invalid moves: anything that leaves a microchip without its corresponding generator
# def isValid(s):
#     location = s['E']
#
#     # the floor is empty
#     if len(s[location]) == 0:
#         return True
#
#     for x in s[location]:
#         element = x[0]
#         component = x[1]
#         tx = []
#         for y in s[location]:
#             ty = []
#             if element == y[0]:
#                 ty.append[True]
#         # Need to revisit all this logic: is this the best way to track what combinations are ok?
#         if t == [True, True]:
#             return True
#         else:
#             return False
#
#
#
# while len(state['F4']) < 10:
#     # generate a list of possible next states
#     n = nextStates(state)
#     # add valid states + move count to statedict
#     for each in n:
#         if isValid(each):
#             if str(each) not in statedict:
#                 statedict[str(each)] = count
#             # TODO need to figure out how to represent states as keys; maybe write a function for it?
#
#     count += 1
#     # recurse on all valid states? what does count do on recursion?
#
# # at the end, print the first state where all items are on F4? use that to look up its count in the dictionary? or just print count directly?
# print statedict
# print count