import pygame as pg

from config import Settings
from my_board import Minesweeper

pg.init()

screen = pg.display.set_mode(Settings.SIZE)
pg.display.set_caption(Settings.TITLE)
clock = pg.time.Clock()
game = Minesweeper(20, 20, 50)
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        game.handle_event(event)
    screen.fill(Settings.BACKGROUND)
    game.draw(screen)
    pg.display.flip()
    clock.tick(Settings.FPS)
pg.quit()
