import numpy as np
import pygame

import tetris
from tetris.CONFIGS import N_COLS, N_ROWS, GRID_POS, GRID_DX, GRID_DY, LEFT_PANEL_TEXT_POS, BLOCK_LIST


class Map:
    def __init__(self, surface):
        self.surface = surface
        self.new()

    def new(self):
        self.killed_lines = 0
        self.map = -np.ones((N_COLS, N_ROWS), dtype=np.int8)

    def check_collision(self, block):
        is_collision = False
        for ind in block.block:
            iy = ind[1] + block.iy
            ix = ind[0] + block.ix
            if ix >= N_COLS or iy >= N_ROWS:
                is_collision = True
                break
            if self.map[ix, iy] >= 0:
                is_collision = True
                break
        return is_collision

    def put_block(self, block):
        for ind in block.block:
            self.map[ind[0] + block.ix, ind[1] + block.iy] = block.i_color

    def check_lines(self, crunch_sound):
        for iy in range(N_ROWS):
            if not (-1 in self.map[:, iy]):
                # remove this line
                self.map[:, 1:iy+1] = self.map[:, :iy]
                self.killed_lines += 1
                crunch_sound.play()

    def draw(self):
        for ix in range(N_COLS):
            for iy in range(N_ROWS):
                if self.map[ix, iy] >= 0:
                    pygame.draw.rect(self.surface, BLOCK_LIST[self.map[ix, iy]][2],
                                     (GRID_POS[0] + ix * GRID_DX + 1,
                                      GRID_POS[1] + iy * GRID_DY + 1,
                                      GRID_DX - 1,
                                      GRID_DY - 1))
        self.print_number_of_lines()

    def print_number_of_lines(self):
        # text 'Next' in the right panel
        text = tetris.game.myfont.render(str(self.killed_lines), True, (255, 255, 0))
        self.surface.blit(text, (LEFT_PANEL_TEXT_POS[0], LEFT_PANEL_TEXT_POS[1]+40))
