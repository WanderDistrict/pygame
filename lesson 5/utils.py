import dataclasses
import os
import sys

import pygame as pg

from config import Config


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


def load_many_imgs(image_path: str, colorkey=None, row_count: int = 1, col_count: int = 1,
                   size: tuple[int, int] | None = None) -> list[pg.Surface]:
    result = []
    og_img = load_img(image_path, colorkey)
    if size:
        w = og_img.get_width() // col_count
        h = og_img.get_height() // row_count

    rect = pg.Rect(0, 0, w, h)

    for row in range(row_count):
        for col in range(col_count):
            sub_img = og_img.subsurface(rect.move((col * w, row * h)))
            sub_img = pg.transform.scale(sub_img, size)
            #########
            # sub_img_bytes = pg.image.tobytes(sub_img, 'RGB')
            # img = Image.frombytes('RGB', sub_img.get_size(), sub_img_bytes)
            # img = img.quantize(5).convert('RGB')
            # sub_img = pg.image.frombytes(img.tobytes(), sub_img.get_size(), 'RGB')

            #########
            result.append(sub_img)

    result.append(og_img)
    return result


def load_map(filename: str) -> list[str]:
    path = os.path.join('data', 'maps', filename)
    with open(path, encoding='utf-8') as f:
        my_map = list(map(str.rstrip, f.readlines()))
    width = max(len(s) for s in my_map)
    return [s.ljust(width, '.') for s in my_map]


@dataclasses.dataclass
class TileGroup:
    all_tile: pg.sprite.Group = pg.sprite.Group()
    obstacle: pg.sprite.Group = pg.sprite.Group()


tile_imgs = {
    ' ': load_img('wood.png'),
    '#': load_img('cobblestone.jpg'),
    '%': load_img('dark.jpg')
}
tile_imgs = {
    c: pg.transform.scale(img, (Config.TILE, Config.TILE))
    for c, img in tile_imgs.items()
}


def read_map(my_map: list[str]) -> TileGroup:

    from tile import Tile
    result = TileGroup()
    for row, s in enumerate(my_map):
        for col, cell in enumerate(s):
            if cell == '.':
                continue
            img = tile_imgs[cell]
            tile = Tile(img, row * Config.TILE, col * Config.TILE)
            result.all_tile.add(tile)
            if cell in '#' or cell in '%':
                result.obstacle.add(tile)

    return result
