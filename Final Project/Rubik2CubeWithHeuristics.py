'''
Nikola Dancejic
dancejic
dancejic_EightPuzzleWithHamming.py

This file augments Rubik2Cube.py with heuristic information,
so that it can be used by an A* implementation.
The particular heuristic is my heuristic
'''

from Rubik2Cube import *
#import statistics

OPPOSITES = {'GREEN':'BLUE',
             'BLUE':'GREEN',
             'YELLOW':'WHITE',
             'RED':'ORANGE',
             'WHITE':'YELLOW',
             'ORANGE':'RED'}

def h(s):
  '''We return the amount of tiles that are not opposites on the other side'''
  count = 0
  for i in range(0,6,2):
    for j in range(4):
      color = s.b[i][j]
      for k in range(0,4):
        if color != OPPOSITES[s.b[i+1][k]]:
          count += 1
  return count

