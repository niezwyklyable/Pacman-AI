from .constants import BG_X, BG_Y, FACTOR

class Sprite(): # an abstract class
    def __init__(self, IMG, TYPE, x, y): # x, y - centre pos
        self.IMG = IMG
        self.TYPE = TYPE
        self.x = BG_X + FACTOR * x
        self.y = BG_Y + FACTOR * y

    def draw(self, win):
        win.blit(self.IMG, (self.x - self.IMG.get_width() // 2, \
            self.y - self.IMG.get_height() // 2))
             