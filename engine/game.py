import chess

from .search import alpha_beta_search


def choose_engine_move(board: chess.Board, depth: int = 3) -> chess.Move:
    """Choose the best move for the side to move using alpha-beta search."""
    best_move = None
    best_value = float('-inf')

    for move in board.legal_moves:
        board.push(move)
        score = -alpha_beta_search(board, depth - 1, float('-inf'), float('inf'))
        board.pop()

        if score > best_value or best_move is None:
            best_value = score
            best_move = move

    return best_move


def play_cli_game():
    board = chess.Board()
    print("Welcome to the Phase 1 chess engine (CLI).\n")
    print(board)

    while not board.is_game_over():
        if board.turn:
            # White (human)
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
            # Black (engine)
            print("\nEngine thinking...")
            move = choose_engine_move(board, depth=3)
            print(f"Engine plays: {move}")
            board.push(move)

        print("\n", board, sep="")

    print("\nGame over.")
    print("Result:", board.result())


if __name__ == "__main__":
    play_cli_game()
