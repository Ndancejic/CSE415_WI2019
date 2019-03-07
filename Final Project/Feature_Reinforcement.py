'''
Nikola Dacejic
dancejic
Feature_Reinforcement.py

This file implements the feature reinforcement algorithm on the rubiks cube
'''

from dancejic_Rubik2Cube import *
import dancejic_Rubik2CubeWithHeuristics as cube
import random

gamma = 0.9
episodes = 1000
max_steps = 100

Q_Values = {}
F = [] #set of features
S = []
weights = [1]*len(F)

def SARSA_FA(n):
    global Q_Values, weights
    for episode in episodes:
        s = State()
        a = random.choice(cube.directions)
        update_Q(s,a)
        for steps in range(max_steps):
            sp = s.copy()
            sp.move(a)
            R = R(sp)
            max_a = 'F'
            for action in cube.directions:
                update_Q(sp, action)
                if Q_Values[(sp,a)] > max_a:
                    max_a = action
            ap = max_a
            delta = R + gamma*Q_Values[(sp,ap)]-Q_Values[(s,a)]
            for i in range(len(F)):
                weights[i] = weights[i]+n*delta*F(s,a,i)
            s = sp
            a = ap
            if(cube.goal_test(sp)):
                break

def update_Q(s,a):
    global Q_Values, F, weights
    Q_Values[(s,a)] = sum([weights[k]*F[k] for k in len(F)])

def R(s):
    '''
    :param s: current state
    :return: reward for state
    '''
    global Q_Values
    max_Q = 0
    for a in cube.directions:
        if Q_Values[(s,a)] > max_Q:
            max_Q = Q_Values[(s,a)]
    return max_Q

def F(s,a,i):
    '''
    :param s: current state
    :param a: action to take
    :param i: feature to compare
    :return: 1 if feature is true, 0 if feature is false
    '''
    sp = s.copy()
    sp.move(a)
    if sp.b == F[i]:
        return 1
    return 0

