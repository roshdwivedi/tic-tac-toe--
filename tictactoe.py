"""
Tic Tac Toe Player
"""

import math
import random
from custom_errors import InvalidActionError
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
    # Scan board for entries and determine next player:

    X_count = 0
    O_count = 0
    EMPTY_count = 0

    for row in board:
      X_count += row.count(X)
      O_count += row.count(O)
      EMPTY_count += row.count(EMPTY)

    # If X has more squares than O, its O's turn:
    if X_count > O_count:
      return O

    # Otherwise it is X's turn:
    else:
      return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.

    i represents the board row, j the board column, both 0, 1 or 2

    The actions are are represented as the tuple (i, j) where the piece can be placed.
    """

    moves = set()

    for i in range(3):
      for j in range(3):
        if board[i][j] == EMPTY:
          moves.add((i, j))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    i = action[0]
    j = action[1]

    # Check move is valid:
    if i not in [0, 1, 2] or j not in [0, 1, 2]:
      raise InvalidActionError(action, board, 'Result function given an invalid board position for action: ')
    elif board[i][j] != EMPTY:
      raise InvalidActionError(action, board, 'Result function tried to perform invalid action on occupaied tile: ')

    # Make a deep copy of the board and update with the current player's move:
    board_copy = deepcopy(board)
    board_copy[i][j] = player(board)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check rows:
    for row in board:
      if row.count(X) == 3:
        return X
      if row.count(O) == 3:
        return O

    # Check columns:
    for j in range(3):
      column = ''
      for i in range(3):
        column += str(board[i][j])

      if column == 'XXX':
        return X
      if column == 'OOO':
        return O

    # Check Diagonals:
    diag1 = ''
    diag2 = ''
    j = 2

    for i in range(3):
      diag1 += str(board[i][i])
      diag2 += str(board[i][j])
      j -= 1

    if diag1 == 'XXX' or diag2 == 'XXX':
      return X
    elif diag1 == 'OOO' or diag2 == 'OOO':
      return O

    # Otherwise no current winner, return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Game is over if it is a winning board or all tiles are full (no actions):

    if winner(board) or not actions(board):
      return True
    else:
      return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == 'X':
      return 1
    elif winner(board) == 'O':
      return -1
    else:
      return 0


def minimax(board):
    if terminal(board):
      return None

    if player(board) == 'X':
      best_move = max_player(board)[1]
      return best_move
    else:
      best_move = min_player(board)[1]
      return best_move

def max_player(board, best_min = 10):

      if terminal(board):
        return (utility(board), None)

      value = -10
      best_action = None

      action_set = actions(board)

      while len(action_set) > 0:
        action = random.choice(tuple(action_set))
        action_set.remove(action)

        if best_min <= value:
          break
        min_player_result = min_player(result(board, action), value)
        if min_player_result[0] > value:
          best_action = action
          value = min_player_result[0]

      return (value, best_action)
      

def min_player(board, best_max = -10):
      if terminal(board):
        return (utility(board), None)

      value = 10
      best_action = None

      action_set = actions(board)

      while len(action_set) > 0:
        action = random.choice(tuple(action_set))
        action_set.remove(action)
        if best_max >= value:
          break
        max_player_result = max_player(result(board, action), value)
        if max_player_result[0] < value:
          best_action = action
          value = max_player_result[0]

      return (value, best_action)