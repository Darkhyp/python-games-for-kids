import random
import threading
import time

import pygame

from tetris.CONFIGS import COLOR_LIST, BLOCK_LIST, N_COLS, GRID_DX, GRID_DY, GRID_POS, PLAYER_LEFT, PLAYER_RIGHT, \
    PAUSE_KEY, NEXT_PANEL_WIDTH, NEXT_PANEL_HEIGHT, PLAYER_UP, BLOCK_SPEED, PLAYER_DOWN


class Block(threading.Thread):
    block = []
    def __init__(self, surface, pos=(0, 0), draw_pos=(0, 0)):
        threading.Thread.__init__(self)

        self.surface = surface
        self.ix = pos[0]
        self.iy = pos[1]
        self.draw_pos = draw_pos
        self.speed = BLOCK_SPEED

        self.isPause = False
        self.signal_stop = True
        self.daemon = True  # close thread correctly!!!

    def copy(self, blc):
        self.block = blc.block
        self.color = blc.color
        self.ix_max = blc.ix_max
        self.iy_max = blc.iy_max
        self.ix = (N_COLS + self.ix_max) // 2
        self.iy = 0

    def init_block(self):
        # random choice of the block and its color
        self.color = random.choice(COLOR_LIST)
        self.block = random.choice(BLOCK_LIST)

        # max dimensions
        self.ix_max = 0
        self.iy_max = 0
        for coordinate in self.block:
            if self.ix_max < coordinate[0]:
                self.ix_max = coordinate[0]
            if self.iy_max < coordinate[1]:
                self.iy_max = coordinate[1]
        # define center
        self.draw_pos = ((NEXT_PANEL_WIDTH - (self.ix_max + 1) * GRID_DX) / 2,
                         (NEXT_PANEL_HEIGHT - (self.iy_max + 1) * GRID_DY) / 2)

    def draw(self):
        for coordinate in self.block:
            pygame.draw.rect(self.surface, self.color,
                             (self.draw_pos[0] + (self.ix + coordinate[0]) * GRID_DX + 1,
                              self.draw_pos[1] + (self.iy + coordinate[1]) * GRID_DY + 1,
                              GRID_DX - 1,
                              GRID_DY - 1))

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[PLAYER_LEFT] and self.ix != 0:
            self.ix -= 1
        if keys[PLAYER_RIGHT] and self.ix + self.ix_max + 1 < N_COLS:
            self.ix += 1
        # rotate object
        if keys[PLAYER_UP]:
            rotated_object = set()
            for coordinate in self.block:
                rotated_object.add((self.iy_max - coordinate[1], coordinate[0]))
            self.block = rotated_object
            self.ix_max, self.iy_max = self.iy_max, self.ix_max
        if keys[PLAYER_DOWN]:
            self.speed = BLOCK_SPEED/5
        if keys[PAUSE_KEY]:
            self.isPause = not self.isPause

    def fall(self):
        self.iy += 1

    def run(self):
        while self.signal_stop:
            try:
                time.sleep(self.speed)
            except Exception as e:
                print(e)
            if not self.isPause:
                self.fall()
            pygame.display.update()
