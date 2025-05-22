import pygame as pg


class Camera:
    def __init__(self):
        self._group = pg.sprite.Group()
        self._target: pg.sprite.Sprite | None = None
        self._pos = 0, 0
        self._spring: float = 0.05

    def update(self) -> None:
        if self._target is not None:
            dx = self._target.rect.centerx - self._pos[0]
            dy = self._target.rect.centery - self._pos[1]
            dx *= self._spring
            dy *= self._spring
            for sprite in self._group:
                sprite.rect.move_ip(-dx, -dy)

    def set_pos(self, x: int, y: int) -> 'Camera':
        self._pos = x, y
        return self

    def set_target(self, target: pg.sprite.Sprite | None) -> 'Camera':
        self._target = target
        return self

    @property
    def group(self) -> pg.sprite.Group:
        return self._group

    def add(self, object: pg.sprite.Sprite | pg.sprite.Group) -> 'Camera':
        if isinstance(object, pg.sprite.Sprite):
            self._group.add(object)
        elif isinstance(object, pg.sprite.Group):
            for sprite in object:
                self._group.add(sprite)
        return self
