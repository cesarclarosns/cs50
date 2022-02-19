"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Set variables to 0 store the number of X and O in the board
    num_x = 0
    num_o = 0

    # Iterate over the rows of the board
    for i, row in enumerate(board):
        # Iterate over the columns of each row 
        for j, column in enumerate(row):
            # Increase num_x and num_o if (i, j) is equal to X or O
            if board[i][j] == X:
                num_x += 1
            if board[i][j] == O:
                num_o += 1

    # Return the player who has the next turn on board
    if num_o > num_x or (num_x + num_o) == 0 or num_o == num_x:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Initialize an empty set to store all the possible actions
    actions = set()

    # Iterate over the rows of the table
    for i, row in enumerate(board):
        # Iterate over the columns of each row
        for j, column in enumerate(row):
            # Add actions to the set of actions if (i, j) is EMPTY
            if board[i][j] == EMPTY:
                actions.add((i, j))
    # Return actions
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Create a deep copy of the board
    new_board = deepcopy(board)
    p = player(new_board)

    # If the action is valid, apply the action to the new board and return it
    if board[action[0]][action[1]] == EMPTY:
        new_board[action[0]][action[1]] = p
        return new_board
    else:
        raise ValueError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Define win states in rows
    win_states_r = [[(0, 0), (0, 1), (0, 2)],
                    [(1, 0), (1, 1), (1, 2)],
                    [(2, 0), (2, 1), (2, 2)]]
    # Define win states in columns
    win_states_c = [[(0, 0), (1, 0), (2, 0)],
                    [(0, 1), (1, 1), (2, 1)],
                    [(0, 2), (1, 2), (2, 2)]]
    # Define win states in diagonals
    win_states_d = [[(0, 0), (1, 1), (2, 2)],
                    [(2, 0), (1, 1), (0, 2)]]

    win_states = win_states_r + win_states_c + win_states_d

    # Compare each position in win_state to X or O
    for win_state in win_states:
        points_x = 0
        points_o = 0
        for position in win_state:
            if X == board[position[0]][position[1]]:
                points_x += 1
            if O == board[position[0]][position[1]]:
                points_o += 1
        if points_x == 3:
            return X
        if points_o == 3:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None or len(actions(board)) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    p_winner = winner(board)

    if p_winner == X:
        return 1
    elif p_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    # If the board is a terminal board, the minimax function should return None
    if terminal(board) == True:
        return None

    # Create empty lists to store the value of each action
    vals = []
    acts = []

    p = player(board)

    # The maximizing player picks an action a in actions(board) that produces
    # the highest value of min_value(result(board, action))
    if p == X:
        
        # For each action store its value and the action
        for action in actions(board):
            acts.append(action)
            vals.append(min_value(result(board, action)))
        
        # Find the highest value of vals and its index
        n = max(vals)
        index = vals.index(n)
        # Return the action that produces the highest value in vals
        return acts[index]

    # The minimizing player picks an action a in actions(board) that produces
    # the lowest value of max_value(result(board, action))
    if p == O:
        
        # For each action store its value and the action
        for action in actions(board):
            acts.append(action)
            vals.append(max_value(result(board, action)))
        
        # Find the lowest value of vals and its index
        n = min(vals)
        index = vals.index(n)
        # Return the action that produces the lowest value in vals
        return acts[index]


def max_value(board):
    """
    Returns max value
    """
    v = float('-inf')

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    """
    Returns min value
    """

    v = float('inf')

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v
