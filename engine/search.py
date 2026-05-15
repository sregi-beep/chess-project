import math
import chess

from .eval import basic_eval


def alpha_beta_search(board: chess.Board, depth: int, alpha: float, beta: float) -> float:
    """Alpha-beta search that returns a score for the given board.

    Assumes the side to move is the maximizing player.
    """
    if depth == 0 or board.is_game_over():
        return basic_eval(board)

    value = -math.inf
    for move in board.legal_moves:
        board.push(move)
        score = -alpha_beta_search(board, depth - 1, -beta, -alpha)
        board.pop()

        if score > value:
            value = score
        if value > alpha:
            alpha = value
        if alpha >= beta:
            break

    return value
