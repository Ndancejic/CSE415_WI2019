'''FarmerFox
'''

#METADATA
PROBLEM_NAME = "Farmer Fox"
PROBLEM_VERSION = "0"
PROBLEM_AUTHOR = "Nikola Dancejic"
PROBLEM_CREATION_DATE = "23-JAN-2018"
PROBLEM_DESC =\
            '''
            Get the Farmer, Fox, Chicken, and Grains across the river without
            leaving the Fox and Chicken or the Chicken and Grain together
            '''

#COMMON_DATA
river = ['left','right']
bad_move = {'f':'C', 'C':'G', 'C':'f', 'G':'C'}
#COMMON_CODE

import copy

class State():

    #initial state
    def __init__(self, d = None):               #takes in self and input parameter default to none
        if d == None:                           #if no input start parameter
            d = {'left':['F', 'f', 'C', 'G'],   #things on left bank
                 'right':[]}                    #things on right bank
        self.d = d

    def __eq__(self, state2):                   #determines if two states are equal
        for prop in river:                      #for positions
            if self.d[prop] != state2.d[prop]:  
                return False                    #return false if mismatched states
            return True

    def __str__(self):                          #returns a string representation of itself
        left = self.d['left']
        right = self.d['right']
        txt = "\nItems on the left bank: " + str(left) + "\n"
        txt += "Items on the right bank: " + str(right) + "\n"
        side = 'left'
        if 'F' in self.d['right']: side = 'right'
        txt += "Farmer and Boat are on the " + side + ".\n"
        return txt

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        newState = State({})
        newState.d['left'] = copy.deepcopy(self.d['left']) #not sure about this one
        newState.d['right'] = copy.deepcopy(self.d['right']) #not sure about this one
        return newState

    def can_move(self, item):
        side = 'left'
        if 'F' in self.d['right']: side = 'right'
        if item not in self.d[side]:
            return False
        for things in self.d[side]:
            if (things != 'F') and (things != item):
                if bad_move[things] in self.d[side]:
                    if bad_move[things] != item:
                        return False
        return True

    def move(self, item):
        news = self.copy()
        side = 'left'
        other = 'right'
        if 'F' in self.d['right']:
            side = 'right'
            other = 'left'
        if item != 'F':
            news.d[side].remove(item)
            news.d[other].append(item)
        news.d[side].remove('F')
        news.d[other].append('F')
        return news

def goal_test(state):
    for items in ['F', 'f', 'C', 'G']:
        if items not in state.d['right']:
            return False
    return True

def goal_message(state):
    return "Success!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

#INITIAL STATE
CREATE_INITIAL_STATE = lambda : State(d=None)

#OPERATORS
ITEMS = ['F', 'f', 'C', 'G']

OPERATORS = [Operator(
    "Cross the river with the " + str(i),
    lambda s, i1 = i: s.can_move(i1),
    lambda s, i1 = i: s.move(i1) )
    for i in ITEMS]
            
#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
