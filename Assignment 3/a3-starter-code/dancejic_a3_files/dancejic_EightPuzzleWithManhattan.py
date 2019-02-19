'''
Nikola Dancejic
dancejic
dancejic_EightPuzzleWithManhattan.py

This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
The particular heuristic is Manhattan
'''

from EightPuzzle import *

POSITIONS = {0:[0,0], 1:[0,1], 2:[0,2], 3:[1,0], 4:[1,1], 5:[1,2], 6:[2,0], 7:[2,1], 8:[2,2]}

def h(s):
  '''returns the distance that tiles are out of place'''
  count = 0
  for i in range(3):
    for j in range(3):
      num = s.b[i][j]
      #iy = num/3
      #jy = num%3
      if num != 0:
        count += abs(POSITIONS[num][0]-i) + abs(POSITIONS[num][1]-j)
  return count


# A simple test:
#print(h('Nantes'))
