import enum
from typing import override

import pygame as pg

from board import Board
from config import Settings


class Cell(enum.Enum):
    EMPTY = 0
    CROSS = 1
    CIRCLE = 2


class TickTackToe(Board):
    COLOR_CROSS = '#FF0000'
    COLOR_CIRCLE = '#00FF00'
    COLOR_TEXT = '#FFFFFF'
    FIGURE_WIDTH = 5

    def __init__(self, width: int, height: int):
        super().__init__(width, height, initial_value=Cell.EMPTY)
        self._current_user = Cell.CROSS
        self._is_finished = False
        self._font = pg.font.SysFont('Comic Sans MS', 26)

    def next_player(self):
        if self._is_finished:
            return
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
        #  Проверяем строки
        for row in range(self._height):
            n = 0
            for col in range(self._width):
                cell = self.get_cell(row, col)
                if cell == Cell.EMPTY or cell is None:
                    continue
                if cell == self.get_cell(row, col - 1):
                    n += 1
                    if n == 5:
                        self._is_finished = True
                        return
                else:
                    n = 1
        # Проверяем столбцы
        for col in range(self._width):
            n = 0
            for row in range(self._height):
                cell = self.get_cell(row, col)
                if cell == Cell.EMPTY or cell is None:
                    continue
                if cell == self.get_cell(row - 1, col):
                    n += 1
                    if n == 5:
                        self._is_finished = True
                        return
                else:
                    n = 1
        # Проверяем главные диагонали
        for row in range(-self._height, self._height):
            n = 0
            for col in range(self._width):
                cell = self.get_cell(row + col, col)
                if cell == Cell.EMPTY or cell is None:
                    continue
                if cell == self.get_cell(row + col - 1, col - 1):
                    n += 1
                    if n == 5:
                        self._is_finished = True
                        return
                else:
                    n = 1
        # Проверяем побочные диагонали
        for row in range(-self._height, self._height):
            n = 0
            for col in range(self._width):
                cell = self.get_cell(row + col, self._width - col - 1)
                if cell == Cell.EMPTY or cell is None:
                    continue
                if cell == self.get_cell(row + col - 1, self._width - col):
                    n += 1
                    if n == 5:
                        self._is_finished = True
                        return
                else:
                    n = 1

    @override
    def draw(self, screen: pg.Surface) -> None:
        super().draw(screen)
        text = ''
        if self._is_finished:
            text += 'Выиграли: '
        else:
            text += 'Текущий ход: '
        if self._current_user == Cell.CIRCLE:
            text += 'НОЛИКИ'
        else:
            text += 'КРЕСТИКИ'
        text_img = self._font.render(text, True, self.COLOR_TEXT)
        screen.blit(text_img, ((Settings.WIDTH - text_img.get_width()) // 2, 0))


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
