from .CONFIGS import *
import pygame


class Cube:
    def __init__(self, win, pos, color=SNAKE_COLOR, dir=(1, 0)):
        self.win = win
        self.pos = pos
        self.color = color
        self.dir = dir

    def move(self,dir):
        self.dir = dir
        self.pos = (self.pos[0]+dir[0],self.pos[1]+dir[1])

    def draw(self,isEyes=False):
        pygame.draw.rect(self.win,self.color,
                         (self.pos[0] * GRID_DX + 1,
                          self.pos[1] * GRID_DY + 1,
                          GRID_DX - 2,
                          GRID_DY - 2
                           ))
        if isEyes:
            centrex = GRID_DX // 2
            centrey = GRID_DY // 2
            radius = 3
            x0 = self.pos[0] * GRID_DX + centrex
            y0 = self.pos[1] * GRID_DY + centrey
            if self.dir[0]!=0:
                circle1 = (x0 + centrex/2*self.dir[0], y0 - centrey/2)
                circle2 = (x0 + centrex/2*self.dir[0], y0 + centrey/2)
            else:
                circle1 = (x0 - centrex/2, y0 + centrey/2*self.dir[1])
                circle2 = (x0 + centrex/2, y0 + centrey/2*self.dir[1])
            pygame.draw.circle(self.win, EYE_COLOR, circle1, radius)
            pygame.draw.circle(self.win, EYE_COLOR, circle2, radius)
