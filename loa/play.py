import pygame

pygame.init() 


from .constants import WIDTH, HEIGHT, BLACK, WHITE, RED, BLUE, GREEN
from .game import Game

 
class Play:
    def __init__(self, win, rows, cols, square_size, with_ai):
        self.win = win
        self.square_size = square_size
        self.FPS = 60
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.with_ai = with_ai
        self.font = pygame.font.Font('freesansbold.ttf', 32) 
  

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        row = y // self.square_size
        col = x // self.square_size
        return row, col

   
            

    def start_playing(self):
        run = True
        clock = pygame.time.Clock()
        game = Game(self.win, self.rows, self.cols, self.square_size, self.with_ai)
        finished = False

        while run:

            clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_row_col_from_mouse(pos)
                    game.select(row, col)

            if not finished:
                game.update()
            else:
                pygame.display.update()

            result  = game.winner()
            if result != None:
                if result == BLACK:
                    text = self.font.render('BLACK WINS!', True, GREEN, )
                else:
                    text = self.font.render('WHITE WINS!', True, GREEN, )

                textRect = text.get_rect()  
                textRect.center = (WIDTH// 2, HEIGHT // 2) 
                self.win.fill(BLACK)
                self.win.blit(text, textRect) 
                finished = True

           
        

    