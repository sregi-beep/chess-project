import chess

# ---------------------------------------------------------------------------
# Piece values (centipawns)
# ---------------------------------------------------------------------------
PIECE_VALUES = {
    chess.PAWN:   100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK:   500,
    chess.QUEEN:  900,
    chess.KING:   20000,
}

# ---------------------------------------------------------------------------
# Phase weights — used to blend MG/EG tables
# MAX_PHASE = 4*1 + 4*1 + 4*2 + 2*4 = 24
# ---------------------------------------------------------------------------
PHASE_WEIGHTS = {
    chess.KNIGHT: 1,
    chess.BISHOP: 1,
    chess.ROOK:   2,
    chess.QUEEN:  4,
}
MAX_PHASE = 24


def get_phase(board: chess.Board) -> float:
    """Return a float 1.0 (opening/middlegame) -> 0.0 (pure endgame)."""
    phase = 0
    for piece_type, weight in PHASE_WEIGHTS.items():
        phase += len(board.pieces(piece_type, chess.WHITE)) * weight
        phase += len(board.pieces(piece_type, chess.BLACK)) * weight
    return min(phase, MAX_PHASE) / MAX_PHASE


# ---------------------------------------------------------------------------
# Middlegame piece-square tables  (White perspective, rank8=index0)
# ---------------------------------------------------------------------------
PAWN_MG = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0,
]

KNIGHT_MG = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

BISHOP_MG = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

ROOK_MG = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0,
]

QUEEN_MG = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20,
]

KING_MG = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20,
]

# ---------------------------------------------------------------------------
# Endgame piece-square tables
# ---------------------------------------------------------------------------
PAWN_EG = [
     0,  0,  0,  0,  0,  0,  0,  0,
    80, 80, 80, 80, 80, 80, 80, 80,
    50, 50, 50, 50, 50, 50, 50, 50,
    30, 30, 30, 30, 30, 30, 30, 30,
    20, 20, 20, 20, 20, 20, 20, 20,
    10, 10, 10, 10, 10, 10, 10, 10,
     5,  5,  5,  5,  5,  5,  5,  5,
     0,  0,  0,  0,  0,  0,  0,  0,
]

KNIGHT_EG = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0,  5, 10, 10,  5,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5,  5, 10, 10,  5,  5,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

BISHOP_EG = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

ROOK_EG = [
     0,  0,  0,  0,  0,  0,  0,  0,
    10, 10, 10, 10, 10, 10, 10, 10,
     0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,
]

QUEEN_EG = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -10,  5,  5,  5,  5,  5,  0,-10,
      0,  0,  5,  5,  5,  5,  0, -5,
     -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20,
]

KING_EG = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50,
]

# ---------------------------------------------------------------------------
# Table lookup dicts
# ---------------------------------------------------------------------------
MG_TABLES = {
    chess.PAWN:   PAWN_MG,
    chess.KNIGHT: KNIGHT_MG,
    chess.BISHOP: BISHOP_MG,
    chess.ROOK:   ROOK_MG,
    chess.QUEEN:  QUEEN_MG,
    chess.KING:   KING_MG,
}

EG_TABLES = {
    chess.PAWN:   PAWN_EG,
    chess.KNIGHT: KNIGHT_EG,
    chess.BISHOP: BISHOP_EG,
    chess.ROOK:   ROOK_EG,
    chess.QUEEN:  QUEEN_EG,
    chess.KING:   KING_EG,
}


# ---------------------------------------------------------------------------
# Square index helper
# ---------------------------------------------------------------------------
def _square_index(square: int, is_white: bool) -> int:
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    row  = (7 - rank) if is_white else rank
    return row * 8 + file


# ---------------------------------------------------------------------------
# Tapered evaluation
# ---------------------------------------------------------------------------
def basic_eval(board: chess.Board) -> int:
    if board.is_checkmate():
        return -100000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    phase = get_phase(board)   # 1.0 = opening/MG, 0.0 = endgame
    score = 0

    for piece_type in PIECE_VALUES:
        mg_table = MG_TABLES.get(piece_type)
        eg_table = EG_TABLES.get(piece_type)

        for square in board.pieces(piece_type, chess.WHITE):
            mg_bonus = mg_table[_square_index(square, True)]  if mg_table else 0
            eg_bonus = eg_table[_square_index(square, True)]  if eg_table else 0
            positional = phase * mg_bonus + (1 - phase) * eg_bonus
            score += PIECE_VALUES[piece_type] + round(positional)

        for square in board.pieces(piece_type, chess.BLACK):
            mg_bonus = mg_table[_square_index(square, False)] if mg_table else 0
            eg_bonus = eg_table[_square_index(square, False)] if eg_table else 0
            positional = phase * mg_bonus + (1 - phase) * eg_bonus
            score -= PIECE_VALUES[piece_type] + round(positional)

    return score if board.turn == chess.WHITE else -score
