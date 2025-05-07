"""
Этот модуль содержит классы для создания спрайтов в Pygame,
включая игрового персонажа (MySprite), платформы (Platform) и лестницы (Ladder).
"""
import random

import pygame as pg

from utils import load_img


class MySprite(pg.sprite.Sprite):
    """
    Класс, представляющий игрового персонажа.

    Атрибуты:
        IMG (pg.Surface): Поверхность, используемая для отображения спрайта. Залита лаймовым цветом.
        STEP (int): Количество пикселей, на которое спрайт перемещается за один кадр при движении по горизонтали.
        FALL_SPEED (int): Скорость падения спрайта под действием гравитации.
        JUMP_SPEED (int): Начальная скорость прыжка спрайта.

    Методы:
        __init__(*groups): Инициализирует спрайт, устанавливает изображение, прямоугольник и начальные значения.
        update(events, platforms, ladders): Обновляет состояние спрайта в каждом кадре.
        handle_input(ladders): Обрабатывает ввод пользователя для перемещения и прыжков.
        jump(): Заставляет спрайт прыгнуть.
        apply_gravity(platforms): Применяет гравитацию к спрайту.
        move_x(): Перемещает спрайт по горизонтали.
        move_y(platforms, ladders): Перемещает спрайт по вертикали и обрабатывает столкновения с платформами и лестницами.
        check_ladder_collision(ladders): Проверяет, находится ли спрайт на лестнице.
    """
    IMG = pg.Surface([20, 20])
    IMG.fill('lime')
    STEP = 10
    FALL_SPEED = 1
    JUMP_SPEED = -15

    def __init__(self, *groups):
        """
        Инициализирует спрайт игрока.

        Аргументы:
            *groups: Группы спрайтов, в которые добавляется спрайт игрока.
        """
        super().__init__(*groups)
        self.image = self.IMG
        self.rect = self.image.get_rect()
        self.y_velocity = 0
        self.falling = True
        self.on_ground = False
        self.on_ladder = False
        self.jump_count = 0

    def update(self, events, platforms, ladders):
        """
        Обновляет состояние спрайта в каждом кадре.

        Аргументы:
            events: Список событий Pygame.
            platforms: Группа спрайтов платформ.
            ladders: Группа спрайтов лестниц.
        """
        self.handle_input(ladders)
        if not self.on_ladder:
            self.apply_gravity(platforms)
        self.move_x()
        self.move_y(platforms, ladders)

    def handle_input(self, ladders):
        """
        Обрабатывает ввод пользователя для перемещения и прыжков.

        Аргументы:
            ladders: Группа спрайтов лестниц.
        """
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
        """
        Заставляет спрайт прыгнуть.
        """
        self.y_velocity = self.JUMP_SPEED
        self.falling = True
        self.on_ground = False
        self.on_ladder = False
        self.jump_count += 1
        print(self.jump_count)

    def apply_gravity(self, platforms):
        """
        Применяет гравитацию к спрайту.

        Аргументы:
            platforms: Группа спрайтов платформ.
        """
        if self.falling and not self.on_ladder:
            self.y_velocity += self.FALL_SPEED

            if self.y_velocity > 15:
                self.y_velocity = 15

    def move_x(self):
        """
        Перемещает спрайт по горизонтали.
        """
        if not self.on_ladder:
            self.rect.x += self.x_direction * self.STEP

    def move_y(self, platforms, ladders):
        """
        Перемещает спрайт по вертикали и обрабатывает столкновения с платформами и лестницами.

        Аргументы:
            platforms: Группа спрайтов платформ.
            ladders: Группа спрайтов лестниц.
        """
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
        """
        Проверяет, находится ли спрайт на лестнице.

        Аргументы:
            ladders: Группа спрайтов лестниц.
        """
        self.on_ladder = False
        for ladder in ladders:
            if self.rect.colliderect(ladder.rect):
                self.on_ladder = True
                break


class Platform(pg.sprite.Sprite):
    """
    Класс, представляющий платформу.

    Атрибуты:
        image (pg.Surface): Изображение платформы (белый прямоугольник).
        rect (pg.Rect): Прямоугольник, определяющий положение и размер платформы.

    Методы:
        __init__(x, y, *groups): Инициализирует платформу, устанавливает положение и добавляет в группы спрайтов.
    """

    def __init__(self, x, y, *groups):
        """
        Инициализирует платформу.

        Аргументы:
            x (int): X-координата верхнего левого угла платформы.
            y (int): Y-координата верхнего левого угла платформы.
            *groups: Группы спрайтов, в которые добавляется платформа.
        """
        super().__init__(*groups)
        self.image = pg.Surface([100, 10])
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ladder(pg.sprite.Sprite):
    """
    Класс, представляющий лестницу.

    Атрибуты:
        image (pg.Surface): Изображение лестницы (красный прямоугольник).
        rect (pg.Rect): Прямоугольник, определяющий положение и размер лестницы.

    Методы:
        __init__(x, y, *groups): Инициализирует лестницу, устанавливает положение и добавляет в группы спрайтов.
    """

    def __init__(self, x, y, *groups):
        """
        Инициализирует лестницу.

        Аргументы:
            x (int): X-координата верхнего левого угла лестницы.
            y (int): Y-координата верхнего левого угла лестницы.
            *groups: Группы спрайтов, в которые добавляется лестница.
        """
        super().__init__(*groups)
        self.image = pg.Surface([10, 50])
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
