"""Start-up menu: choose board size and playing mode, then launch a game."""
import os

os.environ.setdefault("SDL_VIDEO_CENTERED", "1")

import pygame
import pygame_menu

from .constants import WIDTH, HEIGHT
from .play import Play


class Settings:
    def __init__(self):
        self.rows = 6
        self.cols = 6
        self.with_ai = False

    @property
    def square_size(self):
        return WIDTH // self.cols


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lines of Action")

    settings = Settings()

    def set_board_size(_selected, size):
        settings.rows = settings.cols = size

    def set_playing_mode(_selected, with_ai):
        settings.with_ai = with_ai

    def start_the_game():
        play = Play(win, settings.rows, settings.cols, settings.square_size, settings.with_ai)
        play.start_playing()

    menu = pygame_menu.Menu(
        height=600,
        width=600,
        theme=pygame_menu.themes.THEME_BLUE,
        title="Lines of Action",
    )
    menu.add.selector("Board Size: ", [("6x6", 6), ("8x8", 8)], onchange=set_board_size)
    menu.add.selector(
        "Playing mode: ",
        [("Human vs Human", False), ("Human vs AI", True)],
        onchange=set_playing_mode,
    )
    menu.add.button("Play", start_the_game)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(win)


if __name__ == "__main__":
    main()
