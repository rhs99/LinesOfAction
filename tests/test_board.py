"""Pure-logic tests for the board (no display needed)."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pytest

from loa.board import Board
from loa.constants import BLACK, WHITE


def color_at(board, r, c):
    p = board.get_piece(r, c)
    return None if p == 0 else p.color


@pytest.mark.parametrize("n", [6, 8])
def test_initial_setup(n):
    b = Board(n, n, 800 // n)
    assert b.black_left == b.white_left == (n - 2) * 2
    for c in range(1, n - 1):
        assert color_at(b, 0, c) == BLACK
        assert color_at(b, n - 1, c) == BLACK
    for r in range(1, n - 1):
        assert color_at(b, r, 0) == WHITE
        assert color_at(b, r, n - 1) == WHITE
    for corner in [(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)]:
        assert color_at(b, *corner) is None


def test_no_winner_at_start():
    b = Board(6, 6, 100)
    assert b.winner(BLACK) is None


def test_initial_valid_moves_for_top_edge_piece():
    b = Board(6, 6, 100)
    piece = b.get_piece(0, 1)
    moves = set(b.get_valid_moves(piece))
    # Vertical line has 2 pieces (rows 0 and 5): move 2 down.
    assert (2, 1) in moves
    # Horizontal line has 4 pieces: jumping 4 to the right over own pieces lands on the empty corner.
    assert (0, 5) in moves
    # ...but 4 to the left is off-board.
    assert (0, -3) not in moves
    # Diagonal towards (2, 3): line (0,1)-(1,2)-(2,3)-(3,4)-(4,5) has 2 pieces -> (2,3).
    assert (2, 3) in moves
    # Diagonal towards (1, 0) has 2 pieces [(0,1),(1,0)]; landing would be (2,-1): off-board.
    assert all(0 <= r < 6 and 0 <= c < 6 for r, c in moves)


def test_cannot_jump_over_opponent():
    b = Board(6, 6, 100)
    # Clear a row and set up: BLACK at (2,0), WHITE at (2,1), empty beyond.
    for r in range(6):
        for c in range(6):
            b.board[r][c] = 0
    from loa.piece import Piece

    b.board[2][0] = Piece(2, 0, BLACK, 100)
    b.board[2][1] = Piece(2, 1, WHITE, 100)
    b.black_left, b.white_left = 1, 1
    moves = b.get_valid_moves(b.board[2][0])
    # Horizontal count = 2, target (2,2); path crosses WHITE at (2,1) -> illegal.
    assert (2, 2) not in moves


def test_capture_and_connectivity():
    from loa.piece import Piece

    b = Board(6, 6, 100)
    for r in range(6):
        for c in range(6):
            b.board[r][c] = 0
    b.board[2][2] = Piece(2, 2, BLACK, 100)
    b.board[2][3] = Piece(2, 3, BLACK, 100)
    b.board[4][4] = Piece(4, 4, WHITE, 100)
    b.board[0][0] = Piece(0, 0, WHITE, 100)
    b.black_left, b.white_left = 2, 2

    assert b.is_connected(b.board[2][2]) is True
    assert b.is_connected(b.board[4][4]) is False
    # Only black is connected -> black wins regardless of whose turn.
    assert b.winner(WHITE) == BLACK

    b.remove(b.board[0][0])
    assert b.white_left == 1
    assert b.is_connected(b.board[4][4]) is True
    # Both connected: the player who just moved (not `turn`) wins.
    assert b.winner(BLACK) == WHITE
    assert b.winner(WHITE) == BLACK


def test_move_updates_board_and_piece():
    b = Board(6, 6, 100)
    piece = b.get_piece(0, 1)
    b.move(piece, 2, 1)
    assert b.get_piece(0, 1) == 0
    assert b.get_piece(2, 1) is piece
    assert (piece.row, piece.col) == (2, 1)
