from flask import Flask, render_template, request, jsonify
import chess

from engine.game import choose_engine_move

app = Flask(__name__)

# Single global board for now (later you can add per-session boards)
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
    global board
    data = request.get_json()
    move_uci = data.get("move")

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
    global board
    if board.is_game_over():
        return jsonify({"error": "Game is already over"}), 400

    move = choose_engine_move(board, depth=3)
    board.push(move)

    return jsonify({
        "move": move.uci(),
        "fen": board.fen(),
        "game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else None,
    })


if __name__ == "__main__":
    app.run(debug=True)
