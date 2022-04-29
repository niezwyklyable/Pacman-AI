from .sprite import Sprite
from .constants import PACMAN_LEFT_1, PACMAN_LEFT_2, PACMAN_RIGHT_1, PACMAN_RIGHT_2,\
     PACMAN_UP_1, PACMAN_UP_2, PACMAN_DOWN_1, PACMAN_DOWN_2, PACMAN_FULL, FACTOR

class Pacman(Sprite):
    STEP = 1 # be careful with it.. (it has a linkage with collision_detection method in the Game class)

    def __init__(self, x, y):
        super().__init__(IMG=PACMAN_FULL, TYPE='PACMAN', x=x, y=y)
        self.current_dir = 'LEFT'
        self.future_dir = 'LEFT'
        #self.img_state = 0

    def set_future_dir(self, dir):
        if dir == 'LEFT':
            self.future_dir = 'LEFT'
        elif dir == 'RIGHT':
            self.future_dir = 'RIGHT'
        elif dir == 'UP':
            self.future_dir = 'UP'
        elif dir == 'DOWN':
            self.future_dir = 'DOWN'

    def change_dir(self):
        self.current_dir = self.future_dir

    def stop(self):
        self.current_dir = None

    def move(self):
        if self.current_dir == 'LEFT':
            self.x -= self.STEP * FACTOR
        elif self.current_dir == 'RIGHT':
            self.x += self.STEP * FACTOR
        elif self.current_dir == 'UP':
            self.y -= self.STEP * FACTOR
        elif self.current_dir == 'DOWN':
            self.y += self.STEP * FACTOR
        else:
            pass # do nothing if current_dir is None

    def change_image(self):
        if self.current_dir == 'LEFT':
            pass
