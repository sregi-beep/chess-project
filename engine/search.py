import math
import chess
from .eval import basic_eval, PIECE_VALUES

# ---------------------------------------------------------------------------
# Transposition table  { zobrist_hash: {'depth': int, 'score': int, 'flag': str} }
# flag: 'exact' | 'lower' (fail-high) | 'upper' (fail-low)
# ---------------------------------------------------------------------------
TT: dict = {}
TT_MAX_SIZE = 1_000_000   # cap to avoid unbounded memory growth


def tt_lookup(key: int, depth: int, alpha: float, beta: float):
    """Return cached score or None."""
    entry = TT.get(key)
    if entry is None or entry['depth'] < depth:
        return None
    score = entry['score']
    flag  = entry['flag']
    if flag == 'exact':               return score
    if flag == 'lower' and score >= beta:  return score
    if flag == 'upper' and score <= alpha: return score
    return None


def tt_store(key: int, depth: int, score: int, flag: str):
    if len(TT) >= TT_MAX_SIZE:
        TT.clear()   # simple replacement: clear when full
    TT[key] = {'depth': depth, 'score': score, 'flag': flag}


def clear_tt():
    TT.clear()


# ---------------------------------------------------------------------------
# MVV-LVA move ordering
# ---------------------------------------------------------------------------
def _move_order_key(board: chess.Board, move: chess.Move) -> int:
    score = 0
    if board.is_capture(move):
        victim   = board.piece_at(move.to_square)
        attacker = board.piece_at(move.from_square)
        victim_val   = PIECE_VALUES.get(victim.piece_type,   0) if victim   else 0
        attacker_val = PIECE_VALUES.get(attacker.piece_type, 0) if attacker else 0
        score += 10 * victim_val - attacker_val
    if move.promotion:
        score += PIECE_VALUES.get(move.promotion, 0)
    return score


# ---------------------------------------------------------------------------
# Quiescence search — only examines captures at leaf nodes
# ---------------------------------------------------------------------------
def quiescence(board: chess.Board, alpha: float, beta: float) -> float:
    stand_pat = basic_eval(board)
    if stand_pat >= beta:
        return beta
    if stand_pat > alpha:
        alpha = stand_pat

    captures = [
        m for m in board.legal_moves
        if board.is_capture(m)
    ]
    captures.sort(key=lambda m: _move_order_key(board, m), reverse=True)

    for move in captures:
        board.push(move)
        score = -quiescence(board, -beta, -alpha)
        board.pop()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha


# ---------------------------------------------------------------------------
# Negamax alpha-beta with:
#   - transposition table
#   - null move pruning (R=2)
#   - MVV-LVA move ordering
#   - quiescence at leaf nodes
# ---------------------------------------------------------------------------
def alpha_beta_search(
    board: chess.Board,
    depth: int,
    alpha: float,
    beta: float,
    allow_null: bool = True,
) -> float:

    # --- TT lookup ---
    key = board.zobrist_hash()
    tt_score = tt_lookup(key, depth, alpha, beta)
    if tt_score is not None:
        return tt_score

    # --- Leaf node ---
    if depth == 0 or board.is_game_over():
        return quiescence(board, alpha, beta)

    original_alpha = alpha

    # --- Null move pruning (skip when in check, depth must be >= 3) ---
    if allow_null and depth >= 3 and not board.is_check():
        board.push(chess.Move.null())
        null_score = -alpha_beta_search(board, depth - 3, -beta, -beta + 1, False)
        board.pop()
        if null_score >= beta:
            tt_store(key, depth, beta, 'lower')
            return beta

    # --- Move loop ---
    moves = sorted(
        board.legal_moves,
        key=lambda m: _move_order_key(board, m),
        reverse=True,
    )

    if not moves:
        return quiescence(board, alpha, beta)

    best_score = -math.inf
    for move in moves:
        board.push(move)
        score = -alpha_beta_search(board, depth - 1, -beta, -alpha, True)
        board.pop()

        if score > best_score:
            best_score = score
        if best_score > alpha:
            alpha = best_score
        if alpha >= beta:
            tt_store(key, depth, alpha, 'lower')
            return alpha

    # Store result in TT
    flag = 'exact' if best_score > original_alpha else 'upper'
    tt_store(key, depth, best_score, flag)
    return best_score
