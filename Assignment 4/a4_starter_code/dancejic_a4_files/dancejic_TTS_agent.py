'''dancejic_TTS_agent.py
Nikola Dancejic

uses:
python game_master.py Simple_Game_Type Player_Newman dancejic_TTS_agent
python game_master.py Gold_Rush_Game_Type Player_Newman dancejic_TTS_agent
python game_master.py Gold_Rush_Game_Type dancejic_TTS_agent dancejic_TTS_agent

python timed_tts_game_master.py Gold_Rush_Game_Type Player_Newman dancejic_TTS_agent 2

python timed_tts_game_master.py Gold_Rush_Game_Type dancejic_TTS_agent Player_Newman 1

python timed_tts_game_master.py Gold_Rush_Game_Type varunv97_TTS_agent dancejic_TTS_agent 2

python timed_tts_game_master.py Gold_Rush_Game_Type dancejic_TTS_agent varunv97_TTS_agent 1

'''

from TTS_State import TTS_State
import time
import random

#testing settings
USE_CUSTOM_STATIC_EVAL_FUNCTION = True
A_B = True

#win condition
K = 3

#timing things
StartTime = 0
timeLimit = 0

#testing variables
n_states = 0
n_evals = 0
max_depth = 0
n_cutoff = 0
ply_covered = []

#utterances
Utterances = ['Lets try this!',
              'I think I\'m finally understanding',
              'NOPE I take that back, I have no idea',
              'Ok so if I play here maybe?',
              'To be honest I just picked a move I thought would be cool',
              'HAH I think I did something good',
              'Things are not looking great',
              'Maybe this might work?',
              'A lucky guess!',
              'I\'m pretty sure I got pretty lucky this game and picked some good moves']
Used_Utterances = []

class MY_TTS_State(TTS_State):
    def static_eval(self):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else:
            return self.basic_static_eval()

    def basic_static_eval(self):
        global StartTime, timeLimit, K, n_evals
        n_evals += 1
        X = 2  # default
        B_row = 0
        W_row = 0
        #precalculating the size of the board in the i direction
        b_size = len(self.board)
        for i in range(b_size):
            #precalculating the size of the board in the j direction
            b_sizej = len(self.board[i])
            for j in range(b_sizej):
                #set all lines to 0
                R_W_tiles = 0
                R_B_tiles = 0
                DR_W_tiles = 0
                DR_B_tiles = 0
                D_W_tiles = 0
                D_B_tiles = 0
                DL_W_tiles = 0
                DL_B_tiles = 0
                R_tiles = 0
                DR_tiles = 0
                D_tiles = 0
                DL_tiles = 0
                #check all directions for black, white, or blocked tiles
                for k in range(K):
                    if (self.board[i][(j + k) % b_sizej] == 'W'):
                        R_W_tiles += 1
                    if (self.board[i][(j + k) % b_sizej] == 'B'):
                        R_B_tiles += 1
                    if (self.board[i][(j + k) % b_sizej] == '-'):
                        R_tiles += 1
                    if (self.board[(i + k) % b_size][(j + k) % b_sizej] == 'W'):
                        DR_W_tiles += 1
                    if (self.board[(i + k) % b_size][(j + k) % b_sizej] == 'B'):
                        DR_B_tiles += 1
                    if (self.board[(i + k) % b_size][(j + k) % b_sizej] == '-'):
                        DR_tiles += 1
                    if (self.board[(i + k) % b_size][j] == 'W'):
                        D_W_tiles += 1
                    if (self.board[(i + k) % b_size][j] == 'B'):
                        D_B_tiles += 1
                    if (self.board[(i + k) % b_size][j] == '-'):
                        D_tiles += 1
                    if (self.board[(i + k) % b_size][(j + b_sizej - k) % b_sizej] == 'W'):
                        DL_W_tiles += 1
                    if (self.board[(i + k) % b_size][(j + b_sizej - k) % b_sizej] == 'B'):
                        DL_B_tiles += 1
                    if (self.board[(i + k) % b_size][(j + b_sizej - k) % b_sizej] == '-'):
                        DL_tiles += 1
                #for any rows with X player tiles that are not blocked, add to W_row and B_row
                if (R_W_tiles == X and R_B_tiles == 0 and R_tiles == 0):
                    W_row += 1
                if (R_B_tiles == X and R_W_tiles == 0 and R_tiles == 0):
                    B_row += 1
                if (DR_W_tiles == X and DR_B_tiles == 0 and DR_tiles == 0):
                    W_row += 1
                if (DR_B_tiles == X and DR_W_tiles == 0 and DR_tiles == 0):
                    B_row += 1
                if (D_W_tiles == X and D_B_tiles == 0 and D_tiles == 0):
                    W_row += 1
                if (D_B_tiles == X and D_W_tiles == 0 and D_tiles == 0):
                    B_row += 1
                if (DL_W_tiles == X and DL_B_tiles == 0 and DL_tiles == 0):
                    W_row += 1
                if (DL_B_tiles == X and DL_W_tiles == 0 and DL_tiles == 0):
                    B_row += 1
                #stop if youre out of time
                if (time.perf_counter() - StartTime > timeLimit):
                    return W_row - B_row
        #return the amount found for white - amount found for black
        return W_row - B_row

    #custom eval finds number of unblocked lines increasing from 2 to K-1 weighing them seperately
    def custom_static_eval(self):
        global StartTime, timeLimit, K, n_evals
        n_evals += 1
        B_row = 0
        W_row = 0
        b_size = len(self.board)
        #similar function to basic eval but runs for varying X
        for X in range(2, K):
            for i in range(b_size):
                b_sizej = len(self.board[i])
                for j in range(b_sizej):
                    R_W_tiles = 0
                    R_B_tiles = 0
                    DR_W_tiles = 0
                    DR_B_tiles = 0
                    D_W_tiles = 0
                    D_B_tiles = 0
                    DL_W_tiles = 0
                    DL_B_tiles = 0
                    R_tiles = 0
                    DR_tiles = 0
                    D_tiles = 0
                    DL_tiles = 0
                    for k in range(K):
                        if (self.board[i][(j + k) % b_sizej] == 'W'):
                            R_W_tiles += 1
                        if (self.board[i][(j + k) % b_sizej] == 'B'):
                            R_B_tiles += 1
                        if (self.board[i][(j + k) % b_sizej] == '-'):
                            R_tiles += 1
                        if (self.board[(i + k) % b_size][(j + k) % b_sizej] == 'W'):
                            DR_W_tiles += 1
                        if (self.board[(i + k) % b_size][(j + k) % b_sizej] == 'B'):
                            DR_B_tiles += 1
                        if (self.board[(i + k) % b_size][(j + k) % b_sizej] == '-'):
                            DR_tiles += 1
                        if (self.board[(i + k) % b_size][j] == 'W'):
                            D_W_tiles += 1
                        if (self.board[(i + k) % b_size][j] == 'B'):
                            D_B_tiles += 1
                        if (self.board[(i + k) % b_size][j] == '-'):
                            D_tiles += 1
                        if (self.board[(i + k) % b_size][(j + b_sizej - k) % b_sizej] == 'W'):
                            DL_W_tiles += 1
                        if (self.board[(i + k) % b_size][(j + b_sizej - k) % b_sizej] == 'B'):
                            DL_B_tiles += 1
                        if (self.board[(i + k) % b_size][(j + b_sizej - k) % b_sizej] == '-'):
                            DL_tiles += 1
                    if (R_W_tiles == X and R_B_tiles == 0 and R_tiles == 0):
                        W_row += 1 * X * 2 ** (X - 1)
                    if (R_B_tiles == X and R_W_tiles == 0 and R_tiles == 0):
                        B_row += 1 * X * 2 ** (X - 1)
                    if (DR_W_tiles == X and DR_B_tiles == 0 and DR_tiles == 0):
                        W_row += 1 * X * 2 ** (X - 1)
                    if (DR_B_tiles == X and DR_W_tiles == 0 and DR_tiles == 0):
                        B_row += 1 * X * 2 ** (X - 1)
                    if (D_W_tiles == X and D_B_tiles == 0 and D_tiles == 0):
                        W_row += 1 * X * 2 ** (X - 1)
                    if (D_B_tiles == X and D_W_tiles == 0 and D_tiles == 0):
                        B_row += 1 * X * 2 ** (X - 1)
                    if (DL_W_tiles == X and DL_B_tiles == 0 and DL_tiles == 0):
                        W_row += 1 * X * 2 ** (X - 1)
                    if (DL_B_tiles == X and DL_W_tiles == 0 and DL_tiles == 0):
                        B_row += 1 * X * 2 ** (X - 1)
                    # print(time.perf_counter() - StartTime)
                    if (time.perf_counter() - StartTime > timeLimit):
                        return W_row - B_row
        #checking one last time for any wins
        for i in range(b_size):
            b_sizej = len(self.board[i])
            for j in range(b_sizej):
                R_W_tiles = 0
                R_B_tiles = 0
                DR_W_tiles = 0
                DR_B_tiles = 0
                D_W_tiles = 0
                D_B_tiles = 0
                DL_W_tiles = 0
                DL_B_tiles = 0
                R_tiles = 0
                DR_tiles = 0
                D_tiles = 0
                DL_tiles = 0
                for k in range(K):
                    if (self.board[i][(j + k) % b_sizej] == 'W'):
                        R_W_tiles += 1
                    if (self.board[i][(j + k) % b_sizej] == 'B'):
                        R_B_tiles += 1
                    if (self.board[i][(j + k) % b_sizej] == '-'):
                        R_tiles += 1
                    if (self.board[(i + k) % b_size][(j + k) % b_sizej] == 'W'):
                        DR_W_tiles += 1
                    if (self.board[(i + k) % b_size][(j + k) % b_sizej] == 'B'):
                        DR_B_tiles += 1
                    if (self.board[(i + k) % b_size][(j + k) % b_sizej] == '-'):
                        DR_tiles += 1
                    if (self.board[(i + k) % b_size][j] == 'W'):
                        D_W_tiles += 1
                    if (self.board[(i + k) % b_size][j] == 'B'):
                        D_B_tiles += 1
                    if (self.board[(i + k) % b_size][j] == '-'):
                        D_tiles += 1
                    if (self.board[(i + k) % b_size][(j + b_sizej - k) % b_sizej] == 'W'):
                        DL_W_tiles += 1
                    if (self.board[(i + k) % b_size][(j + b_sizej - k) % b_sizej] == 'B'):
                        DL_B_tiles += 1
                    if (self.board[(i + k) % b_size][(j + b_sizej - k) % b_sizej] == '-'):
                        DL_tiles += 1
                #return a huge (or small) number if a win is found
                if (R_W_tiles == K):
                    return 1000000
                if (R_B_tiles == K):
                    return -1000000
                if (DR_W_tiles == K):
                    return 1000000
                if (DR_B_tiles == K):
                    return -1000000
                if (D_W_tiles == K):
                    return 1000000
                if (D_B_tiles == K):
                    return -1000000
                if (DL_W_tiles == K):
                    return 1000000
                if (DL_B_tiles == K):
                    return -100000
                if (time.perf_counter() - StartTime > timeLimit):
                    return W_row - B_row
        return W_row - B_row


def take_turn(current_state, last_utterance, time_limit):
    global StartTime, timeLimit
    timeLimit = time_limit
    # print(time_limit)

    # Compute the new state for a move.
    # Start by copying the current state.
    new_state = MY_TTS_State(current_state.board)
    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = 'B'
    if who == 'B': new_who = 'W'
    new_state.whose_turn = new_who

    #set the start time of the program
    StartTime = time.perf_counter()

    #find the location to play using iterative deepening
    location = IterativeDeepeningDFS(new_state, new_who, 1000000)

    #play the move (maybe not needed?)
    new_state.board[location[0]][location[1]] = who

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    move = location

    # Make up a new remark
    new_utterance = utter_phrase()

    return [[move, new_state], new_utterance]

#not used although I probably could have
def _find_next_vacancy(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == ' ': return (i, j)
    return False

#named after a buddy of mine
def moniker():
    return "Patty"  # Return your agent's short nickname here.

def who_am_i():
    return """My name is Patrick, created by Nikola Dancejic.
(UWNetID: dancejic) I'm pretty lucky I guess, don't know how I do it."""

#doesn't do much, didnt have time to implement
def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like eval pre-calculation, here.
    global K
    K = k
    return "OK"


# The following is a skeleton for the function called parameterized_minimax,
# which should be a top-level function in each agent file.
# A tester or an autograder may do something like
# import ABC_TTS_agent as player, call get_ready(),
# and then it will be able to call tryout using something like this:
# results = player.parameterized_minimax(**kwargs
def parameterized_minimax(
        current_state=None,
        use_iterative_deepening_and_time=False,
        max_ply=2,
        use_default_move_ordering=False,
        alpha_beta=False,
        time_limit=1.0,
        use_custom_static_eval_function=False):
    # All students, add code to replace these default
    # values with correct values from your agent (either here or below).
    current_state_static_val = -1000.0
    n_states_expanded = 0
    n_static_evals_performed = 0
    max_depth_reached = 0
    n_ab_cutoffs = 0

    # STUDENTS: You may create the rest of the body of this function here.
    global A_B, n_cutoff, max_depth, n_evals, n_states, USE_CUSTOM_STATIC_EVAL_FUNCTION, timeLimit

    #reset the globals in case they were used previously
    n_states = 0
    n_evals = 0
    max_depth = 0
    n_cutoff = 0

    USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function

    if(current_state != None):
        current_state_static_val = MY_TTS_State(current_state).static_eval()

    #I use the default_move_ordering already

    #this should not be used in a normal game A_B is by default true
    if(not alpha_beta):
        A_B = False

    if(use_iterative_deepening_and_time):
        timeLimit = time_limit
        IterativeDeepeningDFS(current_state, current_state.whose_turn, max_ply)
    else:
        if(alpha_beta):
            Alpha_Beta(current_state, current_state.whose_turn, -1000000, 1000000, max_ply)
        else:
            minimax_search(current_state, current_state.whose_turn, max_ply)

    #give back values
    n_states_expanded = n_states
    n_static_evals_performed = n_evals
    max_depth_reached = max_depth
    n_ab_cutoffs = n_cutoff


    # Prepare to return the results, don't change the order of the results
    results = []
    results.append(current_state_static_val)
    results.append(n_states_expanded)
    results.append(n_static_evals_performed)
    results.append(max_depth_reached)
    results.append(n_ab_cutoffs)
    # Actually return the list of all results...
    return (results)


def minimax_search(board, whoseMove, plyLeft):
    global StartTime, timeLimit
    #precalculate all possible moves
    openspots = open_Spots(board)
    #return if no possible moves
    if (openspots == []):
        return [[], board.static_eval()]
    #find first opening
    location = openspots[0]
    if plyLeft == 0:
        return [location, board.static_eval()]
    #initialize provisional to inf if black -inf if white
    otherMove = 'W'
    if whoseMove == 'W':
        provisional = -1000000
        otherMove = 'B'
    else:
        provisional = 1000000
    # traverse the open spots
    for spots in openspots:
        # make a new board for a move
        newBoard = MY_TTS_State(board.board, whoseMove)
        newBoard.board[spots[0]][spots[1]] = whoseMove
        #recursively look for better value
        newVal = minimax_search(newBoard, otherMove, plyLeft - 1)[1]
        if (whoseMove == 'W' and newVal > provisional or whoseMove == 'B' and newVal < provisional):
            provisional = newVal
            location = spots
        # break if out of time
        if (time.perf_counter() - StartTime > timeLimit):
            break
    return [location, provisional]

#similar to minimax
def Alpha_Beta(board, whoseMove, alpha, beta, plyLeft):
    global StartTime, timeLimit, n_states, max_depth, n_cutoff, ply_covered
    if(plyLeft not in ply_covered):
        max_depth += 1
    successors = open_Spots(board)
    if (successors == []):
        return [[], board.static_eval()]
    location = successors[0]
    if (plyLeft == 0):
        return [location, board.static_eval()]
    otherMove = 'W'
    if whoseMove == 'W':
        otherMove = 'B'
    # print("in AB")
    n_states += 1
    if (whoseMove == 'W'):
        for locations in successors:
            newBoard = MY_TTS_State(board.board, whoseMove)
            newBoard.board[locations[0]][locations[1]] = whoseMove
            newVal = Alpha_Beta(newBoard, otherMove, alpha, beta, plyLeft - 1)
            if (newVal[1] > alpha):
                alpha = newVal[1]
                location = locations
            if (alpha >= beta):
                n_cutoff += 1
                break
            # print(time.perf_counter() - StartTime)
            if (time.perf_counter() - StartTime > timeLimit):
                break
        return [location, alpha]
    else:
        for locations in successors:
            newBoard = MY_TTS_State(board.board, whoseMove)
            newBoard.board[locations[0]][locations[1]] = whoseMove
            newVal = Alpha_Beta(newBoard, otherMove, alpha, beta, plyLeft - 1)
            if (newVal[1] < beta):
                beta = newVal[1]
                location = locations
            if (alpha >= beta):
                n_cutoff += 1
                break
            # print(time.perf_counter() - StartTime)
            if (time.perf_counter() - StartTime > timeLimit):
                break
        return [location, beta]

#takes in a board and returns all open positions
def open_Spots(board):
    OPEN = []
    for i in range(len(board.board)):
        for j in range(len(board.board[i])):
            if (board.board[i][j] == ' '):
                OPEN.append([i, j])
    return OPEN

#itarative deepening
def IterativeDeepeningDFS(board, whoseMove, maxPly):
    global StartTime, timeLimit
    for depth in range(maxPly):
        if(A_B):
            result = Alpha_Beta(board, whoseMove, -1000000, 1000000, depth)
        else:
            minimax_search(board, whoseMove, depth)
        location = result[0]
        if (time.perf_counter() - StartTime) > timeLimit:
            return location

def utter_phrase():
    global Used_Utterances, Utterances
    for i in range(len(Utterances)):
        phrase = random.choice(Utterances)
        if phrase not in Used_Utterances:
            Used_Utterances.append(phrase)
            return phrase
    phrase = random.choice(Utterances)
    Used_Utterances = []
    Used_Utterances.append(phrase)
    return phrase
