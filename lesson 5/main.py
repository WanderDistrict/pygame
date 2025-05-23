import pygame as pg
from config import Config



pg.init()
from camera import Camera
screen = pg.display.set_mode(Config.SIZE)
import utils
from player import *
from cutscene import start_scene


def main(screen):
    clock = pg.time.Clock()
    camera = Camera()
    background = 'white'

    level = utils.load_map('map1.txt')
    groups = utils.read_map(level)
    peoples = pg.sprite.Group()
    player = BossChina(size=(Config.TILE * 1.5, Config.TILE * 1.5))
    player.rect.move_ip(Config.TILE * 2, Config.TILE * 2)
    peoples.add(player)

    (camera.add(peoples)
        .add(groups.all_tile)
        .add(player)
        .set_pos(Config.WIDTH // 2, Config.HEIGHT // 2)
        .set_target(player))

    running = True
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
        screen.fill(background)
        groups.all_tile.draw(screen)
        peoples.update(events=events, groups=groups)
        camera.update()
        peoples.draw(screen)


        pg.display.flip()
        clock.tick(Config.FPS)

if __name__ == '__main__':
    # start_scene(screen)
    main(screen)
    pg.quit()
