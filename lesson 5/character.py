from enum import IntEnum
from utils import load_many_imgs
import pygame as pg


class Emotion(IntEnum):
    NORMAL = 0
    SMILEY = 1
    ANGER = 2
    OGO = 3


class Character(pg.sprite.Sprite):
    IMG_PATH: str | None = None
    IMG_LIST: list[pg.Surface] = []
    ROWS = 2
    COLS = 2

    def __init__(self, *args, size: tuple[int, int] | None = None):
        super().__init__(*args)
        self.class_init()
        self.emotion = Emotion.NORMAL
        self.images = self.IMG_LIST.copy()
        if size:
            self.images = [
                pg.transform.scale(image, size).convert_alpha() for image in self.images
            ]
        self.image: pg.Surface = self.images[self.emotion]
        self.rect = self.image.get_rect()

    def emote(self, emotion: Emotion) -> None:
        self.emotion = emotion
        self.image = self.images[self.emotion]

    @classmethod
    def class_init(cls):
        if not cls.IMG_LIST:
            cls.IMG_LIST = load_many_imgs(cls.IMG_PATH, "white", cls.ROWS, cls.COLS, (200, 200))
