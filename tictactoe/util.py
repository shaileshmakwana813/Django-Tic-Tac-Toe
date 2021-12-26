"""
Tic Tac Toe Player
"""

import math
import copy

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
    x,o = 0,0
    for row in board:
        x += row.count(X)
        o += row.count(O)
    if x>o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == None:
                moves.add((row,col))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] not in [0,1,2] and action[1] not in [0,1,2]:
        raise Exception('Wrond index for action')
    
    if board[action[0]][action[1]] != None:
        raise Exception('Index already filled for action')
    
    turn = player(board)
    state = copy.deepcopy(board)
    state[action[0]][action[1]] = turn
    return state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #Horizontal Check
    for row in board:
        if row[0]==row[1] and row[1]==row[2] and row[0] != None:
                return row[0]
    
    #Vertical Check
    for i in range(len(board[0])):
        if board[0][i]==board[1][i] and board[1][i]==board[2][i] and board[0][i] != None:
                return board[0][i]
    
    #Diagonal Check
    if board[0][0]==board[1][1] and board[1][1]==board[2][2] and board[0][0] != None:
            return board[0][0]
    if board[0][2]==board[1][1] and board[1][1]==board[2][0] and board[0][2] != None:
            return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if (winner(board) != None):
        return True

    for row in board:
        if row.count(None) > 0:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    val = winner(board)
    if val==X:
        return 1
    elif val==O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    
    turn = player(board)
    last_action = None
    if turn==X:
        last_v = -math.inf
        for action in actions(board):
            v=min_value(result(board,action))
            if last_v < v:
                last_v = v
                last_action = action
        return last_action
    elif turn==O:
        last_v = math.inf
        for action in actions(board):
            v=max_value(result(board,action))
            if last_v > v:
                last_v = v
                last_action = action
        return last_action


def max_value(board):
    """
    Returns the maximum utility of the current board.
    """
    v = -math.inf
    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = max(v, min_value(result(board,action)))
    return v

def min_value(board):
    """
    Returns the minimum utility of the current board.
    """
    v = math.inf
    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = min(v, max_value(result(board,action)))
    return v


def get_matrix(matrix):
    matrix2 = []
    row = []
    for index,data in enumerate(matrix):
        if index == 3 or index == 6:
            matrix2.append(row)
            row = []
        if data == '0':
            row.append(None)
        else:
            row.append(data)
    matrix2.append(row)
    return matrix2