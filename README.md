# Lines of Action

A desktop implementation of the abstract strategy game **[Lines of Action](https://en.wikipedia.org/wiki/Lines_of_Action)**
with a Pygame GUI and a C++ minimax AI opponent.

- 6x6 or 8x8 board
- Human vs Human, or Human vs AI (alpha-beta minimax, depth 5 on 6x6 / depth 4 on 8x8)
- Black (human) always moves first

## Rules in brief

Each turn a piece moves in a straight line (horizontal, vertical or diagonal) exactly as many
squares as there are pieces, of either colour, on that whole line. It may jump over its own
pieces but not over opponent pieces, and it captures by landing on an opponent piece.
You win when all of your remaining pieces form a single 8-connected group. If a move connects
both players at once, the player who moved wins.

## Requirements

| Tool | Notes |
|------|-------|
| Python 3.9 - 3.13 | `.python-version` pins **3.12.13** for [pyenv](https://github.com/pyenv/pyenv) |
| A C++17 compiler | `g++` or `clang++` (macOS: `xcode-select --install`; Debian/Ubuntu: `sudo apt install build-essential`) |
| `make` | optional, convenience only |

Python dependencies are listed in `requirements.txt` (`pygame`, `pygame-menu`) and
`requirements-dev.txt` (adds `pytest`).

## Quick start

```bash
git clone <this repo> && cd LinesOfAction
./run.sh
```

`run.sh` installs the pinned Python with pyenv if available, creates `.venv`, installs the
requirements, compiles the AI engine, and starts the game.

### Manual setup

```bash
# 1. Python (pyenv)
pyenv install -s 3.12.13          # picks up .python-version automatically afterwards
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

# 2. AI engine (only needed for Human vs AI)
make ai                           # or: g++ -O2 -std=c++17 ai/ai.cpp -o ai/loa_ai

# 3. Play
python main.py                    # or: python -m loa
```

If `ai/loa_ai` is missing when you start a Human vs AI game, the launcher compiles it for you
using the first of `$CXX`, `g++`, `clang++`, `c++` that it finds.

## Controls

- Click one of your pieces to see its legal moves (blue dots), then click a destination.
- `ESC` or closing the window returns to the menu.

## Running the tests

```bash
make test        # or: python -m pytest
```

The board-logic tests need no display. The engine test compiles `ai/ai.cpp` and plays one
exchange; it is skipped automatically when no C++ compiler is installed.

## Project layout

```
.
├── main.py              # entry point (python main.py)
├── run.sh               # one-shot setup + launch
├── Makefile             # ai / run / test / setup / clean
├── requirements.txt     # runtime deps
├── requirements-dev.txt # + pytest
├── .python-version      # pyenv pin
├── ai/
│   └── ai.cpp           # minimax engine (compiled to ai/loa_ai, git-ignored)
├── loa/
│   ├── __main__.py      # python -m loa
│   ├── menu.py          # start-up menu (board size, mode)
│   ├── play.py          # game loop, input handling, result screen
│   ├── game.py          # turn logic, move application, AI hand-off
│   ├── board.py         # board state, move generation, win detection
│   ├── piece.py         # piece model + drawing
│   ├── ai_client.py     # subprocess bridge to the C++ engine
│   └── constants.py
└── tests/
```

## How the GUI talks to the AI

`loa/ai_client.py` starts `ai/loa_ai` as a subprocess and exchanges plain integers over
stdin/stdout:

```
GUI -> AI : <rows> <cols>            once
GUI -> AI : <sx> <sy> <tx> <ty>      the human's move
AI  -> GUI: <sx> <sy> <tx> <ty>      the AI's reply, or -1 -1 -1 -1 if there is no move
```

The engine logs its thinking time to stderr.
