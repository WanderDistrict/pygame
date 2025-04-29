import enum

from board import Board
import random
import pygame as pg

from utils import load_img


CLOSED = -1
MINE = 10
FLAG = 110
QUESTION = 220


class Status(enum.Enum):
    NOT_INITIALIZED = 0
    PLAYING = 1
    WINNING = 2
    LOSING = 3


class Minesweeper(Board):
    """
    0       - 0 mines around (open cell)
    1...8   - 1-8 mines around (open cell)
    -1      - closed cell (not mine)
    10      - mine
    +100    - flag
    +200    - question
    """
    CELL_COLOR = pg.Color('black')
    DOUBLE_CLICK_DELAY = 500

    def __init__(self, width: int, height: int, count_mines: int):
        super().__init__(width, height, initial_value=CLOSED)
        self._count_mines = count_mines
        self._status = Status.NOT_INITIALIZED
        self._show_mines = False  # TODO return to False
        self._no_mines = self._width * self._height - count_mines
        font = pg.font.Font(None, round(self._cell_size * 1.25))
        self._digit = [
            font.render(str(i), True, color)
            for i, color in enumerate([
                'black', 'blue', 'green', 'red', 'darkviolet', 'steelblue', 'khaki3', 'olivedrab4', 'lightsalmon'
            ])
        ]
        self._image_question = font.render('?', True, 'yellow')
        self._image_bomb = pg.transform.smoothscale(
            load_img('tnt.jpg'),
            (self._cell_size, self._cell_size)
        )
        self._image_flag = pg.transform.smoothscale(
            load_img('flag.png', -1),
            (self._cell_size, self._cell_size)
        )
        self._double_click_clock = pg.time.Clock()
        self._last_coord = None

    def draw_cell(self, screen: pg.Surface, row: int, col: int, rect: pg.Rect) -> None:
        cell = self._board[row][col]
        if cell == MINE and self._show_mines:
            screen.blit(self._image_bomb, rect.topleft)
        elif cell == CLOSED or cell % 100 == MINE and not self._show_mines or cell >= 100:
            pg.draw.rect(screen, '#505050', rect)
            if cell // 100 == 1:
                screen.blit(self._image_flag, rect.topleft)
            elif cell // 100 == 2:
                screen.blit(self._image_question, (
                    rect.centerx - self._image_question.get_width() // 2,
                    rect.centery - self._image_question.get_height() // 2,
                ))
        elif 0 < cell <= 8:
            digit = self._digit[cell]
            screen.blit(self._digit[cell],
                        (rect.centerx - digit.get_width() // 2,
                         rect.centery - digit.get_height() // 2))

    def on_click(self, row: int, col: int) -> None:
        if row < 0 or col < 0 or row >= self._height or col >= self._width:
            return
        if self._status == Status.WINNING or self._status == Status.LOSING:
            return
        if self._status == Status.NOT_INITIALIZED:
            self._initial(row, col)
        cell = self._board[row][col]
        if 0 <= cell <= 8:
            return
        if cell == MINE:
            self._lose()
        if cell == CLOSED:
            self._no_mines -= 1
            self._board[row][col] = self._get_neighbours(row, col)
            if self._board[row][col] == 0:
                self._open_neighbours(row, col)
            if self._no_mines == 0:
                self._win()

    def _open_neighbours(self, row: int, col: int) -> None:
        for x in range(col - 1, col + 2):
            for y in range(row - 1, row + 2):
                if x != col or y != row:
                    self.on_click(y, x)

    def _get_neighbours(self, row: int, col: int) -> int:
        result = 0
        for x in range(col - 1, col + 2):
            for y in range(row - 1, row + 2):
                if self.get_cell(y, x) == MINE:
                    result += 1
        return result

    def _win(self) -> None:
        self._status = Status.WINNING
        print('WIN')

    def _lose(self) -> None:
        self._status = Status.LOSING
        self._show_mines = True
        print('LOSE')

    def _initial(self, row: int, col: int) -> None:
        self._status = Status.PLAYING
        n = 0
        assert self._count_mines < self._width * self._height
        while n < self._count_mines:
            x = random.randrange(self._width)
            y = random.randrange(self._height)
            if (y, x) != (row, col) and self._board[y][x] == CLOSED:
                self._board[y][x] = MINE
                n += 1

    def on_double_click(self, row: int, col: int) -> None:
        if self._status == Status.WINNING or self._status == Status.LOSING:
            return
        if 1 <= self._board[row][col] <= 8:
            count_flags = 0
            for x in range(col - 1, col + 2):
                for y in range(row - 1, row + 2):
                    if self.get_cell(y, x) == MINE:
                        count_flags += 1
            if count_flags == self._board[row][col]:
                for x in range(col - 1, col + 2):
                    for y in range(row - 1, row + 2):
                        self.on_click(y, x)


    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            coord = self.get_at(*event.pos)
            if coord:
                if event.button == 1:
                    if coord == self._last_coord and self._double_click_clock.tick() < self.DOUBLE_CLICK_DELAY:
                        self.on_double_click(*coord)
                    else:
                        self.on_click(*coord)
                    self._last_coord = coord
                elif event.button == 3:
                    self.right_click(*coord)


    def right_click(self, row: int, col: int) -> None:
        if row < 0 or col < 0 or row >= self._height or col >= self._width:
            return
        if self._status == Status.WINNING or self._status == Status.LOSING:
            return
        if self._status == Status.NOT_INITIALIZED:
            return
        if self._board[row][col] in (CLOSED, MINE):
            self._board[row][col] += 110
        elif self._board[row][col] // FLAG == 1:
            self._board[row][col] += 110
        elif self._board[row][col] // 100 == 2:
            self._board[row][col] -= 220

