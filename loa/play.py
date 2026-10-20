import pygame

from .constants import WIDTH, HEIGHT, BLACK, GREEN
from .game import Game


class Play:
    FPS = 60

    def __init__(self, win, rows, cols, square_size, with_ai):
        self.win = win
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.with_ai = with_ai
        self.font = pygame.font.Font(pygame.font.get_default_font(), 32)
        self.small_font = pygame.font.Font(pygame.font.get_default_font(), 20)

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        return y // self.square_size, x // self.square_size

    def _show_result(self, result):
        label = "BLACK WINS!" if result == BLACK else "WHITE WINS!"
        text = self.font.render(label, True, GREEN)
        hint = self.small_font.render("Press ESC or close the window to return to the menu", True, GREEN)
        self.win.fill(BLACK)
        self.win.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        self.win.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
        pygame.display.update()

    def start_playing(self):
        """Run one game. Returns to the caller (menu) when the window is closed or ESC is pressed."""
        clock = pygame.time.Clock()
        game = Game(self.win, self.rows, self.cols, self.square_size, self.with_ai)
        run = True
        finished = False

        try:
            while run:
                clock.tick(self.FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        run = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and not finished:
                        row, col = self.get_row_col_from_mouse(event.pos)
                        if 0 <= row < self.rows and 0 <= col < self.cols:
                            game.select(row, col)

                if finished:
                    continue

                game.update()
                result = game.winner()
                if result is not None:
                    self._show_result(result)
                    finished = True
        finally:
            game.close()
