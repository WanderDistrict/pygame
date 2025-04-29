import pygame as pg
import random

from board import Board


class Game(Board):
    def __init__(self, width: int, height: int, left: int = 10, top: int = 10, cell_size: int = 40):
        super().__init__(width, height, left, top, cell_size, initial_value=0)
        for row in range(height):
            for col in range(width):
                self._board[row][col] = random.randint(0, 1)
        self.current_player = 0

    def draw_cell(self, screen: pg.Surface, row: int, col: int, rect: pg.Rect) -> None:
        if self._board[row][col] == 0:
            color = pg.Color('white')
        else:
            color = pg.Color('black')
        pg.draw.circle(screen, color, rect.center, rect.w * 0.4)

    def on_click(self, row: int, col: int) -> None:
        if self._board[row][col] == self.current_player:
            return

        for i in range(self._width):
            self._board[row][i] = self.current_player
        for i in range(self._height):
            self._board[i][col] = self.current_player

        self.current_player = 1 - self.current_player
