import pygame as pg
from scene_manager import SceneManager, SkipException
from character import Emotion

from player import *
from susarik import Suharik

def start_scene(screen: pg.Surface):
    def move(self, *args, **kwargs):
        self.i += 1
        if self.i % 10 == 0:
            self.rect.move_ip(0, 20)
        elif self.i % 10 == 5:
            self.rect.move_ip(0, -20)

    background = 'white'
    try:
        # for x in (0, 200, 400):
        #     with SceneManager(screen, 2, background) as scene:
        #         scene.add(Player(size=(400 + 2 * x, 400 + 2 * x)), (200 - x, 200 - x))
        #     with SceneManager(screen, 2, background) as scene:
        #         scene.add(Suharik(size=(400 + 2 * x, 400 + 2 * x)), (200 - x, 200 - x))
        with SceneManager(screen, 10, background) as scene:
            hero = (Player(size=(500, 500)))
            hero.emote(Emotion.SMILEY)
            scene.add(hero, (100, 0))
            SUHARIK = Suharik(size=(200, 200))
            SUHARIK.i = 0
            scene.add(SUHARIK, (250, 250))
            scene.set_update(SUHARIK, move)


            kitai = BossChina(size=(200, 200))
            scene.add(kitai, (1100, 100))
            scene.set_animation(kitai, (1100, 100), (100, 100), 4, 5)


    except SkipException:
        return