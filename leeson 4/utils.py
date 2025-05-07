# utils.py
import os
import sys

import pygame as pg


def load_img(image_path: str, colorkey=None) -> pg.Surface:
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
