import math
import chess
from .eval import basic_eval, PIECE_VALUES


def _move_order_key(board: chess.Board, move: chess.Move) -> int:
    """Score a move for ordering: higher = search first.
    Captures ordered by MVV-LVA (most valuable victim, least valuable attacker).
    """
    score = 0
    if board.is_capture(move):
        victim = board.piece_at(move.to_square)
        attacker = board.piece_at(move.from_square)
        victim_val = PIECE_VALUES.get(victim.piece_type, 0) if victim else 0
        attacker_val = PIECE_VALUES.get(attacker.piece_type, 0) if attacker else 0
        score += 10 * victim_val - attacker_val
    if move.promotion:
        score += PIECE_VALUES.get(move.promotion, 0)
    return score


def alpha_beta_search(
    board: chess.Board,
    depth: int,
    alpha: float,
    beta: float,
) -> float:
    """Negamax alpha-beta search.
    Returns a score from the perspective of the side to move.
    Positive = good for side to move.
    """
    if depth == 0 or board.is_game_over():
        return basic_eval(board)

    # Order moves: try captures and promotions first
    moves = sorted(
        board.legal_moves,
        key=lambda m: _move_order_key(board, m),
        reverse=True,
    )

    value = -math.inf
    for move in moves:
        board.push(move)
        score = -alpha_beta_search(board, depth - 1, -beta, -alpha)
        board.pop()

        if score > value:
            value = score
        if value > alpha:
            alpha = value
        if alpha >= beta:
            break  # beta cutoff

    return value
