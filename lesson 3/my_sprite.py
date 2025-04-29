import random

import pygame as pg

from utils import load_img

class MySprite(pg.sprite.Sprite):
    IMG = load_img('ivanovfil.jpg')
    IMG = pg.transform.smoothscale(IMG, (40, 40))
    STEP = 15
    IMG_FLIP = pg.transform.flip(IMG, True, False)

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.IMG
        self.rect = self.IMG.get_rect()

    def update(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                pass

        keyboard = pg.key.get_pressed()
        if (keyboard[pg.K_a] or keyboard[pg.K_LEFT]) and self.rect.left > 0:
            self.image = self.IMG
            self.rect.move_ip(-self.STEP, 0)
        if (keyboard[pg.K_d] or keyboard[pg.K_RIGHT]) and self.rect.right < 800:
            self.image = self.IMG_FLIP
            self.rect.move_ip(self.STEP, 0)
        if (keyboard[pg.K_w] or keyboard[pg.K_UP]) and self.rect.top > 0:
            self.image = self.IMG
            self.rect.move_ip(0, -self.STEP)
        if (keyboard[pg.K_s] or keyboard[pg.K_DOWN]) and self.rect.bottom < 800:
            self.image = self.IMG_FLIP
            self.rect.move_ip(0, self.STEP)

class Python(pg.sprite.Sprite):
    IMG = pg.transform.smoothscale(
        load_img('logo.png'),
        (10, 1000))
    MASK = pg.mask.from_surface(IMG)
    SPEED = 50

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.IMG
        self.rect = self.IMG.get_rect()
        self.rect.bottom = 0
        self.rect.left = random.randrange(0, 800 - self.rect.width)
        self.mask = self.MASK

    def update(self, events):
        self.rect.y += self.SPEED
        if self.rect.top > 810:
            self.kill()
