from .pacman import Pacman
from .constants import BLINKY_RIGHT_1, BLINKY_RIGHT_2, BLINKY_LEFT_1, BLINKY_LEFT_2, \
    BLINKY_UP_1, BLINKY_UP_2, BLINKY_DOWN_1, BLINKY_DOWN_2, \
    PINKY_DOWN_1, PINKY_DOWN_2, PINKY_LEFT_1, PINKY_LEFT_2, PINKY_UP_1, PINKY_UP_2, PINKY_RIGHT_1, PINKY_RIGHT_2, \
    INKY_DOWN_1, INKY_DOWN_2, INKY_LEFT_1, INKY_LEFT_2, INKY_RIGHT_1, INKY_RIGHT_2, INKY_UP_1, INKY_UP_2, \
    CLYDE_DOWN_1, CLYDE_DOWN_2, CLYDE_LEFT_1, CLYDE_LEFT_2, CLYDE_RIGHT_1, CLYDE_RIGHT_2, CLYDE_UP_1,\
    CLYDE_UP_2, BLUE_1, BLUE_2, GREY_1, GREY_2, EYES_DOWN, EYES_LEFT, EYES_RIGHT, EYES_UP, \
    GHOST_CAPTION_1, GHOST_CAPTION_2, GHOST_CAPTION_3, GHOST_CAPTION_4, \
    BG_X, BG_Y, FACTOR
import random
from .sprite import Sprite

class Ghost(Pacman):
    def __init__(self, x, y, STEP, GO_OUT_THRESHOLD, HALF_BLUE_THRESHOLD):
        super().__init__(x=x, y=y, STEP=STEP)
        self.IMG = None
        self.TYPE = 'GHOST'
        self.STEP_NORMAL = STEP
        self.STEP_SLOWER = STEP * 0.55 # in the tunnel
        self.STEP_FASTER = STEP * 6 # during home returning
        self.stay_at_home = True # if it is True the ghost cannot escape the home (the centre of the map)
        self.GO_OUT_THRESHOLD = GO_OUT_THRESHOLD # number of frames to go out (escape the home)
        self.HALF_BLUE_THRESHOLD = HALF_BLUE_THRESHOLD # number of frames to change state from FULL BLUE to HALF BLUE
        self.NORMAL_THRESHOLD = 1.2 * HALF_BLUE_THRESHOLD # number of frames to change state from HALF BLUE to NORMAL
        self.state = 'NORMAL'
        self.STATES_DOWN = []
        self.STATES_DOWN_NORMAL = []
        self.STATES_UP = []
        self.STATES_UP_NORMAL = []
        self.STATES_LEFT = []
        self.STATES_LEFT_NORMAL = []
        self.STATES_RIGHT = []
        self.STATES_RIGHT_NORMAL = []
        self.FULL_BLUE = [BLUE_1, BLUE_1, BLUE_2, BLUE_2]
        self.HALF_BLUE = [BLUE_1, BLUE_1, GREY_1, GREY_1, BLUE_2, BLUE_2, GREY_2, GREY_2]
        self.EYES_LEFT = [EYES_LEFT]
        self.EYES_RIGHT = [EYES_RIGHT]
        self.EYES_UP = [EYES_UP]
        self.EYES_DOWN = [EYES_DOWN]
        self.frames = 0
        self.eaten = False # when it is True it means that the ghost was eaten by Pacman but still not started path finding process
        self.return_home_path = [] # list of dirs for the ghost to reach the goal (home center)
        self.follow_pacman_path = [] # list of dirs for the ghost to follow the Pacman (tracking) - actually only the last (the first for the ghost) dir is sufficient

    def change_state(self, state):
        if state == 'NORMAL':
            self.state = 'NORMAL'
            self.STATES_LEFT = self.STATES_LEFT_NORMAL
            self.STATES_RIGHT = self.STATES_RIGHT_NORMAL
            self.STATES_UP = self.STATES_UP_NORMAL
            self.STATES_DOWN = self.STATES_DOWN_NORMAL
        elif state == 'FULL_BLUE':
            self.state = 'FULL_BLUE'
            self.frames = 0 # needed for the recovery process
            self.STATES_LEFT = self.FULL_BLUE
            self.STATES_RIGHT = self.FULL_BLUE
            self.STATES_UP = self.FULL_BLUE
            self.STATES_DOWN = self.FULL_BLUE
        elif state == 'HALF_BLUE':
            self.state = 'HALF_BLUE'
            self.STATES_LEFT = self.HALF_BLUE
            self.STATES_RIGHT = self.HALF_BLUE
            self.STATES_UP = self.HALF_BLUE
            self.STATES_DOWN = self.HALF_BLUE
        elif state == 'EYES':
            self.state = 'EYES'
            self.eaten = True
            self.STEP = self.STEP_FASTER
            self.STATES_LEFT = self.EYES_LEFT
            self.STATES_RIGHT = self.EYES_RIGHT
            self.STATES_UP = self.EYES_UP
            self.STATES_DOWN = self.EYES_DOWN
    
    def draw(self, win):
        win.blit(self.IMG, (self.x - self.IMG.get_width() // 2, \
             self.y - self.IMG.get_height() // 2))

    # it is necessary to allow the ghost to go out (escape the home) when fleeing from Pacman is activated
    def generate_random_dir(self):
        dir = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        self.set_future_dir(dir)

    def take_dir_to_go_home(self):
        if self.return_home_path:
            dir = self.return_home_path.pop()
        else:
            dir = 'DOWN' # the last step to go home
        self.set_future_dir(dir)

    def change_dir_to_opposite(self):
        if self.current_dir == 'LEFT':
            self.set_future_dir('RIGHT')
            self.change_dir()
        elif self.current_dir == 'RIGHT':
            self.set_future_dir('LEFT')
            self.change_dir()
        elif self.current_dir == 'UP':
            self.set_future_dir('DOWN')
            self.change_dir()
        elif self.current_dir == 'DOWN':
            self.set_future_dir('UP')
            self.change_dir()

    def take_dir_to_follow_pacman(self, pacman_x, pacman_y):
        if self.follow_pacman_path:
            dir = self.follow_pacman_path.pop()
            self.set_future_dir(dir)
        else: # if the path is spent (empty), try to find the pacman between the nodes (intersections)
            # consider the tunnel case firstly
            if self.y == pacman_y and self.y == BG_Y + 116 * FACTOR and (pacman_x < BG_X + 52 * FACTOR or pacman_x > BG_X + 172 * FACTOR):
                if self.x == BG_X + 52 * FACTOR:
                    self.set_future_dir('LEFT')
                elif self.x == BG_X + 172 * FACTOR:
                    self.set_future_dir('RIGHT')
            # check vertically
            elif self.x == pacman_x:
                if self.y > pacman_y:
                    self.set_future_dir('UP')
                elif self.y < pacman_y:
                    self.set_future_dir('DOWN')
            # check horizontally
            elif self.y == pacman_y:
                if self.x > pacman_x:
                    self.set_future_dir('LEFT')
                elif self.x < pacman_x:
                    self.set_future_dir('RIGHT')

    def take_dir_to_flee_from_pacman(self, possible_dirs):
        if self.follow_pacman_path: # sometimes there is no path due to the first execution of collision_detection method in the Game class
            dir_to_pacman = self.follow_pacman_path.pop()
            dirs = {'LEFT', 'RIGHT', 'DOWN', 'UP'}
            dirs.remove(dir_to_pacman)
            dirs = tuple(dirs)
            while True:
                random_dir = random.choice(dirs)
                if random_dir in possible_dirs:
                    self.set_future_dir(random_dir)
                    self.change_dir() # assign future_dir to current_dir
                    break

class Blinky(Ghost):
    def __init__(self, x, y, STEP, GO_OUT_THRESHOLD, HALF_BLUE_THRESHOLD):
        super().__init__(x=x, y=y, STEP=STEP, GO_OUT_THRESHOLD=GO_OUT_THRESHOLD, HALF_BLUE_THRESHOLD=HALF_BLUE_THRESHOLD)
        self.IMG = BLINKY_LEFT_1
        self.STATES_LEFT_NORMAL = [BLINKY_LEFT_1, BLINKY_LEFT_2]
        self.STATES_RIGHT_NORMAL = [BLINKY_RIGHT_1, BLINKY_RIGHT_2]
        self.STATES_UP_NORMAL = [BLINKY_UP_1, BLINKY_UP_2]
        self.STATES_DOWN_NORMAL = [BLINKY_DOWN_1, BLINKY_DOWN_2]
        self.stay_at_home = False
        self.change_state('NORMAL')
        self.SUBTYPE = 'BLINKY'

class Inky(Ghost):
    CHANGE_MODE_THRESHOLD = 600
    FLEEING_RANGE = 50

    def __init__(self, x, y, STEP, GO_OUT_THRESHOLD, HALF_BLUE_THRESHOLD):
        super().__init__(x=x, y=y, STEP=STEP, GO_OUT_THRESHOLD=GO_OUT_THRESHOLD, HALF_BLUE_THRESHOLD=HALF_BLUE_THRESHOLD)
        self.current_dir = 'UP'
        self.future_dir = 'UP'
        self.IMG = INKY_UP_1
        self.STATES_LEFT_NORMAL = [INKY_LEFT_1, INKY_LEFT_2]
        self.STATES_RIGHT_NORMAL = [INKY_RIGHT_1, INKY_RIGHT_2]
        self.STATES_UP_NORMAL = [INKY_UP_1, INKY_UP_2]
        self.STATES_DOWN_NORMAL = [INKY_DOWN_1, INKY_DOWN_2]
        self.change_state('NORMAL')
        self.SUBTYPE = 'INKY'
        self.mode = 'being_like_blinky'
        self.frames_to_change_mode = 0 # it is totally different than self.frames

    def change_mode(self):
        self.mode = random.choice(['being_like_blinky', 'being_like_pinky', 'being_like_clyde'])
        self.frames_to_change_mode = 0 # reset

class Pinky(Ghost):
    def __init__(self, x, y, STEP, GO_OUT_THRESHOLD, HALF_BLUE_THRESHOLD):
        super().__init__(x=x, y=y, STEP=STEP, GO_OUT_THRESHOLD=GO_OUT_THRESHOLD, HALF_BLUE_THRESHOLD=HALF_BLUE_THRESHOLD)
        self.current_dir = 'DOWN'
        self.future_dir = 'DOWN'
        self.IMG = PINKY_DOWN_1
        self.STATES_LEFT_NORMAL = [PINKY_LEFT_1, PINKY_LEFT_2]
        self.STATES_RIGHT_NORMAL = [PINKY_RIGHT_1, PINKY_RIGHT_2]
        self.STATES_UP_NORMAL = [PINKY_UP_1, PINKY_UP_2]
        self.STATES_DOWN_NORMAL = [PINKY_DOWN_1, PINKY_DOWN_2]
        self.change_state('NORMAL')
        self.SUBTYPE = 'PINKY'

class Clyde(Ghost):
    FLEEING_RANGE = 50

    def __init__(self, x, y, STEP, GO_OUT_THRESHOLD, HALF_BLUE_THRESHOLD):
        super().__init__(x=x, y=y, STEP=STEP, GO_OUT_THRESHOLD=GO_OUT_THRESHOLD, HALF_BLUE_THRESHOLD=HALF_BLUE_THRESHOLD)
        self.current_dir = 'UP'
        self.future_dir = 'UP'
        self.IMG = CLYDE_UP_1
        self.STATES_LEFT_NORMAL = [CLYDE_LEFT_1, CLYDE_LEFT_2]
        self.STATES_RIGHT_NORMAL = [CLYDE_RIGHT_1, CLYDE_RIGHT_2]
        self.STATES_UP_NORMAL = [CLYDE_UP_1, CLYDE_UP_2]
        self.STATES_DOWN_NORMAL = [CLYDE_DOWN_1, CLYDE_DOWN_2]
        self.change_state('NORMAL')
        self.SUBTYPE = 'CLYDE'

class GhostCaption(Sprite):
    HIDE_THRESHOLD = 50

    def __init__(self, x, y, ghost_score):
        super().__init__(IMG=None, TYPE='GHOST_CAPTION', x=x, y=y)
        if ghost_score == 200:
            self.type_num = 0
        elif ghost_score == 400:
            self.type_num = 1
        elif ghost_score == 800:
            self.type_num = 2
        elif ghost_score == 1600:
            self.type_num = 3

        self.GHOST_CAPTIONS = [GHOST_CAPTION_1, GHOST_CAPTION_2, GHOST_CAPTION_3, GHOST_CAPTION_4]
        self.IMG = self.GHOST_CAPTIONS[self.type_num]
        self.frames = 0
