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

win = pygame.display.set_mode((WIDTH, HEIGHT))

 

def set_board_size(selected, value):
    if value == 2:
        global rows 
        rows = 8
        global cols 
        cols = 8
        global square_size
        square_size = WIDTH // cols
  

def set_playing_mode(selected, value):
    """
    Set the difficulty of the game.
    """
    print('Set difficulty to {} ({})'.format(selected[0], value))


def start_the_game():
    play = Play(win, rows, cols, square_size)
    play.start_playing()



menu = pygame_menu.Menu(height=600,
                        width=600,
                        theme=pygame_menu.themes.THEME_BLUE,
                        title='Welcome')

#menu.add_text_input('Name: ', default='John Doe')
menu.add_selector('Board Size: ', [('6x6', 1), ('8x8', 2)], onchange=set_board_size)
menu.add_selector('Playing mode: ', [('Human vs Human', 1), ('Human vs AI', 2)], onchange=set_playing_mode)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(win)