# -*- coding: utf-8 -*-
import sys
from models.move import Move
import random

class CornerPlayer:
  def __init__(self, color):
    self.color = color

  def play(self, board):

    score = board.score()

    really_important_moves = [Move(1,1), Move(1,8), Move(8,1), Move(8,8)]

    forbiden_moves = [Move(1,2), Move(2,2), Move(2,1),
                        Move(1,7), Move(2,7), Move(2,8),
                        Move(7,1), Move(7,2), Move(8,2),
                        Move(8,7), Move(7,7), Move(7,8)]

    if(score[0] + score[1] < 45):

      moves = board.valid_moves(self.color)
      moves = self.filter_unique_moves(moves)

      best_move = []
      score_goal = 2
      lowest_score_until_now = sys.maxint

      for move in range(len(moves)):
        if moves[move] in forbiden_moves:
          continue
        if moves[move] in really_important_moves:
          return moves[move]
        
        local_board = board.get_clone()
        local_board.play(moves[move], self.color)
        local_score = local_board.score()

        if self.color == '■':
          if local_score[0] < 2:
            continue

          opp_moves = local_board.valid_moves(board._opponent(self.color))
          opp_moves = self.filter_unique_moves(opp_moves)
          pre_corner_boards = self.calculate_pre_corner_boards(local_board, opp_moves, 3, board._opponent(self.color))
          
          if pre_corner_boards == None:
            pre_corner_boards = 0

          theta =  0.5
          heuristic = theta * pre_corner_boards + (1 - theta) * local_score[0]
          if local_score[0] == 2:
            lowest_score_until_now = local_score[0]
            best_move = moves[move]

        else:
          if local_score[1] < 2:
            continue

          opp_moves = local_board.valid_moves(board._opponent(self.color))
          opp_moves = self.filter_unique_moves(opp_moves)
          pre_corner_boards = self.calculate_pre_corner_boards(local_board, opp_moves, 3, board._opponent(self.color))
          
          if pre_corner_boards == None:
            pre_corner_boards = 0

          theta =  0.5
          heuristic = theta * pre_corner_boards + (1 - theta) * local_score[1]
          
          if local_score[0] == 2:
            lowest_score_until_now = local_score[0]
            best_move = moves[move]

        if heuristic < lowest_score_until_now:
          lowest_score_until_now = heuristic
          best_move = moves[move]


      if best_move == []:
        best_move = random.choice(moves)

      return best_move



    else:

      moves = board.valid_moves(self.color)
      moves = self.filter_unique_moves(moves)

      best_move = []
      highest_score_until_now = -sys.maxint - 1

      for move in range(len(moves)):
        if moves[move] in forbiden_moves:
          continue
        if moves[move] in really_important_moves:
          return moves[move]
        
        local_board = board.get_clone()
        local_board.play(moves[move], self.color)
        local_score = local_board.score()

        if self.color == '■':
          if local_score[0] > highest_score_until_now:
            highest_score_until_now = local_score[0]
            best_move = moves[move]
        else:
          if local_score[1] > highest_score_until_now:
            highest_score_until_now = local_score[1]
            best_move = moves[move]


      if best_move == []:
        best_move = random.choice(moves)

      return best_move

  def filter_unique_moves(self, moves):
    unique_moves = []

    for move in moves:
      if move not in unique_moves:
        unique_moves.append(move)

    return unique_moves

  def calculate_pre_corner_boards(self, board, moves, level, color):

    forbiden_moves = [Move(1,2), Move(2,2), Move(2,1),
                        Move(1,7), Move(2,7), Move(2,8),
                        Move(7,1), Move(7,2), Move(8,2),
                        Move(8,7), Move(7,7), Move(7,8)]

    pre_corner_boards = 0
    level = level - 1

    if level == 0:
      return 0

    if self.color == color:

      for move in moves:
        
        local_board = board.get_clone()

        if move in forbiden_moves:
          pre_corner_boards += 1

        local_board.play(move, self.color)
        opp_moves = local_board.valid_moves(board._opponent(self.color))
        opp_moves = self.filter_unique_moves(opp_moves)

        pre_corner_boards += self.calculate_pre_corner_boards(local_board, opp_moves, level, board._opponent(self.color))
      return pre_corner_boards

    else:

      for move in moves:
        local_board = board.get_clone()

        local_board.play(move, board._opponent(self.color))

        new_moves = local_board.valid_moves(self.color)
        new_moves = self.filter_unique_moves(new_moves)

        pre_corner_boards += self.calculate_pre_corner_boards(local_board, new_moves, level, self.color)

        return pre_corner_boards
