from character import Character


class Player(Character):
    IMG_PATH = 'collage.png'


class Boss(Character):
    pass


class BossChina(Boss):
    IMG_PATH = 'kitai.png'
    ROWS = 1
    COLS = 1