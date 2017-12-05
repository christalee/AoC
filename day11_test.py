import copy

# store each item as a dictionary? label floors with strings or in variables?
# F1 = {'TmG': {'element': 'Tm', 'type': 'G'}, }

state = {
    4: [], 
    3: [('Pr','G'), ('Pr','M'), ('Ru','G'), ('Ru','M')], 
    2: [('Pu','M'), ('Sr','M')],
    1: [('Tm','G'), ('Tm','M'), ('Pu','G'), ('Sr','G')],
    'E': 1
}

# change this to be just lists?
state = {
    '4': [], 
    '3': [('Li','G')], 
    '2': [('H','G')],
    '1': [('H','M'), ('Li','M')],
    'E': [2]
}

moves = 0

statedict = {str(state): moves}

# given a state s, returns a list of reachable states ms
def nextmoves(s):
    ms = []
    for each in s:
        location = each['E'][0]
        up = location + 1
        down = location - 1
    # Elevator can move 1 or 2 items in location, to either of the nextlocations.
        x = copy.deepcopy(s)
        x[str(location)].remove()
        for item in things:
        
        
        
        
        
        
        # currently only moves 1 item. How to move two? "choose any two?"
#        moveUp = transfer(s, item, str(location + 1))
#        moveDown = transfer(s, item, str(location -1))
#        moves.extend([moveUp, moveDown])
    return ms

# don't need this?
def transfer(s, item, floor):
    # need to make copies, not modify s itself
    for each in s:
        if item in s[each]:
            s[each].remove(item)
    s[floor].append(item)
    return s

def isValid(s):
    location = str(s['E'][0])
    
    # the floor is empty
    if len(s[location]) == 0:
        return True

    for x in s[location]:
        element = x[0]
        component = x[1]
        tx = []
        for y in s[location]:
            ty = []
            if element == y[0]:
                ty.append[True]
        # Need to revisit all this logic: is this the best way to track what combinations are ok?
        if t == [True, True]:
            return True
        else:
            return False