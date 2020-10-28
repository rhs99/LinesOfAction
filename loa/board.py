import pygame
from .constants import BLACK, RED, WHITE, BLUE, YELLOW1, YELLOW2
from .piece import Piece

class Board:
    def __init__(self, win, rows, cols, square_size):
        self.board = []
        self.black_left = self.white_left = (rows-2)*2
        self.win = win
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.create_board()

        
    
    def draw_squares(self, win):
        win.fill(YELLOW2)
        for row in range(self.rows):
            for col in range(row % 2, self.cols, 2):
                pygame.draw.rect(win, YELLOW1, (row*self.square_size, col *self.square_size, self.square_size, self.square_size))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

         

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                self.board[row].append(0)

        for col in range(1, self.cols-1):
            self.board[0][col] = Piece(0, col, BLACK, self.square_size)
            self.board[self.rows-1][col] = Piece(self.rows-1, col, BLACK, self.square_size)

        for row in range(1, self.rows-1):
            self.board[row][0] = Piece(row, 0, WHITE, self.square_size)
            self.board[row][self.cols-1] = Piece(row, self.cols-1, WHITE, self.square_size)

    
    def draw(self, win, turn):
        self.draw_squares(win)
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win, turn)

    def remove(self, piece):
        self.board[piece.row][piece.col] = 0
        if piece != 0:
            if piece.color == BLACK:
                self.black_left -= 1
            else:
                self.white_left -= 1
    
    def winner(self):
        if self.black_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK
        return None 

        
    
    def get_valid_moves(self, piece):
        moves = {}
        moves.update(self._traverse_horizontal(piece))
        moves.update(self._traverse_verticle(piece))
        moves.update(self._traverse_diagonal1(piece))
        moves.update(self._traverse_diagonal2(piece))
        return moves


    def _traverse_horizontal(self, piece):
        moves = {}

        cur_r = piece.row
        piece_cnt = 1

        cur_c = piece.col
        while cur_c+1 < self.cols:
            cur_c += 1
            if self.board[cur_r][cur_c] != 0:
                piece_cnt += 1
        
        cur_c = piece.col
        while cur_c-1 >= 0:
            cur_c -= 1
            if self.board[cur_r][cur_c] != 0:
                piece_cnt += 1

        cur_c = piece.col
        if cur_c + piece_cnt < self.cols:
            temp = piece_cnt-1
            opp_cnt = 0
            while temp>0:
                cur_c += 1
                if self.board[cur_r][cur_c] != 0 and self.board[cur_r][cur_c].color != piece.color:
                    opp_cnt += 1
                temp -= 1
            if opp_cnt == 0 and (self.board[cur_r][piece.col + piece_cnt]==0 or self.board[cur_r][piece.col + piece_cnt].color != piece.color):
                moves[(cur_r, piece.col + piece_cnt)] = self.board[cur_r][piece.col + piece_cnt]

        cur_c = piece.col
        if cur_c - piece_cnt >= 0:
            temp = piece_cnt-1
            opp_cnt = 0
            while temp>0:
                cur_c -= 1
                if self.board[cur_r][cur_c] != 0 and self.board[cur_r][cur_c].color != piece.color:
                    opp_cnt += 1
                temp -= 1
            if opp_cnt == 0 and (self.board[cur_r][piece.col - piece_cnt]==0 or self.board[cur_r][piece.col - piece_cnt].color != piece.color):
                moves[(cur_r, piece.col - piece_cnt)] = self.board[cur_r][piece.col - piece_cnt]

        return moves


    def _traverse_verticle(self, piece):
        moves = {}

        cur_c = piece.col
        piece_cnt = 1

        cur_r = piece.row
        while cur_r+1 < self.rows:
            cur_r += 1
            if self.board[cur_r][cur_c] != 0:
                piece_cnt += 1
        
        cur_r = piece.row
        while cur_r-1 >= 0:
            cur_r -= 1
            if self.board[cur_r][cur_c] != 0:
                piece_cnt += 1
 
        cur_r = piece.row
        if cur_r + piece_cnt < self.rows:
            temp = piece_cnt-1
            opp_cnt = 0
            while temp>0:
                cur_r += 1
                if self.board[cur_r][cur_c] != 0 and self.board[cur_r][cur_c].color != piece.color:
                    opp_cnt += 1
                temp -= 1
            if opp_cnt == 0 and (self.board[piece.row + piece_cnt][piece.col]==0 or self.board[piece.row + piece_cnt][piece.col].color != piece.color):
                moves[(piece.row + piece_cnt, piece.col)] = self.board[piece.row + piece_cnt][piece.col]

        cur_r = piece.row
        if cur_r - piece_cnt >= 0:
            temp = piece_cnt-1
            opp_cnt = 0
            while temp>0:
                cur_r -= 1
                if self.board[cur_r][cur_c] != 0 and self.board[cur_r][cur_c].color != piece.color:
                    opp_cnt += 1
                temp -= 1
            if opp_cnt == 0 and (self.board[piece.row - piece_cnt][piece.col]==0 or self.board[piece.row - piece_cnt][piece.col].color != piece.color):
                moves[(piece.row - piece_cnt, piece.col)] = self.board[piece.row - piece_cnt][piece.col]

        return moves




    def _traverse_diagonal1(self, piece):
        moves = {}

        piece_cnt = 1

        cur_r = piece.row
        cur_c = piece.col

        while cur_r-1>=0 and cur_c+1<self.cols:
            cur_r -= 1
            cur_c += 1
            if self.board[cur_r][cur_c] != 0:
                piece_cnt += 1

        cur_r = piece.row
        cur_c = piece.col

        while cur_r+1<self.rows and cur_c-1>=0:
            cur_r += 1
            cur_c -= 1
            if self.board[cur_r][cur_c] != 0:
                piece_cnt += 1

        if piece.row-piece_cnt >=0 and piece.col + piece_cnt < self.cols:
            temp = piece_cnt-1
            cur_r = piece.row
            cur_c = piece.col
            opp_cnt = 0
            while temp > 0:
                cur_r -= 1
                cur_c += 1
                if self.board[cur_r][cur_c] != 0 and self.board[cur_r][cur_c].color != piece.color:
                    opp_cnt += 1
                temp -= 1
            if opp_cnt == 0 and (self.board[piece.row - piece_cnt][piece.col + piece_cnt]==0 or self.board[piece.row - piece_cnt][piece.col + piece_cnt].color != piece.color):
                moves[(piece.row - piece_cnt, piece.col + piece_cnt)] = self.board[piece.row - piece_cnt][piece.col + piece_cnt]

        if piece.row + piece_cnt < self.rows and piece.col - piece_cnt >= 0:
            temp = piece_cnt-1
            cur_r = piece.row
            cur_c = piece.col
            opp_cnt = 0
            while temp > 0:
                cur_r += 1
                cur_c -= 1
                if self.board[cur_r][cur_c] != 0 and self.board[cur_r][cur_c].color != piece.color:
                    opp_cnt += 1
                temp -= 1
            if opp_cnt == 0 and (self.board[piece.row + piece_cnt][piece.col - piece_cnt]==0 or self.board[piece.row + piece_cnt][piece.col - piece_cnt].color != piece.color):
                moves[(piece.row + piece_cnt, piece.col - piece_cnt)] = self.board[piece.row + piece_cnt][piece.col - piece_cnt]

          
        return moves

    def _traverse_diagonal2(self, piece):
        moves = {}

        piece_cnt = 1

        cur_r = piece.row
        cur_c = piece.col

        while cur_r-1 >= 0 and cur_c-1 >= 0:
            cur_r -= 1
            cur_c -= 1
            if self.board[cur_r][cur_c] != 0:
                piece_cnt += 1

        cur_r = piece.row
        cur_c = piece.col

        while cur_r+1 < self.rows and cur_c+1 < self.cols:
            cur_r += 1
            cur_c += 1
            if self.board[cur_r][cur_c] != 0:
                piece_cnt += 1

        if piece.row - piece_cnt >=0 and piece.col - piece_cnt >= 0:
            temp = piece_cnt-1
            cur_r = piece.row
            cur_c = piece.col
            opp_cnt = 0

            while temp > 0:
                cur_r -= 1
                cur_c -= 1
                if self.board[cur_r][cur_c] != 0 and self.board[cur_r][cur_c].color != piece.color:
                    opp_cnt += 1
                temp -= 1

            if opp_cnt == 0 and (self.board[piece.row - piece_cnt][piece.col - piece_cnt] == 0 or self.board[piece.row - piece_cnt][piece.col - piece_cnt].color != piece.color):
                moves[(piece.row - piece_cnt, piece.col - piece_cnt)] = self.board[piece.row - piece_cnt][piece.col - piece_cnt]

        if piece.row + piece_cnt < self.rows and piece.col + piece_cnt < self.cols:
            temp = piece_cnt-1
            cur_r = piece.row
            cur_c = piece.col
            opp_cnt = 0
            while temp > 0:
                cur_r += 1
                cur_c += 1
                if self.board[cur_r][cur_c] != 0 and self.board[cur_r][cur_c].color != piece.color:
                    opp_cnt += 1
                temp -= 1
            if opp_cnt == 0 and (self.board[piece.row + piece_cnt][piece.col + piece_cnt] == 0 or self.board[piece.row + piece_cnt][piece.col + piece_cnt].color != piece.color):
                moves[(piece.row + piece_cnt, piece.col + piece_cnt)] = self.board[piece.row + piece_cnt][piece.col + piece_cnt]

          
        return moves