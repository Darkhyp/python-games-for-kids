import random
import threading
import time

from ursina import held_keys, Vec3, Wait, destroy, color

from .CONFIGS import SNAKE_COLOR, SNAKE_DT, KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, KEY_PAUSE, SNAKE_TAIL_COLOR, \
    SNAKE_POS0, EYE_COLOR
from .block import Block

KEYS = [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN]
DIRECTIONS = {
    KEY_LEFT: Vec3(-1, 0, 0),
    KEY_RIGHT: Vec3(1, 0, 0),
    KEY_DOWN: Vec3(0, -1, 0),
    KEY_UP: Vec3(0, 1, 0)
    }


class Snake(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.new(SNAKE_POS0)

        self.daemon = True  # close thread correctly!!!

    def new(self, position):
        self.turns = {}
        self.rnd_direction()
        self.head = Block(is_head=True, position=position, color=SNAKE_COLOR, direction=self.direction, texture=EYE_COLOR)
        self.body = [self.head]
        self.isPause = False

    # def reset(self):
    #     print('self.body=', self.body)
    #     for body in self.body:
    #         body.model = color.black
    #         body.clear()
    #         destroy(body)
    #     print('self.body=', self.body)
    #     self.new(SNAKE_POS0)

    def run(self):
        while True:
            try:
                time.sleep(SNAKE_DT)
            except Exception as e:
                print(e)
            if not self.isPause:
                self.move()

    def check_keys(self, key):
        if key in DIRECTIONS.keys():
            self.direction = DIRECTIONS[key]
            self.turns[self.head.position] = self.direction
        if key == KEY_PAUSE:
            self.isPause = not self.isPause

    def move(self):
        for i, c in enumerate(self.body):
            p = c.position
            if p in self.turns:
                c.move(self.turns[p])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.direction)

    def rnd_direction(self):
        if random.choice([0, 1]) == 0:
            self.direction = Vec3(0, random.choice([-1, 1]), 0)
        else:
            self.direction = Vec3(random.choice([-1, 1]), 0, 0)

    def self_eat(self): # if head has the same position as tail
        return self.head.position in list(map(lambda x: x.position, self.body[1:]))

    def add_block(self):
        tail = self.body[-1]
        self.body.append(Block(position=tail.position - tail.direction, color=SNAKE_TAIL_COLOR, direction=tail.direction))
