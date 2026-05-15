from flask import Flask, render_template, request, jsonify
import chess
from engine.game import choose_engine_move

app = Flask(__name__)

# Global board — stays in sync via FEN from client
board = chess.Board()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/reset", methods=["POST"])
def reset():
    global board
    board = chess.Board()
    return jsonify({"fen": board.fen()})


@app.route("/move", methods=["POST"])
def player_move():
    """Apply player's move. Expects JSON: {move: 'e2e4'} or {fen: '...'}"""
    global board
    data = request.get_json(force=True) or {}

    # If client sends current FEN, sync server board first
    fen = data.get("fen")
    if fen:
        try:
            board = chess.Board(fen)
        except Exception:
            return jsonify({"error": "Invalid FEN"}), 400

    move_uci = data.get("move")
    if not move_uci:
        # No move to apply — just confirm sync
        return jsonify({
            "fen": board.fen(),
            "game_over": board.is_game_over(),
            "result": board.result() if board.is_game_over() else None,
        })

    try:
        move = chess.Move.from_uci(move_uci)
    except ValueError:
        return jsonify({"error": "Invalid move format"}), 400

    if move not in board.legal_moves:
        return jsonify({"error": "Illegal move"}), 400

    board.push(move)
    return jsonify({
        "fen": board.fen(),
        "game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else None,
    })


@app.route("/engine-move", methods=["POST"])
def engine_move():
    """Sync board from FEN, run engine, return best move."""
    global board
    data = request.get_json(force=True) or {}

    # Sync board from client FEN so we are always consistent
    fen = data.get("fen")
    if fen:
        try:
            board = chess.Board(fen)
        except Exception:
            return jsonify({"error": "Invalid FEN"}), 400

    if board.is_game_over():
        return jsonify({"error": "Game is already over"}), 400

    if not list(board.legal_moves):
        return jsonify({"error": "No legal moves"}), 400

    try:
        move = choose_engine_move(board, depth=3)
        board.push(move)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "move": move.uci(),
        "fen": board.fen(),
        "game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else None,
    })


if __name__ == "__main__":
    app.run(debug=True)
