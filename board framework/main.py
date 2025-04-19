import pygame as pg

from config import Settings

pg.init()

screen = pg.display.set_mode(Settings.SIZE)
pg.display.set_caption(Settings.TITLE)
clock = pg.time.Clock()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill(Settings.BACKGROUND)

    pg.display.flip()
    clock.tick(Settings.FPS)
pg.quit()
