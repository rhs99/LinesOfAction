from .constants import GREY, RED
import pygame

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color, square_size):
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.square_size = square_size
        self.calc_pos()

    def calc_pos(self):
        self.x = self.square_size * self.col + self.square_size // 2
        self.y = self.square_size * self.row + self.square_size // 2

    
    
    def draw(self, win, turn):
        radius = self.square_size//2 - self.PADDING
        if self.color == turn:
            pygame.draw.circle(win, RED, (self.x, self.y), radius + self.OUTLINE + 3)
        else:
            pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)

        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

        

        

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)