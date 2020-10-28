import pygame

from .constants import WIDTH, HEIGHT
from .game import Game

 
class Play:
    def __init__(self, win, rows, cols, square_size):
        self.win = win
        self.square_size = square_size
        self.FPS = 60
        self.rows = rows
        self.cols = cols
        self.square_size = square_size

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        row = y // self.square_size
        col = x // self.square_size
        return row, col

    def start_playing(self):
        run = True
        clock = pygame.time.Clock()
        game = Game(self.win, self.rows, self.cols, self.square_size)

        while run:
            clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_row_col_from_mouse(pos)
                    game.select(row, col)

            game.update()
        
        pygame.quit()

    