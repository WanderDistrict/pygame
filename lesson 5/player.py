from character import Character
import pygame as pg
from utils import TileGroup


class Player(Character):
    IMG_PATH = 'collage.png'


class Boss(Character):
    pass


class BossChina(Boss):
    IMG_PATH = 'kitai.png'
    ROWS = 1
    COLS = 1
    SPEED = 4

    def update(self, *args, groups: TileGroup | None = None, **kwargs):
        dx = dy = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            dx -= self.SPEED
        if keys[pg.K_d]:
            dx += self.SPEED
        if keys[pg.K_w]:
            dy -= self.SPEED
        if keys[pg.K_s]:
            dy += self.SPEED
        self.rect.move_ip(dx, dy)
        if groups and pg.sprite.spritecollideany(self, groups.obstacle):
            self.rect.move_ip(-dx, -dy)
