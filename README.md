# Chess Project

Phase 1: Core chess engine in Python using `python-chess` with a simple alpha-beta search and command-line interface. Later phases will add a web UI and neural network evaluation.

## Structure

- `engine/eval.py` – basic evaluation function (material-based)
- `engine/search.py` – minimax/alpha-beta search on top of python-chess
- `engine/game.py` – command-line game loop (human vs engine)

## Getting Started

```bash
pip install -r requirements.txt
python -m engine.game
```
