"""
Этот модуль содержит основную логику игры, включая инициализацию Pygame,
создание окна, обработку событий и отрисовку игровых объектов.
"""
import pygame as pg

pg.init()
SIZE = WIDTH, HEIGHT = 500, 500
screen = pg.display.set_mode(SIZE)

from my_sprite import MySprite, Platform, Ladder

FPS = 60
BG_COLOR = pg.Color('black')


def game():
    """
    Основная функция игры, которая инициализирует и запускает игровой цикл.
    """
    all_sprites = pg.sprite.Group()
    platform_group = pg.sprite.Group()
    ladder_group = pg.sprite.Group()
    player = MySprite(all_sprites)
    player.rect.bottom = HEIGHT / 2
    player.rect.centerx = WIDTH / 2

    clock = pg.time.Clock()
    running = True
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Platform(event.pos[0], event.pos[1], all_sprites, platform_group)
                elif event.button == 3:
                    Ladder(event.pos[0], event.pos[1], all_sprites, ladder_group)
                    player.falling = True

        screen.fill(BG_COLOR)

        f1 = pg.font.Font(None, 36)
        text1 = f1.render('Лестница = ПКМ', 1, (100, 100, 100))

        screen.blit(text1, (10, 10))

        all_sprites.draw(screen)
        all_sprites.update(events, platform_group, ladder_group)

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()


game()
