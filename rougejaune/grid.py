import pygame

from .CONFIGS import *
from .tools import coordinate

class Grid:
    def __init__(self,surface,size,step):
        self.surface = surface
        self.size = size
        self.step = step

    def draw(self):
        self.surface.fill(BACKGROUND_COLOR)

        # game region for placed balls
        pygame.draw.rect(self.surface, GRID_BACKGROUND, (0, self.step[1], DISPLAY_SIZE[0], DISPLAY_SIZE[1]))

        # holes for placed balls
        for ix in range(self.size[0]):
            for iy in range(self.size[1]-1,-1,-1):
                pygame.draw.circle(self.surface, BACKGROUND_COLOR, coordinate((ix,iy)), self.step[0]/2-GRID_THICKNESS/2)

        # put separators
        for x in range(0,self.step[0]*self.size[0]+1,self.step[0]):
            pygame.draw.line(self.surface, GRID_COLOR, (x, DISPLAY_SIZE[1]), (x, self.step[1]),GRID_THICKNESS)
