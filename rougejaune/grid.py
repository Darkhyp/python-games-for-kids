import pygame

from .CONFIGS import *
from .tools import coordinate

class Grid:
    def __init__(self,win,size,step):
        self.win = win
        self.size = size
        self.step = step

    def draw(self):
        self.win.fill(BACKGROUND_COLOR)

        pygame.draw.rect(self.win, GRID_BACKGROUND, (0, self.step[1], DISPLAY_SIZE[0], DISPLAY_SIZE[1]))

        for ix in range(self.size[0]):
            for iy in range(self.size[1],0,-1):
                pygame.draw.circle(self.win, BACKGROUND_COLOR, coordinate((ix,iy)), self.step[0]/2-GRID_THICKNESS/2)

        x = 0
        y = self.step[1]
        for ix in range(self.size[0]+1):
            pygame.draw.line(self.win, GRID_COLOR, (x, DISPLAY_SIZE[1]), (x, y),GRID_THICKNESS)
            x += self.step[0]
