import enum
from typing import override

import pygame as pg

from board import Board


class Cell(enum.Enum):
    EMPTY = 0
    CROSS = 1
    CIRCLE = 2


class TickTackToe(Board):
    COLOR_CROSS = '#FF0000'
    COLOR_CIRCLE = '#00FF00'
    FIGURE_WIDTH = 5

    def __init__(self, width: int, height: int):
        super().__init__(width, height, initial_value=Cell.EMPTY)
        self._current_user = Cell.CROSS
        self._is_finished = False

    def next_player(self):
        if self._current_user == Cell.CROSS:
            self._current_user = Cell.CIRCLE
        else:
            self._current_user = Cell.CROSS

    @override
    def on_click(self, row: int, col: int) -> None:
        if self._is_finished:
            return
        if self.get_cell(row, col) != Cell.EMPTY:
            return
        self._board[row][col] = self._current_user
        self.check_win()
        self.next_player()

    def check_win(self) -> None:
        # TODO: Есть ли выигрыш
        ...

    @override
    def draw_cell(self, screen: pg.Surface, row: int, col: int, rect: pg.Rect) -> None:
        cell = self.get_cell(row, col)
        rect2 = rect.copy()
        rect2.w -= 8
        rect2.h -= 8
        rect2.center = rect.center
        if cell == Cell.CROSS:
            pg.draw.line(screen, self.COLOR_CROSS, rect2.topleft, rect2.bottomright, self.FIGURE_WIDTH)
            pg.draw.line(screen, self.COLOR_CROSS, rect2.topright, rect2.bottomleft, self.FIGURE_WIDTH)
        elif cell == Cell.CIRCLE:
            pg.draw.circle(screen, self.COLOR_CIRCLE, rect2.center, rect2.w // 2, self.FIGURE_WIDTH)
