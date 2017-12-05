# Christalee Bieber, 2017
# cbieber@alum.mit.edu
# http://adventofcode.com/2016/day/18

# Problem: You face a room with 40 rows of tiles, some of which are safe (.) and some are traps (^). Given the layout of the first row, you can determine the layout of the next row by following the rules below. 

# Rules:
# For each tile, look at the tile in the prior row and the two adjacent to that tile. Call these tiles the left, center, and right tiles. A new tile is a trap if:
#   - The left and center tiles are traps, but the right tile is not.
#   - The center and right tiles are traps, but the left tile is not.
#   - Only the left tile is a trap.
#   - Only the right tile is a trap.
# The wall (end of each row) counts as safe; any tile that is not a trap per these rules is safe.

# Part 1: How many safe tiles are in this room?