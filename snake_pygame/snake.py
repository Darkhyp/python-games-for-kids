import random
import threading
import time

from .CONFIGS import *
from .cube import Cube
import pygame


class Snake(threading.Thread):
    turns = {}
    isPause = False

    def __init__(self, win, pos, color):
        threading.Thread.__init__(self)

        self.win = win
        self.color = color
        self.rnd_direction()
        self.head = Cube(self.win, pos, color, self.dir)
        self.body = [self.head]

        self.daemon = True  # close thread correctly!!!


    def reset(self, pos):
        self.turns = {}
        self.rnd_direction()
        self.head = Cube(self.win, pos, self.color, self.dir)
        self.body = [self.head]
        self.isPause = False

    def run(self):
        while True:
            try:
                time.sleep(SNAKE_DT)
            except Exception as e:
                print(e)
            if not self.isPause:
                self.move()
            pygame.display.update()

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dir = (-1, 0)
            self.turns[self.head.pos] = self.dir
        if keys[pygame.K_RIGHT]:
            self.dir = (1, 0)
            self.turns[self.head.pos] = self.dir
        if keys[pygame.K_UP]:
            self.dir = (0, -1)
            self.turns[self.head.pos] = self.dir
        if keys[pygame.K_DOWN]:
            self.dir = (0, 1)
            self.turns[self.head.pos] = self.dir
        if keys[PAUSE_KEY]:
            self.isPause = not self.isPause

    def move(self):
        self.check_keys()
        for i, c in enumerate(self.body):
            p = c.pos
            if p in self.turns:
                c.move(self.turns[p])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else: # reach boundaries
                if c.dir[0] == -1 and c.pos[0] <= 0:
                    c.pos = (NROWS - 1, c.pos[1])
                elif c.dir[0] == 1 and c.pos[0] >= NROWS - 1:
                    c.pos = (0, c.pos[1])
                elif c.dir[1] == 1 and c.pos[1] >= NCOLS - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dir[1] == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], NCOLS - 1)
                else:
                    c.move(c.dir)

    def rnd_direction(self):
        if random.choice([0,1]) == 0:
            self.dir = (0, random.choice([-1,1]))
        else:
            self.dir = (random.choice([-1,1]), 0)

    def self_eat(self): # if head has the same position as tail
        return self.head.pos in list(map(lambda x: x.pos, self.body[1:]))

    def addCube(self):
        tail = self.body[-1]
        self.body.append(Cube(self.win, (tail.pos[0] - tail.dir[0], tail.pos[1] - tail.dir[1]), SNAKETAIL_COLOR))
        self.body[-1].dir = tail.dir

    def draw(self):
        for c in reversed(self.body):
            c.draw(c == self.head)
