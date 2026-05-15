import chess

# Piece values in centipawns
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
}


def material_count(board: chess.Board) -> int:
    """Return a simple material count from the perspective of the side to move.

    Positive means good for side to move, negative means bad.
    """
    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, board.turn)) * value
        score -= len(board.pieces(piece_type, not board.turn)) * value
    return score


def basic_eval(board: chess.Board) -> int:
    """Basic evaluation function.

    For now, just returns the material difference (centipawns) for side to move.
    """
    # Handle terminal positions explicitly
    if board.is_checkmate():
        # If it's checkmate and it's our turn, we are lost; large negative score
        return -100000
    if board.is_stalemate() or board.is_insufficient_material() or board.can_claim_draw():
        return 0

    return material_count(board)
