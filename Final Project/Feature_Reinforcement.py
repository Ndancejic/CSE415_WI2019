'''
Nikola Dacejic
dancejic

Rebecca Rollins
rrolli

use:
python Feature_Reinforcement.py

This file implements the feature reinforcement algorithm on the rubiks cube
'''

from Rubik2Cube import *
import Rubik2CubeWithHeuristics as cube
import random

#Run conditions
DEFAULT_START = False #false for random start state
start_rotations = 15 #depth of start state
initial_w = 1
episodes = 200
max_steps = 100

#variables
n = 10
epsilon = 0.2
gamma = 0.9
epsilon_decay = 0.99
gamma_decay = 0.5

'''
These seem to work well:
n = 0.1
epsilon = 0.2
gamma = 0.9
epsilon_decay = 1
gamma_decay = 0.5
'''

#Stored Values
Q_Values = {}
weights = [] #[initial_w]*(len(F) + len(F2)) Initialized in function now

#Features
F = [] #automated now
F2 = [2,2,2,2,2,2, # Feature checking if there are 2 tiles of the same color on a face
      3,3,3,3,3,3, # Feature checking if there are 3 tiles of the same color on a face
      4,4,4,4,4,4] # Feature checking if there are 4 tiles of the same color on a face

def SARSA_FA():
    '''
    :return: None
    performs feature based SARSA with Q_value approximation
    '''
    global Q_Values, weights, n, gamma, episode, max_steps, epsilon
    Generate_F()
    weights = [initial_w]*(len(F) + len(F2))
    print("Finding solution . . .")
    start_state = generate_start()
    solution = []
    min_steps = 1000
    solution_found = False
    for episode in range(episodes):
        if DEFAULT_START:
            s = State(cube.init_state_list)
        else:
            s = start_state
        if episode == 0:
            print("Starting at initial state: " + str(s.b))
        chance = random.choice(range(100))
        if chance < epsilon*100:
            a = random.choice(cube.directions)
        else:
            max = random.choice(cube.directions)
            for action in cube.directions:
                if get_Q(s,action) > get_Q(s,max):
                    max = action
            a = max
        temp = []
        print("Episode " + str(episode) + " . . .")
        for steps in range(max_steps):
            temp.append(a)
            if(cube.goal_test(s)):
                print("Found solution in " + str(steps) + " steps")
                if steps < min_steps:
                    min_steps = steps
                    solution = temp
                break
            sp = s.copy()
            sp = sp.move(a)
            R = get_R(sp)
            if chance < epsilon*100:
                ap = random.choice(cube.directions)
            else:
                max_a = random.choice(cube.directions)
                for action in cube.directions:
                    if get_Q(sp,action) > get_Q(sp,max_a):
                        max_a = action
                ap = max_a
            delta = R + gamma*get_Q(sp,ap)-get_Q(s,a)
            gamma = gamma*gamma_decay
            for i in range(len(weights)):
                weights[i] = weights[i]+n*delta*get_F(s,a,i)
            s = sp
            a = ap
            if(cube.goal_test(s)):
                print("Found solution in " + str(steps + 1) + " steps")
                if steps < min_steps:
                    min_steps = steps + 1
                    solution = temp
                break
        if(cube.goal_test(s)):
                solution_found = True
                #break
    epsilon = epsilon_decay*epsilon
    if not solution_found:
        print("Solution not found.")
    else:
        print("Solution found in " + str(min_steps) + " steps")
        print("The following solution was found: " + str(solution))

def get_Q(s,a):
    '''
    :param s: a state of the rubiks cube
    :param a: the action taken
    :return: updates the approximated Q_values and returns the current one
    '''
    global Q_Values, weights
    Q_Values[(s,a)] = sum([weights[k]*get_F(s,a,k) for k in range(len(weights))])
    return Q_Values[(s,a)]

def get_R(s):
    '''
    :param s: current state
    :return: reward for state
    '''
    global Q_Values
    if(cube.goal_test(s)):
        return 100
    max_Q = 0
    for a in cube.directions:
        if get_Q(s,a) > max_Q:
            max_Q = get_Q(s,a)
    return max_Q

def get_F(s,a,i):
    '''
    :param s: current state
    :param a: action to take
    :param i: feature to compare
    :return: 1 if feature is true, 0 if feature is false
    '''
    if i == 0:
        return 1
    sp = s.copy()
    sp = sp.move(a)
    if i > len(F):
        side = (i - len(F)) % 6
        count = 0
        # Feature: count max number of same colored tiles on each side
        # Tile 0
        if sp.b[side][0] == sp.b[side][1]:
            if sp.b[side][0] == sp.b[side][2] and F2[i-len(F)] > 2:
                if sp.b[side][0] == sp.b[side][3] and F2[i-len(F)] > 3:
                    count += 4
                else:
                    count += 3
            else:
                count += 2
        elif sp.b[side][1] == sp.b[side][2]:
            if sp.b[side][1] == sp.b[side][3] and F2[i-len(F)] > 2:
                count += 3
            else:
                count += 2
        elif sp.b[side][2] == sp.b[side][3]:
            count += 2
        return count > 4
    if sp.b == F[i-1]:
         return 1
    return 0

def Generate_F():
    '''
    :return: None
    generates all states 3 moves away from the goal state
    '''
    global F
    goal_state = State([['R', 'R', 'R', 'R'], ['O', 'O', 'O', 'O'],
        ['G', 'G', 'G', 'G'], ['B', 'B', 'B', 'B'],
        ['Y', 'Y', 'Y', 'Y'], ['W', 'W', 'W', 'W']])
    F.append(goal_state.b)
    for action1 in cube.directions:
        newState = goal_state.copy()
        newState = newState.move(action1).move(action1).move(action1)
        if newState.b not in F:
            F.append(newState.b)
        for action2 in cube.directions:
            newState2 = newState.copy()
            newState2 = newState2.move(action2).move(action2).move(action2)
            if newState2.b not in F:
                F.append(newState2.b)
            for action3 in cube.directions:
                newState3 = newState2.copy()
                newState3 = newState3.move(action3).move(action3).move(action3)
                if newState3.b not in F:
                    F.append(newState3.b)

def generate_start():
    '''
    :return: a start state start_rotations away from the goal state
    '''
    start_state = State([['R', 'R', 'R', 'R'], ['O', 'O', 'O', 'O'],
        ['G', 'G', 'G', 'G'], ['B', 'B', 'B', 'B'],
        ['Y', 'Y', 'Y', 'Y'], ['W', 'W', 'W', 'W']])
    for rotations in range(start_rotations):
        a = random.choice(cube.directions)
        start_state = start_state.move(a).move(a).move(a)
    return start_state



SARSA_FA()

