"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None

"""
All the different possibilities to win
"""
cell_combination = {(0, 0): [[(0, 1), (0, 2)], [(1, 0), (2, 0)], [(1, 1), (2, 2)]],
                    (0, 2): [[(1, 2), (2, 2)], [(1, 1), (2, 0)]],
                    (1, 1): [[(0, 1), (2, 1)], [(1, 0), (1, 2)]],
                    (2, 0): [[(2, 1), (2, 2)]]}


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
    final_sum = sum(sum(1 for cell in row if cell == EMPTY) for row in board)
    return O if final_sum % 2 == 0 else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] < 0 or action[1] < 0:
        raise ValueError("Out of bounds move")
    new_board = copy.deepcopy(board)
    if new_board[action[0]][action[1]] is not EMPTY:
        raise ValueError("Illegal move")
    p = player(new_board)
    new_board[action[0]][action[1]] = p
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if sum(sum(1 for cell in row if cell == EMPTY) for row in board) > 4:
        return None

    for key, value in cell_combination.items():
        cell_value = board[key[0]][key[1]]
        if cell_value is not EMPTY:
            for cell in value:
                result = sum(1 for cell_result in cell
                             if board[cell_result[0]][cell_result[1]] == cell_value)
                if result == 2:
                    return cell_value

    return None


def terminal(board: object) -> object:
    """
    Returns True if game is over, False otherwise.
    """
    if sum(sum(1 for cell in row if cell is not EMPTY) for row in board) == 9:
        return True
    return winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win is X:
        return 1
    elif win is O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)
    alpha = -math.inf
    beta = math.inf
    if current_player == X:
        return max_value(board, alpha, beta)[1]
    else:
        return min_value(board, alpha, beta)[1]


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None
    v = float("-inf")
    best_action = None
    for action in actions(board):
        min_v = min_value(result(board, action), alpha, beta)[0]
        if v < min_v:
            v = min_v
            best_action = action
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    return v, best_action


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None
    v = float("inf")
    best_action = None
    for action in actions(board):
        max_v = max_value(result(board, action), alpha, beta)[0]
        if v > max_v:
            v = max_v
            best_action = action
        beta = min(beta, v)
        if alpha >= beta:
            break
    return v, best_action


boardd = initial_state()
kl = player(boardd)
print(minimax(boardd))
