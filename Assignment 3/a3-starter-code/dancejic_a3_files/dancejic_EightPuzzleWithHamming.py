'''
Nikola Dancejic
dancejic
dancejic_EightPuzzleWithHamming.py

This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
The particular heuristic is hamming
'''

from EightPuzzle import *

def h(s):
  '''return the amount of tiles out of place'''
  count = 0
  for i in range(3):
    for j in range(3):
      if s.b[i][j] != 3*i + j:
        if s.b[i][j] != 0:
          count += 1
  return count
