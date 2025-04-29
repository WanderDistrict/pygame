import pygame as pg

from board import Board


class Game(Board):
    def draw_cell(self, screen: pg.Surface, row: int, col: int, rect: pg.Rect) -> None:
        if self._board[row][col] == 0:
            color = pg.Color('white')
        else:
            color = pg.Color('black')
        pg.draw.circle(screen, color, rect.center, rect.w * 0.4)

    def on_click(self, row: int, col: int) -> None:\
        # TODO: turn check
        # it's an example. Code should be different
        self._board[row][col] = 1 - self._board[row][col]