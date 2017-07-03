import sys
from models.move import Move

class CornerPlayer:
  def __init__(self, color):
    self.color = color

  def play(self, board):

    moves = board.valid_moves(self.color)

    unique_moves = []
    move_values = []

    for move in moves:
      if move not in unique_moves:
        if move == Move(1,1) or move == Move(1,8) or move == Move(8,1) or move == Move(8,8):
          return move
        unique_moves.append(move)
        move_values.append(0)

    best_move = []
    fewest_moves = sys.maxint

    alfa = -sys.maxint - 1
    beta = sys.maxint

    for move in range(len(unique_moves)):
      move_values[move] = self.alfa_beta2(board, moves[move], 4, alfa, beta, self.color)

      if move_values[move] < fewest_moves:
        fewest_moves = move_values[move]
        best_move = moves[move]

    if best_move == []:
      best_move = unique_moves[0]

    return best_move

  def get_unique_player_moves(self, board, move, color):

    unique_next_moves = []

    board.play(move, board._opponent(color))
    next_moves = board.valid_moves(color)

    for move in next_moves:
      if move not in unique_next_moves:
        unique_next_moves.append(move)

    return unique_next_moves

  def get_unique_player_moves_from_scratch(self, board, color):

    unique_next_moves = []

    next_moves = board.valid_moves(color)

    for move in next_moves:
      if move not in unique_next_moves:
        unique_next_moves.append(move)

    return unique_next_moves

  def alfa_beta2(self, board, move, level, alfa, beta, color):
    next_level = level - 1

    unique_next_moves = self.get_unique_player_moves(board, move, color)

    if unique_next_moves == []:
      if self.color == color:
        color = board._opponent(self.color)
      else:
        color = self.color
      unique_next_moves = self.get_unique_player_moves_from_scratch(board, color)

    if level == 0 or unique_next_moves == []:
      return len(unique_next_moves)

    if self.color != color:
      v = -sys.maxint - 1

      for move in range(len(unique_next_moves)):
        local_board = board.get_clone()
        a = self.alfa_beta2(local_board, unique_next_moves[move], next_level, alfa, beta, self.color)
        v = max(v,a)
        alfa = max(v,alfa)
        if beta <= alfa:
          break
      return v

    else:
      v = sys.maxint

      for move in range(len(unique_next_moves)):
        local_board = board.get_clone()
        v = min(v, self.alfa_beta2(local_board, unique_next_moves[move], next_level, alfa, beta, board._opponent(self.color)))
        beta = min(v,beta)
        if beta <= alfa:
          break
      return v