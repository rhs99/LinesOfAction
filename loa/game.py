import pygame
from .constants import BLACK, WHITE, BLUE
from .board import Board

class Game:
    def __init__(self, win, rows, cols, square_size):
        self.win = win
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self._init()
    
    def update(self):
        self.board.draw(self.win, self.turn)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board(self.win, self.rows, self.cols, self.square_size)
        self.turn = BLACK
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
        else:
            self.valid_moves = {}


    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves:
            if piece == 0:
                self.board.move(self.selected, row, col)
                self.change_turn()
                return True
            elif piece.color != self.selected.color:
                self.board.remove(piece)
                self.board.move(self.selected, row, col)
                self.change_turn()
                return True

        return False


    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * self.square_size + self.square_size//2, row * self.square_size + self.square_size//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK