import pygame as pg
from utils import load_img


class Suharik(pg.sprite.Sprite):
    IMG = load_img("suharik.png", (60, 90, 90))

    def __init__(self, *args, size: tuple[int, int] | None = None):
        super().__init__(*args)
        self.image = self.IMG
        if size:
            self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
