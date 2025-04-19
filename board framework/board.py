import pygame as pg


class Board:
    CELL_COLOR = pg.Color('white')
    BORDER_WIDTH = 1

    def __init__(self,
                 width: int,
                 height: int,
                 left: int = 10,
                 top: int = 10,
                 cell_size: int = 40,
                 initial_value: int = 0,
                 ):
        self._width = width
        self._height = height
        self._left = left
        self._top = top
        self._cell_size = cell_size
        self._board: list[list[int]] = [
            [initial_value] * width
            for _ in range(height)
        ]

    def set_view(self,
                 left: int,
                 top: int,
                 cell_size: int
                 ) -> None:
        self._left = left
        self._top = top
        self._cell_size = cell_size

    def draw(self, screen: pg.Surface) -> None:
        for row in range(self._height):
            for col in range(self._width):
                rect = pg.Rect(
                    self._left + col * self._cell_size,
                    self._top + row * self._cell_size,
                    self._cell_size,
                    self._cell_size
                )
                pg.draw.rect(screen, self.CELL_COLOR, rect, self.BORDER_WIDTH)
