"""
Этот модуль содержит вспомогательные функции, такие как загрузка изображений.
"""
import os
import sys

import pygame as pg


def load_img(image_path: str, colorkey=None) -> pg.Surface:
    """
    Загружает изображение из файла.

    Аргументы:
        image_path (str): Путь к файлу изображения относительно папки 'data/img'.
        colorkey (optional): Цвет, который будет считаться прозрачным.  Если None, прозрачность не применяется.
                           Если -1, цвет верхнего левого пикселя будет использован как colorkey.

    Возвращает:
        pg.Surface: Загруженное изображение в виде поверхности Pygame.

    Вызывает:
        SystemExit: Если файл изображения не найден.
    """
    fullname = os.path.join('data', 'img', image_path)
    if not os.path.isfile(fullname):
        print(f'"{fullname}" not found!', file=sys.stderr)
        sys.exit(50541)
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
