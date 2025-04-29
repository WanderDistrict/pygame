import random

import pygame as pg

from utils import load_img


class MySprite(pg.sprite.Sprite):
    IMG = load_img('ivanovfil.jpg')
    IMG = pg.transform.smoothscale(IMG, (100, 100))

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.IMG
        self.rect = self.IMG.get_rect()

    def update(self):
        pass