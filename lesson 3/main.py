import random
import time

import pygame as pg

pg.init()
SIZE = WIDTH, HEIGHT = 800, 800
screen = pg.display.set_mode(SIZE)

from my_sprite import MySprite
from my_sprite import Python
from utils import load_img

FPS = 60
BG_COLOR = pg.Color('black')
PHON = pg.transform.smoothscale(load_img('war.jpg'), SIZE)


def game():
    all_sprites = pg.sprite.Group()
    player = MySprite(all_sprites)
    player.rect.bottom = HEIGHT
    player.rect.centerx = WIDTH / 2
    python = Python(all_sprites)
    python_group = pg.sprite.Group()
    clock = pg.time.Clock()
    running = True
    start = time.time()
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
        screen.blit(PHON, (0, 0))

        all_sprites.draw(screen)
        all_sprites.update(events)
        collide = pg.sprite.spritecollideany(player, python_group, None)
        if collide != None:
            print(time.time() - start)
            break
        if random.random() < 0.07:
            Python(all_sprites, python_group)

        pg.display.flip()
        clock.tick(FPS)


while True:
    game()
pg.quit()
