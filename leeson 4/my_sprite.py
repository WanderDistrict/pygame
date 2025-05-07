import random

import pygame as pg

from utils import load_img


class MySprite(pg.sprite.Sprite):
    IMG = pg.Surface([20, 20])
    IMG.fill('lime')
    STEP = 10
    FALL_SPEED = 1
    JUMP_SPEED = -15

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.IMG
        self.rect = self.image.get_rect()
        self.y_velocity = 0
        self.falling = True
        self.on_ground = False
        self.on_ladder = False
        self.jump_count = 0

    def update(self, events, platforms, ladders):
        self.handle_input(ladders)
        if not self.on_ladder:
            self.apply_gravity(platforms)
        self.move_x()
        self.move_y(platforms, ladders)

    def handle_input(self, ladders):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.x_direction = -1
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.x_direction = 1
        else:
            self.x_direction = 0

        if (keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]) and self.on_ground and self.jump_count < 1:
            self.jump()

        if self.on_ladder:
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.y_direction = -1
            elif keys[pg.K_DOWN] or keys[pg.K_s]:
                self.y_direction = 1
            else:
                self.y_direction = 0

    def jump(self):
        self.y_velocity = self.JUMP_SPEED
        self.falling = True
        self.on_ground = False
        self.on_ladder = False
        self.jump_count += 1
        print(self.jump_count)

    def apply_gravity(self, platforms):
        if self.falling and not self.on_ladder:
            self.y_velocity += self.FALL_SPEED

            if self.y_velocity > 15:
                self.y_velocity = 15

    def move_x(self):
        if not self.on_ladder:
            self.rect.x += self.x_direction * self.STEP

    def move_y(self, platforms, ladders):
        if self.on_ladder:
            self.rect.y += self.y_direction * self.STEP
            self.falling = True
            self.y_velocity = 0
            self.on_ground = False
        else:
            self.rect.y += self.y_velocity
            self.falling = True
            if self.y_velocity > 0:
                for platform in platforms:
                    if self.rect.colliderect(platform.rect):
                        self.rect.bottom = platform.rect.top
                        self.y_velocity = 0
                        self.falling = False
                        self.on_ground = True
                        self.on_ladder = False
                        self.jump_count = 0
                        break
                    else:
                        self.on_ground = False
            if self.rect.bottom >= 500:
                self.rect.bottom = 500
                self.y_velocity = 0
                self.falling = False
                self.on_ground = True
                self.on_ladder = False
                self.jump_count = 0

        self.check_ladder_collision(ladders)

    def check_ladder_collision(self, ladders):
        self.on_ladder = False
        for ladder in ladders:
            if self.rect.colliderect(ladder.rect):
                self.on_ladder = True
                break


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pg.Surface([100, 10])
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ladder(pg.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pg.Surface([10, 50])
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
