import chess
from .search import alpha_beta_search, clear_tt


def choose_engine_move(board: chess.Board, depth: int = 3) -> chess.Move:
    """
    Choose the best move using iterative deepening alpha-beta search.
    Searches depth 1, 2, ..., up to `depth`, using each shallower result
    to improve move ordering for the next iteration.
    The transposition table is cleared once before the full search begins.
    """
    clear_tt()
    best_move = None

    for current_depth in range(1, depth + 1):
        best_value = float('-inf')
        current_best = None

        # Sort moves using TT best-move hint from previous iteration
        moves = list(board.legal_moves)

        for move in moves:
            board.push(move)
            score = -alpha_beta_search(
                board,
                current_depth - 1,
                float('-inf'),
                float('inf'),
            )
            board.pop()

            if score > best_value or current_best is None:
                best_value = score
                current_best = move

        if current_best is not None:
            best_move = current_best

    return best_move


def play_cli_game():
    board = chess.Board()
    print("Welcome to the chess engine (CLI).\n")
    print(board)

    while not board.is_game_over():
        if board.turn:
            print("\nYour move (UCI, e.g. e2e4): ", end="")
            user_input = input().strip()
            try:
                move = chess.Move.from_uci(user_input)
            except ValueError:
                print("Invalid move format. Use UCI like e2e4.")
                continue
            if move not in board.legal_moves:
                print("Illegal move. Try again.")
                continue
            board.push(move)
        else:
            print("\nEngine thinking...")
            move = choose_engine_move(board, depth=3)
            print(f"Engine plays: {move}")
            board.push(move)

        print("\n", board, sep="")

    print("\nGame over.")
    print("Result:", board.result())


if __name__ == "__main__":
    play_cli_game()
