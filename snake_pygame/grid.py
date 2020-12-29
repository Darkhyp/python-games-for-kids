import pygame

from .CONFIGS import *


class Grid:
    def __init__(self,surface,size,step):
        self.surface = surface
        self.size = size
        self.step = step

    def draw(self):
        self.surface.fill(BACKGROUND_COLOR)
        y = 0
        for x in range(self.step[0],DISPLAY_WIDTH,self.step[0]):
            pygame.draw.line(self.surface, GRID_COLOR, (x, 0), (x, DISPLAY_WIDTH))
        for y in range(self.step[1],DISPLAY_WIDTH,self.step[1]):
            pygame.draw.line(self.surface, GRID_COLOR, (0, y), (DISPLAY_HEIGHT, y))