import random
import threading
import time

from .CONFIGS import *
from .cube import Cube
import pygame


class Snake(threading.thread):
    turns = {}

    def __init__(self, win, pos, color):
        self.win = win
        self.color = color
        self.rnd_direction()
        self.head = Cube(self.win, pos, color, self.dir)
        self.body = [self.head]

    def run(self):
        while True:
            try:
                time.sleep(SNAKE_DT)
            except Exception as e:
                print(e)
            if not self.isPause:
                self.move()
            t.update()

    def check_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_LEFT]:
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.dir = (-1, 0)
                    self.turns[self.head.pos] = self.dir
                # elif keys[pygame.K_RIGHT]:
                elif event.key == pygame.K_RIGHT:
                    self.dir = (1, 0)
                    self.turns[self.head.pos] = self.dir
                # elif keys[pygame.K_UP]:
                elif event.key == pygame.K_UP:
                    self.dir = (0, -1)
                    self.turns[self.head.pos] = self.dir
                # elif keys[pygame.K_DOWN]:
                elif event.key == pygame.K_DOWN:
                    self.dir = (0, 1)
                    self.turns[self.head.pos] = self.dir

    def move(self):
        for i, c in enumerate(self.body):
            p = c.pos
            if p in self.turns:
                c.move(self.turns[p])
                if p == len(self.body) - 1:
                    self.turns.pop(p)
            else:
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
        if random.randrange(2) == 0:
            self.dir = (0, random.randrange(-1, 2, 2))
        else:
            self.dir = (random.randrange(-1, 2, 2), 0)

    def reset(self, pos):
        self.turns = {}
        self.rnd_direction()
        self.head = Cube(self.win, pos, self.color, self.dir)
        self.body = [self.head]

    def addCube(self):
        tail = self.body[-1]
        self.body.append(Cube(self.win, (tail.pos[0] - tail.dir[0], tail.pos[1] - tail.dir[1]), SNAKETAIL_COLOR))
        self.body[-1].dir = tail.dir

    def draw(self):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(True)
            else:
                c.draw()
