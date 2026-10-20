import pygame

from .constants import BLACK, WHITE, BLUE
from .board import Board
from .ai_client import AIClient


class Game:
    def __init__(self, win, rows, cols, square_size, with_ai):
        self.win = win
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.with_ai = with_ai
        self.ai = None
        self._init()

    def update(self):
        self.board.draw(self.win, self.turn)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board(self.rows, self.cols, self.square_size)
        self.turn = BLACK
        self.valid_moves = {}
        self.close()
        if self.with_ai:
            self.ai = AIClient(self.rows, self.cols)

    def close(self):
        if self.ai is not None:
            self.ai.close()
            self.ai = None

    def winner(self):
        return self.board.winner(self.turn)

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            self._move(row, col)
            self.selected = None
            self.valid_moves = {}
            return

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
        else:
            self.valid_moves = {}

    def _apply_move(self, piece, row, col):
        """Move `piece` to (row, col), capturing any opponent piece there."""
        target = self.board.get_piece(row, col)
        if target != 0:
            if target.color == piece.color:
                return False
            self.board.remove(target)
        self.board.move(piece, row, col)
        return True

    def _move(self, row, col):
        if not self.selected or (row, col) not in self.valid_moves:
            return
        sx, sy = self.selected.row, self.selected.col
        if self._apply_move(self.selected, row, col):
            self.change_turn()
            if self.with_ai and self.turn == WHITE and self.winner() is None:
                self._ai_turn(sx, sy, row, col)

    def _ai_turn(self, sx, sy, tx, ty):
        move = self.ai.get_move(sx, sy, tx, ty)
        if move is None:
            return
        asx, asy, atx, aty = move
        piece = self.board.get_piece(asx, asy)
        if piece == 0 or piece.color != WHITE:
            return
        if self._apply_move(piece, atx, aty):
            self.change_turn()

    def draw_valid_moves(self, moves):
        for row, col in moves:
            center = (
                col * self.square_size + self.square_size // 2,
                row * self.square_size + self.square_size // 2,
            )
            pygame.draw.circle(self.win, BLUE, center, 15)

    def change_turn(self):
        self.valid_moves = {}
        self.turn = WHITE if self.turn == BLACK else BLACK
