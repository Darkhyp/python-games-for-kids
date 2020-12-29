import pygame

import tetris
from .CONFIGS import *


class Grid:
    def __init__(self,surface,size,step):
        self.surface = surface
        self.size = size
        self.step = step

    def draw(self):
        self.surface.fill(BACKGROUND_COLOR)
        x_last = GRID_POS[0] + N_COLS * GRID_DX
        y_last = GRID_POS[1] + N_ROWS * GRID_DY
        for ix in range(N_COLS + 1):
            x = GRID_POS[0] + ix * GRID_DX
            pygame.draw.line(self.surface, GRID_COLOR, (x, GRID_POS[1]), (x, y_last))
        for iy in range(N_ROWS + 1):
            y = GRID_POS[1] + iy * GRID_DY
            pygame.draw.line(self.surface, GRID_COLOR, (GRID_POS[0], y), (x_last, y))

        # text 'Next' in the right panel
        text = tetris.game.myfont.render('NEXT', True, (255, 255, 0))
        self.surface.blit(text,
                          ((RIGHT_PANEL_TEXT_POS[0] + DISPLAY_WIDTH - text.get_height()) / 2,
                           RIGHT_PANEL_TEXT_POS[1]))

        # text 'Lines:' in the left panel
        text = tetris.game.myfont.render('Lines', True, (255, 255, 0))
        self.surface.blit(text, (LEFT_PANEL_TEXT_POS[0], LEFT_PANEL_TEXT_POS[1]))

        # draw rectangle for the next block
        pygame.draw.rect(self.surface, GRID_COLOR, RIGHT_PANEL_POS + (NEXT_PANEL_WIDTH, NEXT_PANEL_HEIGHT), 4)
