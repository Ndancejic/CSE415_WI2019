'''Rubik2Cube.py
the visualized rubiks cube looks like this:
  center number represents index in overall array
  side corner number represents index of that face
     |---|
     |0|1|
     |-2-|
     |2|3|
-----|---|-----
|0|1||0|1||0|1|
|-4-||-0-||-5-|
|2|3||2|3||2|3|
-----|---|-----
     |0|1|
     |-3-|
     |2|3|
     |---|
     |0|1|
     |-1-|
     |2|3|
     |---|

'''
#<METADATA>
QUIET_VERSION = "0"
PROBLEM_NAME = "Rubik2Cube"
PROBLEM_VERSION = "0"
PROBLEM_AUTHORS = ['Nikola Dancejic']
PROBLEM_CREATION_DATE = "1-FEB-2019"
PROBLEM_DESC=\
'''
This is a formulation of the 2x2x2 Rubiks Cube
'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
# #Indecies of four blocks
# UL = 0;
# UR = 1;
# LL = 2;
# LR = 3;
# never used

#indecies of sides
F = 0;
B = 1;
U = 2;
D = 3;
L = 4;
R = 5;

class State:
  def __init__(self, b):
    self.b = b

  def __eq__(self,s2):
    for i in range(6):
      for j in range(4):
        if self.b[i][j] != s2.b[i][j]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    return str(self.b)

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    news.b = [row[:] for row in self.b]
    return news

  def can_move(self,dir):
    #all moves ok
    return True

  #I need to check these moves
  def move(self,dir):
    '''Assuming it's legal to make the move, this computes
       the new state resulting from moving a tile in the
       given direction clockwise.'''
    news = self.copy() # start with a deep copy.
    b = news.b
    if dir=='F':
      temp = b[F][0]
      b[F][0] = b[F][2]
      b[F][2] = b[F][3]
      b[F][3] = b[F][1]
      b[F][1] = temp
      temp1 = b[U][2]
      temp2 = b[U][3]
      b[U][2] = b[L][3] 
      b[U][3] = b[L][1]
      b[L][3] = b[D][1] 
      b[L][1] = b[D][0]
      b[D][1] = b[R][0] 
      b[D][0] = b[R][2]
      b[R][0] = temp1
      b[R][2] = temp2
    if dir=='B':
      temp = b[B][0]
      b[B][0] = b[B][2]
      b[B][2] = b[B][3]
      b[B][3] = b[B][1]
      b[B][1] = temp
      temp1 = b[D][2]
      temp2 = b[D][3]
      b[D][2] = b[L][0] 
      b[D][3] = b[L][2]
      b[L][0] = b[U][1] 
      b[L][2] = b[U][0]
      b[U][1] = b[R][3] 
      b[U][0] = b[R][1]
      b[R][3] = temp1
      b[R][1] = temp2
    if dir=='U':
      temp = b[U][0]
      b[U][0] = b[U][2]
      b[U][2] = b[U][3]
      b[U][3] = b[U][1]
      b[U][1] = temp
      temp1 = b[B][2]
      temp2 = b[B][3]
      b[B][2] = b[L][1] 
      b[B][3] = b[L][0]
      b[L][1] = b[F][1] 
      b[L][0] = b[F][0]
      b[F][1] = b[R][1] 
      b[F][0] = b[R][0]
      b[R][1] = temp1
      b[R][0] = temp2
    if dir=='D':
      temp = b[D][0]
      b[D][0] = b[D][2]
      b[D][2] = b[D][3]
      b[D][3] = b[D][1]
      b[D][1] = temp
      temp1 = b[F][2]
      temp2 = b[F][3]
      b[F][2] = b[L][2] 
      b[F][3] = b[L][3]
      b[L][2] = b[B][1] 
      b[L][3] = b[B][0]
      b[B][1] = b[R][2] 
      b[B][0] = b[R][3]
      b[R][2] = temp1
      b[R][3] = temp2
    if dir=='L':
      temp = b[L][0]
      b[L][0] = b[L][2]
      b[L][2] = b[L][3]
      b[L][3] = b[L][1]
      b[L][1] = temp
      temp1 = b[U][0]
      temp2 = b[U][2]
      b[U][0] = b[B][0] 
      b[U][2] = b[B][2]
      b[B][0] = b[D][0] 
      b[B][2] = b[D][2]
      b[D][0] = b[F][0] 
      b[D][2] = b[F][2]
      b[F][0] = temp1
      b[F][2] = temp2
    if dir=='R':
      temp = b[R][0]
      b[R][0] = b[R][2]
      b[R][2] = b[R][3]
      b[R][3] = b[R][1]
      b[R][1] = temp
      temp1 = b[U][3]
      temp2 = b[U][1]
      b[U][3] = b[F][3] 
      b[U][1] = b[F][1]
      b[F][3] = b[D][3] 
      b[F][1] = b[D][1]
      b[D][3] = b[B][3] 
      b[D][1] = b[B][1]
      b[B][3] = temp1
      b[B][1] = temp2
    return news # return new state

  def edge_distance(self, s2):
    return 1.0  # Warning, this is only correct when
    # self and s2 are neighboring states.
    # We assume that is the case.  This method is
    # provided so that problems having all move costs equal to
    # don't have to be handled as a special case in the algorithms.
  
def goal_test(s):
  '''If all the sides have a single color, it is the goal state'''
  for i in range(6):
    color = s.b[i][0]
    for j in range(1,4):
      tempcolor = s.b[i][j]
      if color != tempcolor:
        return False
  return True

def goal_message(s):
  return "You solved it!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
  # Use default, but override if new value supplied
             # by the user on the command line.
try:
  import sys
  init_state_string = sys.argv[2]
  print("Initial state as given on the command line: "+init_state_string)
  init_state_list = eval(init_state_string)
except:
  ''' one solution state
        [['R', 'R', 'R', 'R'], ['O', 'O', 'O', 'O'],
        ['G', 'G', 'G', 'G'], ['B', 'B', 'B', 'B'],
        ['Y', 'Y', 'Y', 'Y'], ['W', 'W', 'W', 'W']]
  '''

  ''' 3-Step initial State
      [['RED', 'BLUE', 'RED', 'BLUE'], ['ORANGE', 'GREEN', 'ORANGE', 'GREEN'],
      ['GREEN', 'RED', 'GREEN', 'RED'], ['BLUE', 'ORANGE', 'BLUE', 'ORANGE'],
      ['YELLOW', 'YELLOW', 'YELLOW', 'YELLOW'], ['WHITE', 'WHITE', 'WHITE', 'WHITE']]
  '''

  ''' too hard to complete
      [['ORANGE', 'WHITE', 'RED', 'BLUE'], ['BLUE', 'RED', 'GREEN', 'BLUE'],
      ['WHITE', 'ORANGE', 'YELLOW', 'GREEN'], ['WHITE', 'RED', 'YELLOW', 'YELLOW'],
      ['RED', 'GREEN', 'ORANGE', 'BLUE'], ['ORANGE', 'WHITE', 'YELLOW', 'GREEN'],]
  '''

  ''' 1-Step 1-Solution
      [['RED', 'GREEN', 'RED', 'GREEN'], ['ORANGE', 'BLUE', 'ORANGE', 'BLUE'],
      ['GREEN', 'ORANGE', 'GREEN', 'ORANGE'], ['BLUE', 'RED', 'BLUE', 'RED'],
      ['YELLOW', 'YELLOW', 'YELLOW', 'YELLOW'], ['WHITE', 'WHITE', 'WHITE', 'WHITE']]
  '''

  ''' 2-Step 1-Solution
      [['BLUE', 'BLUE', 'RED', 'RED'], ['ORANGE', 'GREEN', 'ORANGE', 'GREEN'],
      ['BLUE', 'ORANGE', 'WHITE', 'WHITE'], ['YELLOW', 'YELLOW', 'GREEN', 'RED'],
      ['YELLOW', 'ORANGE', 'YELLOW', 'BLUE'], ['RED', 'WHITE', 'GREEN', 'WHITE']]
  '''

  ''' 3-Step Initial State
      [['YELLOW', 'YELLOW', 'ORANGE', 'GREEN'], ['WHITE', 'WHITE', 'BLUE', 'RED'],
      ['ORANGE', 'BLUE', 'RED', 'RED'], ['BLUE', 'ORANGE', 'GREEN', 'GREEN'],
      ['YELLOW', 'GREEN', 'RED', 'WHITE'], ['BLUE', 'WHITE', 'YELLOW', 'ORANGE']]
  '''
  
  init_state_list = [['R', 'B', 'R', 'B'], ['O', 'G', 'O', 'G'],
      ['G', 'R', 'G', 'R'], ['B', 'O', 'B', 'O'],
      ['Y', 'Y', 'Y', 'Y'], ['W', 'W', 'W', 'W']]
  print("Using default initial state list: "+str(init_state_list))

CREATE_INITIAL_STATE = lambda: State(init_state_list)
#</INITIAL_STATE>

#<OPERATORS>
directions = ['F','B','U','D','L','R']
OPERATORS = [Operator("Rotate "+str(dir)+" clockwise",
                      lambda s,dir1=dir: s.can_move(dir1),
                      # The default value construct is needed
                      # here to capture the value of dir
                      # in each iteration of the list comp. iteration.
                      lambda s,dir1=dir: s.move(dir1) )
             for dir in directions]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

