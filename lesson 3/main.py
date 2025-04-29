import pygame as pg
pg.init()
SIZE = WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode(SIZE)
from my_sprite import MySprite

FPS = 60
BG_COLOR = pg.Color('black')
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
player = MySprite(all_sprites)
player.rect.bottom = HEIGHT

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill(BG_COLOR)

    all_sprites.draw(screen)
    all_sprites.update()

    pg.display.flip()
    clock.tick(FPS)
pg.quit()
