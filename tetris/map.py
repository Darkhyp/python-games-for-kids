import numpy as np
import pygame

import tetris
from tetris.CONFIGS import N_COLS, N_ROWS, COLOR_LIST, GRID_POS, GRID_DX, GRID_DY, LEFT_PANEL_TEXT_POS, DISPLAY_WIDTH


class Map:
    killed_lines = 0

    def __init__(self, surface):
        self.surface = surface

        self.map = np.zeros((N_COLS, N_ROWS), dtype=np.uint8)

    def check_collisions(self, block):
        is_collision = False
        for ind in block.block:
            ix = ind[0] + block.ix
            iy = ind[1] + block.iy + 1
            if not iy < N_ROWS:
                is_collision = True
                break
            if self.map[ix, iy] != 0:
                is_collision = True
                break

        return is_collision

    def put_blocks(self, block):
        for ind in block.block:
            ix = ind[0] + block.ix
            iy = ind[1] + block.iy
            self.map[ix, iy] = COLOR_LIST.index(block.color) + 1

    def check_lines(self):
        for iy in range(N_ROWS):
            if not (0 in self.map[:, iy]):
                # remove this line
                self.map[:, 1:iy+1] = self.map[:, :iy]
                self.killed_lines += 1

    def draw(self):
        for ix in range(N_COLS):
            for iy in range(N_ROWS):
                if self.map[ix, iy] != 0:
                    pygame.draw.rect(self.surface, COLOR_LIST[self.map[ix, iy]-1],
                                     (GRID_POS[0] + ix * GRID_DX + 1,
                                      GRID_POS[1] + iy * GRID_DY + 1,
                                      GRID_DX - 1,
                                      GRID_DY - 1))
        self.print_number_of_lines()

    def print_number_of_lines(self):
        # text 'Next' in the right panel
        text = tetris.game.myfont.render(str(self.killed_lines), True, (255, 255, 0))
        self.surface.blit(text, (LEFT_PANEL_TEXT_POS[0], LEFT_PANEL_TEXT_POS[1]+40))


