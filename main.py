import os
import pygame
import pygame_menu

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

from loa.constants import WIDTH, HEIGHT
from loa.play import Play


rows = 6
cols = 6
square_size = WIDTH // cols
with_ai = False

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Lines of Action')

 

def set_board_size(selected, value):

    global rows, cols, square_size

    if value == 1:
        rows = 6
        cols = 6
        square_size = WIDTH // cols

    elif value == 2:
        rows = 8
        cols = 8
        square_size = WIDTH // cols
  

def set_playing_mode(selected, value):
    global with_ai
    if value == 1:
        with_ai = False
    else:
        with_ai = True


def start_the_game():
    play = Play(win, rows, cols, square_size, with_ai)
    play.start_playing()



menu = pygame_menu.Menu(height=600,
                        width=600,
                        theme=pygame_menu.themes.THEME_BLUE,
                        title='Welcome')

menu.add_selector('Board Size: ', [('6x6', 1), ('8x8', 2)], onchange=set_board_size)
menu.add_selector('Playing mode: ', [('Human vs Human', 1), ('Human vs AI', 2)], onchange=set_playing_mode)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(win)