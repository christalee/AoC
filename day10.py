# Christalee Bieber, 2017
# cbieber@alum.mit.edu

# Advent of Code 2016, Day 10
# http://adventofcode.com/2016/day/10

# Part 1: You have instructions for a system of numbered bots that take in numbers, compare them, and deposit them into output bins. Bots don't take any action until they have two numbers to compare. Which bot compares 61 to 17?

# Example:
# value 5 goes to bot 2
# bot 2 gives low to bot 1 and high to bot 0
# value 3 goes to bot 1
# bot 1 gives low to output 1 and high to bot 0
# bot 0 gives low to output 2 and high to output 0
# value 2 goes to bot 2

# Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a value-2 chip and a value-5 chip.
# Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and its higher one (5) to bot 0.
# Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and gives the value-3 chip to bot 0.
# Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in output 0.


instructions = open('day10_input', 'r')
commands = [x.strip() for x in instructions]
bots = {}
outputs = {}

# Brainstorming
# For each command, I need to parse whether it's a input value or a bot output. How should I represent bots and output bins? Maybe a list, ('bot 92', 'low', 'high'). Will it work to parse out all the input values and then run all the bot outputs? Or do I have to run through the list (recursively?) checking for bots that have 2 values and activating them?
# When I'm done, how will I know which bot I'm looking for? How will I know I'm done?

# Refactor this all into multiple functions and then one main loop that calls them in succession?

def botlist():
    for c in commands:
        x = c.split()
        
        # Define each bot as a dictionary with two values, initialized False, and destinations for its high and low values
        if x[0] == 'bot':
            bots[(x[0]+x[1])] = {'v0': False, 'v1': False, 'lowdest': x[5]+x[6], 'highdest': x[10]+x[11]}
        # As you parse commands, also create dictionaries for each output bin
        if x[5] == 'output':
            bots[(x[5]+x[6])] = {'value': False}
        if len(x) > 6 and x[10] == 'output':
            bots[(x[10]+x[11])] = {'value': False}

# Next, populate each bot with its initial values
# Can this be merged with the previous function??
def valrun():
    for c in commands:
        x = c.split()
        if x[0] == 'value':
            bcompare(bots[(x[4]+x[5])], int(x[1]))

# Given a bot or bin, deposit the number in one of the bot's slots or the bin.
def bcompare(bot, x):
    if 'value' in bot.keys():
        bot['value'] = x
    elif bot['v0']:
        bot['v1'] = x
    else:
        bot['v0'] = x

# If a bot has both values, compare & send them to lowdest and highdest and reset them to False
def botrun():
    for k, b in bots.iteritems():
        if ('v0' in b.keys()) and b['v0'] and b['v1']:
            bcompare(bots[b['lowdest']], min(b['v0'], b['v1']))
            bcompare(bots[b['highdest']], max(b['v0'], b['v1']))
            b['v0'] = False
            b['v1'] = False

# 500 runs turns out to be sufficient to reach steady state.
botlist()
valrun()
for i in range(500):
    botrun()

# Part 2: What is the product of the numbers in bins 0, 1, and 2?

r = bots['output0']['value'] * bots['output1']['value'] * bots['output2']['value']
print r