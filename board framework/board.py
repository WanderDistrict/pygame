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
                self.draw_cell(screen, row, col, rect)

    def draw_cell(self, screen: pg.Surface, row: int, col: int, rect: pg.Rect) -> None:
        ...

    def get_at(self, x: int, y: int) -> tuple[int, int] | None:
        col = (x - self._left) // self._cell_size
        row = (y - self._top) // self._cell_size
        if col < 0 or col >= self._width or row < 0 or row >= self._height:
            return None
        return row, col

    def on_click(self, row: int, col: int) -> None:
        ...

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            coord = self.get_at(*event.pos)
            if coord:
                self.on_click(*coord)

    def get_cell(self, row: int, col: int) -> int | None:
        if row < 0 or row >= self._height or col < 0 or col >= self._width:
            return None
        return self._board[row][col]
