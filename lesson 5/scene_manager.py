import time
import types
from typing import Callable

type Coords = tuple[int, int]

from config import Config

import pygame as pg


class SkipException(Exception):
    pass


class SceneManager:
    def __init__(self, screen: pg.Surface, duration: float, background: pg.Color):
        self.screen = screen
        self.duration = duration
        self.background = background
        self.clock = pg.time.Clock()
        self.group = pg.sprite.Group()

    def add(self, sprite: pg.sprite.Sprite, position: Coords = (0, 0)) -> None:
        self.group.add(sprite)
        sprite.rect.move_ip(position)

    def __enter__(self):
        self.time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        t = time.time() - self.time
        while t < self.duration:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    raise SkipException()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        raise SkipException()
                    elif event.key == pg.K_SPACE:
                        return
            self.screen.fill(self.background)
            self.group.update(time=t)
            self.group.draw(self.screen)
            pg.display.flip()
            self.clock.tick(Config.FPS)
            t = time.time() - self.time

    @staticmethod
    def set_update(sprite: pg.sprite.Sprite, callback: Callable) -> None:
        sprite.update = types.MethodType(callback, sprite)

    @staticmethod
    def set_animation(sprite: pg.sprite.Sprite,
                      spos: Coords,
                      epos: Coords,
                      stime: float | int,
                      etime: float | int
                      ) -> None:
        def _update(self: pg.sprite.Sprite, time: float | int) -> None:
            if stime <= time <= etime:
                x1, y1 = spos
                x2, y2 = epos
                x = x1 + (time - stime) * (x2 - x1) / (etime - stime)
                y = y1 + (time - stime) * (y2 - y1) / (etime - stime)
                self.rect.x = x
                self.rect.y = y

        SceneManager.set_update(sprite, _update)
