"""
main class for "snake" classical game using pygame module
15/11/2020
Author A.V.Korovin [a.v.korovin73@gmail.com]
"""
import random
import sys
import pygame

from common import message_box, make_sound
from .CONFIGS import *
from .map import Map
from .block import Block
from .grid import Grid

pygame.font.init()
myfont = pygame.font.SysFont('monospace', 32)


class Game:
    score = []

    def __init__(self):
        self.surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('snake eats snacks')

        self.game_over = True
        self.clock = pygame.time.Clock()

        self.map = Map(self.surface)

        self.grid_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.grid = Grid(self.grid_surface, (N_ROWS, N_COLS), (GRID_DX, GRID_DY))
        self.grid.draw()

        self.next_block_surface = pygame.Surface((NEXT_PANEL_WIDTH, NEXT_PANEL_HEIGHT))
        self.next_block = Block(self.next_block_surface)
        self.next_block.init_block()

        self.isNewBlock = True

        pygame.init()

    def mainloop(self):
        make_sound(2)

        # main loop
        while self.game_over:
            pygame.time.delay(50)
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # pygame.quit()
                    sys.exit()

            # create new block
            if self.isNewBlock:
                self.isNewBlock = False
                self.current_block = Block(self.surface, draw_pos=GRID_POS)
                self.current_block.copy(self.next_block)
                self.next_block.init_block()
                self.current_block.start()

            # redraw game objects
            self.redraw()

            self.current_block.movement()
            self.check_block_collisions()

    def check_block_collisions(self):
        self.isNewBlock = self.map.check_collisions(self.current_block)
        if self.isNewBlock:
            self.current_block.signal_stop = False
            self.map.put_blocks(self.current_block)

            self.map.check_lines()

    def redraw(self):  # redraw game objects
        self.surface.blit(self.grid_surface, (0, 0))
        self.next_block_surface.fill(BLACK)
        self.next_block.draw()
        self.surface.blit(self.next_block_surface, RIGHT_PANEL_POS)
        self.current_block.draw()

        self.map.draw()

        # if pause is pressed
        if self.current_block.isPause:
            text = myfont.render('Pause', True, (255, 255, 0))
            self.surface.blit(text,
                ((self.surface.get_width()-text.get_width())/2,
                 (self.surface.get_height()-text.get_height())/2))

        pygame.display.update()
        # pygame.display.flip()

