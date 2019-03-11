'''
Nikola Dacejic
dancejic
Rubik2CubeWithHamming.py

This file augments Rubik2Cube.py with heuristic information,
so that it can be used by an A* implementation.
The particular heuristic is hamming
'''

from Rubik2Cube import *

#the opposites of each color
OPPOSITES = {'GREEN':'BLUE',
             'BLUE':'GREEN',
             'YELLOW':'WHITE',
             'RED':'ORANGE',
             'WHITE':'YELLOW',
             'ORANGE':'RED'}

def h(s):
  '''We return the amount of tiles out of place'''
  count = 0
  F_color = s.b[0][0]
  B_color = OPPOSITES[F_color]
  U_color = s.b[2][2]
  D_color = OPPOSITES[U_color]
  L_color = s.b[4][1]
  R_color = OPPOSITES[L_color]
  #in the front
  for j in range(1,4):
    if s.b[F][j] != F_color:
      count += 1
  #in the back...etc..
  for j in range(1,4):
    if s.b[B][j] != B_color:
      count += 1
  for j in range(1,4):
    if s.b[U][j] != U_color:
      count += 1
  for j in range(1,4):
    if s.b[D][j] != D_color:
      count += 1
  for j in range(1,4):
    if s.b[L][j] != L_color:
      count += 1
  for j in range(1,4):
    if s.b[R][j] != R_color:
      count += 1
  '''
  for i in range(6):
    color = s.b[i][0]
    for j in range(1,4):
      tempcolor = s.b[i][j]
      if color != tempcolor:
        count += 1'''
  return count


# A simple test:
#print(h('Nantes'))
