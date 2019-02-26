''' varunv97_TTS_agent.py
By Varun Venkatesh
Student Number: 1560337
UWNETID: varunv97
Assignment 4, CSE 415, Winter 2019

This contains the code for the game playing agent created by Varun Venkatesh
'''

import time
from TTS_State import TTS_State
import random

static_eval = 0
max_depth_reached = 0
USE_CUSTOM_STATIC_EVAL_FUNCTION = True
expanded_states = 0
IDDFS = False
limit_time = 1.0
turns = 0
cut_off = 0
reached_limit = False
ab_prune = False

Utter = ['Hmmmm... Ive been practicing this for a while - hopefully it works!',
              'I bet you cant figure out a counter to this move!',
              'I can see it now - this move will decide the game!',
              'Oh man I have to go to work, uhhhhh hopefully this works!',
              'I sweep you across the floor with this move!',
              'Try this one on for a size - Its one of my smartest moves to date',
              'I see your plan, here is a good counter',
              'BOOM! Try winning against that move!!!',
              'I would not have done that - heres a move that you should have done!',
              'Ok I see you thats a good move, but it isnt better than this!']

class MY_TTS_State(TTS_State):
    def static_eval(self):
        global static_eval
        static_eval += 1
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else:
            return self.basic_static_eval()

    def basic_static_eval(self):
        return self.get_t(2)
        # raise Exception("basic_static_eval not yet implemented.")

    def custom_static_eval(self):
        return self.get_custom_t(2)
        # raise Exception("custom_static_eval not yet implemented.")

    def get_t(self, length):
        global K
        count_White = 0
        count_Black = 0
        row_len = len(self.board)
        col_len = len(self.board[0])

        for row in range(row_len):
            for col in range(col_len):
                w_count = 0
                b_count = 0
                block = False
                # start by going down -> figure out wrapping
                count = 0
                for i in range(K):
                    if row + i < row_len:
                        curr = self.board[row+i][col]
                    else:
                        curr = self.board[count][col]
                        count += 1
                    if curr == 'W':
                        w_count += 1
                    elif curr == 'B':
                        b_count += 1
                    elif curr == '-':
                        block = True

                if w_count == length and b_count == 0 and block is False:
                    count_White += 1
                if b_count == length and w_count == 0 and block is False:
                    count_Black += 1

                count = 0
                block = False
                w_count = 0
                b_count = 0

                # next go right -> figure out wrapping
                for i in range(K):
                    if col + i < col_len:
                        curr = self.board[row][col+i]
                    else:
                        curr = self.board[row][count]
                        count += 1
                    if curr == 'W':
                        w_count += 1
                    elif curr == 'B':
                        b_count += 1
                    elif curr == '-':
                        block = True

                if w_count == length and b_count == 0 and block is False:
                    count_White += 1
                if b_count == length and w_count == 0 and block is False:
                    count_Black += 1

                count_row = row
                count_col = col
                block = False
                w_count = 0
                b_count = 0
                first = True
                # next go diagonal down and right -> figure out wrapping
                for i in range(K):
                    if first is False:
                        count_row += 1
                        count_col += 1
                    first = False

                    if count_row < 0 or count_row >= len(self.board):
                        count_row = ((count_row + len(self.board)) % len(self.board))
                    if count_col < 0 or count_col >= len(self.board[0]):
                        count_col = ((count_col + len(self.board[0])) % len(self.board[0]))

                    curr = self.board[count_row][count_col]

                    if curr == 'W':
                        w_count += 1
                    elif curr == 'B':
                        b_count += 1
                    elif curr == '-':
                        block = True
                if w_count == length and b_count == 0 and block is False:
                    count_White += 1
                if b_count == length and w_count == 0 and block is False:
                    count_Black += 1

                count_row = row
                count_col = col
                block = False
                w_count = 0
                b_count = 0
                first = True
                # next go diagonal down and right -> figure out wrapping
                for i in range(K):
                    if first is False:
                        count_row += 1
                        count_col -= 1
                    first = False

                    if count_row < 0 or count_row >= len(self.board):
                        count_row = ((count_row + len(self.board)) % len(self.board))
                    if count_col < 0 or count_col >= len(self.board[0]):
                        count_col = ((count_col + len(self.board[0])) % len(self.board[0]))

                    curr = self.board[count_row][count_col]

                    if curr == 'W':
                        w_count += 1
                    elif curr == 'B':
                        b_count += 1
                    elif curr == '-':
                        block = True
                if w_count == length and b_count == 0 and block is False:
                    count_White += 1
                if b_count == length and w_count == 0 and block is False:
                    count_Black += 1

        return count_White-count_Black

    def get_custom_t(self, length):
        total = 0
        for i in range(1, length):
            total += self.get_t(i) * (10 ** (i-1))

        return total


def take_turn(current_state, last_utterance, time_limit):
    global reached_limit, cut_off, max_depth_reached
    board = current_state.board
    new_position = MY_TTS_State(current_state.board)
    start = time.time()
    who = current_state.whose_turn
    if _find_next_vacancy(new_position.board) is False:
        return [[False, current_state], "There is no possible moves that I can make :("]

    depth = 0
    cut_off = 0
    reached_limit = False
    if IDDFS:
        while reached_limit is False:
            depth += 1
            new_position = timed_alpha_beta(current_state, who, depth, -100000, 100000, time_limit, start)
    else:
        new_position = alphaBeta(current_state, 2, -100000, 100000, who)
    change = ' '
    for i in range(len(board)):
        for j in range(len(board[0])):
            if current_state.board[i][j] != new_position.board[i][j]:
                change = (i, j)

    x = random.randint(0, 10)
    mutter = Utter[x % 10]

    return [[change, new_position], mutter]


def _find_next_vacancy(b):
    for i in range(len(b)):
      for j in range(len(b[0])):
        if b[i][j]==' ': return (i,j)
    return False


def moniker():
    return "Chuck"

def who_am_i():
    return """Hello! My name is Chuck and I'm a vacuum salesman who just loves playing Toro-Tile in my free time!
    This is my one true passion and I believe that one day, I will be the best player in the world! Thanks for 
    helping me practice!!!
    My coach/creator's name is Varun Venkatesh and his netid is varunv97."""

def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like eval pre-calculation, here.
    global my_side, op_side, K
    my_side = who_i_play
    K = k
    op_side = getOpponentSide(my_side)

    return "OK"

def successors(state, opp):
    board = state.board
    success = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if state.board[i][j] == ' ':
                new_position = MY_TTS_State(state.board, getOpponentSide(opp))
                new_position.board[i][j] = opp
                success.append(new_position)

    return success

def getOpponentSide(other_Side):
    if other_Side == 'W':
        return 'B'
    return 'W'

def parameterized_minimax(
       current_state=None,
       use_iterative_deepening_and_time = False,
       max_ply=2,
       use_default_move_ordering = False,
       alpha_beta=False,
       time_limit=1.0,
       use_custom_static_eval_function=False):

    # All students, add code to replace these default
    # values with correct values from your agent (either here or below).
    global ab_prune, reached_limit, expanded_states, IDDFS, limit_time, static_eval, cut_off, max_depth_reached, USE_CUSTOM_STATIC_EVAL_FUNCTION
    expanded_states = 0
    static_eval = 0
    max_depth_reached = 0
    USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function

    ab_prune = alpha_beta
    if use_iterative_deepening_and_time and alpha_beta:
      cut_off = 0
      reached_limit = False
      new_position = MY_TTS_State(current_state.board)
      start = time.time()
      ply = 0
      while reached_limit is False and ply <= max_ply:
          ply += 1
          new_position = timed_alpha_beta(current_state, current_state.whose_turn, ply, -100000, 100000, time_limit, start)

    elif alpha_beta and not use_iterative_deepening_and_time:
        cut_off = 0
        new_position = MY_TTS_State(current_state.board)
        max_depth_reached = max_ply
        new_position = alphaBeta(current_state, max_ply, 100000, 100000, current_state.whose_turn)

    elif use_iterative_deepening_and_time and not alpha_beta:
        reached_limit = False
        new_position = MY_TTS_State(current_state.board)
        start = time.time()
        ply = 0
        while reached_limit is False and ply <= max_ply:
          ply += 1
          new_position = iddfs(new_position, start, time_limit, ply)
    else:
        new_position = MY_TTS_State(current_state.board)
        new_position = minimax(new_position, max_ply)

    current_state_static_val = new_position.static_eval()
    n_states_expanded = expanded_states
    n_static_evals_performed = static_eval
    max_depth_reached = max_ply
    n_ab_cutoffs = cut_off
    IDDFS = use_iterative_deepening_and_time


    # Prepare to return the results, don't change the order of the results
    results = []
    results.append(current_state_static_val)
    results.append(n_states_expanded)
    results.append(n_static_evals_performed)
    results.append(max_depth_reached)
    results.append(n_ab_cutoffs)
    # Actually return the list of all results...
    return(results)

def minimax(position, depth):
    global max_depth_reached, expanded_states
    if depth < max_depth_reached:
        max_depth_reached = depth
    position.__class__ = MY_TTS_State
    if depth == 0 or _find_next_vacancy(position.board) is False:
        return position

    children = successors(position, getOpponentSide(position.whose_turn))
    return_state = position
    if position.whose_turn == 'W':
        maximum = -1000
        for child in children:
            expanded_states += 1
            temp_state = minimax(child, depth - 1)
            score = temp_state.static_eval()
            if score > maximum:
                maximum = score
                return_state = child
        return return_state
    else:
        minimum = 1000
        for child in children:
            expanded_states += 1
            temp_state = minimax(child, depth - 1)
            score = temp_state.static_eval()
            if score < minimum:
                minimum = score
                return_state = child
        return_state

def alphaBeta(position, depth, alpha, beta, who):
    global max_depth_reached, expanded_states, cut_off
    if depth < max_depth_reached:
        max_depth_reached = depth
    position.__class__ = MY_TTS_State
    if depth == 0 or _find_next_vacancy(position.board) is False:
        return position

    children = successors(position, who)
    return_state = position
    if position.whose_turn == 'W':
        maximum = -100000
        for child in children:
            expanded_states += 1
            temp_state = alphaBeta(child, depth - 1, alpha, beta, getOpponentSide(who))
            score = temp_state.static_eval()
            alpha = max(alpha, score)
            if score > maximum:
                maximum = score
                return_state = child
            if beta <= alpha:
                cut_off += 1
                break
        return return_state
    else:
        minimum = 100000
        for child in children:
            expanded_states += 1
            temp_state = alphaBeta(child, depth - 1, alpha, beta, getOpponentSide(who))
            score = temp_state.static_eval()
            beta = min(beta, score)
            if score < minimum:
                minimum = score
                return_state = child
            if beta <= alpha:
                cut_off += 1
                break
        return return_state

def timed_alpha_beta(position, who, depth, alpha, beta, limit, start_time):
    global reached_limit, cut_off, expanded_states
    global max_depth_reached
    if depth < max_depth_reached:
        max_depth_reached = depth
    position.__class__ = MY_TTS_State
    if depth == 0 or _find_next_vacancy(position.board) is False:
        return position

    curr_time = time.perf_counter()
    if ((curr_time - start_time) >= limit) or depth == 0:
        reached_limit = True
        return position

    children = successors(position, who)
    return_state = position
    if position.whose_turn == 'W':
        maximum = -100000
        for child in children:
            expanded_states += 1
            temp_state = timed_alpha_beta(child, getOpponentSide(who), depth - 1, alpha, beta, limit, start_time)
            score = temp_state.static_eval()
            alpha = max(alpha, score)
            if score > maximum:
                maximum = score
                return_state = child
            if beta <= alpha:
                cut_off += 1
                break
        return return_state
    else:
        minimum = 100000
        for child in children:
            expanded_states += 1
            temp_state = timed_alpha_beta(child, getOpponentSide(who), depth - 1, alpha, beta, limit, start_time)
            score = temp_state.static_eval()
            beta = min(beta, score)
            if score < minimum:
                minimum = score
                return_state = child
            if beta <= alpha:
                cut_off += 1
                break
        return return_state

def iddfs(state, start, time_limit, depth):
    global expanded_states, max_depth_reached, reach_limit, ab_prune, my_side
    state.__class__ = MY_TTS_State
    if depth < max_depth_reached:
        max_depth_reached = depth
    curr_time = time.perf_counter()
    who = my_side
    if ((curr_time - start) >= time_limit) or depth == 0:
        reach_limit = True
        return state

    if ab_prune:
        new_position = alphaBeta(state, depth, -1000, 1000, getOpponentSide(who))
    else:
        new_position = minimax(state, depth)
    return new_position
