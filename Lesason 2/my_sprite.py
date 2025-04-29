import random

import pygame as pg

from utils import load_img


class MySprite(pg.sprite.Sprite):
    IMG = load_img('ivanovfil.jpg')
    IMG = pg.transform.smoothscale(IMG, (200, 160))

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.IMG
        self.rect = self.IMG.get_rect()
        self.rect.move_ip(random.randrange(600), random.randrange(500))
        self.rotate = None

    def update(self):
        self.rect.move_ip(random.randint(-3, 3), random.randint(-3, 3))
        if self.rotate is not None:
            self.rotate += 6
            self.image = pg.transform.rotate(self.IMG, self.rotate)
            if self.rotate == 360:
                self.rotate = None
        elif random.random() < 0.01:
            self.rotate = 0