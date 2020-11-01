import pygame
from .constants import BLACK, WHITE, BLUE
from .board import Board

class Game:
    def __init__(self, win, rows, cols, square_size, with_ai):
        self.win = win
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.with_ai = with_ai
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


    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves:
            if piece == 0:
                tx = self.selected.row
                ty = self.selected.col
                self.board.move(self.selected, row, col)
                print(tx, ty, row, col, flush=True) 
                self.change_turn()
            elif piece.color != self.selected.color:
                self.board.remove(piece)
                tx = self.selected.row
                ty = self.selected.col
                self.board.move(self.selected, row, col)
                print(tx, ty, row, col, flush=True) 
                self.change_turn()
               


    def _ai_move(self, piece, row, col):
        temp = self.board.get_piece(row, col)
        if temp == 0:
            self.board.move(piece, row, col)
            self.change_turn()
        elif piece.color != temp.color:
            self.board.remove(temp)
            self.board.move(piece, row, col)
            self.change_turn()



    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * self.square_size + self.square_size//2, row * self.square_size + self.square_size//2), 15)

    def change_turn(self):

        self.valid_moves = {}

        if self.turn == BLACK:
            self.turn = WHITE
            if self.with_ai:
                self.get_move_from_ai()
        else:
            self.turn = BLACK


    def get_move_from_ai(self):
        # for row in range(self.rows):
        #     for col in range(self.cols):
        #         piece = self.board.get_piece(row, col)
        #         if piece == 0:
        #             print(0, flush=True) 
        #         elif piece.color == BLACK:
        #             print(1, flush=True)
        #         else:
        #             print(2, flush=True)

        sx = int(input())
        sy = int(input())
        tx = int(input())
        ty = int(input())
        piece = self.board.get_piece(sx, sy)
        self._ai_move(piece, tx, ty)

        
        
