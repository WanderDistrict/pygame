import pygame as pg


class Tile(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, x: int, y: int):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
