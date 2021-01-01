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
    n_level = 1
    n_blocks = 0
    score = []

    def __init__(self):
        self.surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('tetris')

        self.clock = pygame.time.Clock()

        self.map = Map(self.surface)

        self.grid_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.grid = Grid(self.grid_surface, (N_ROWS, N_COLS), (GRID_DX, GRID_DY))
        self.grid.draw()

        self.next_block_surface = pygame.Surface((NEXT_PANEL_WIDTH, NEXT_PANEL_HEIGHT))
        self.next_block = Block(self.next_block_surface)

        self.is_new_game = True

        pygame.init()

    def start_new_game(self):
        while True:
            pygame.time.delay(50)
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # pygame.quit()
                    sys.exit()

            if self.is_new_game:
                self.next_block.init_block()
                self.is_new_block = True
                self.game_over = False
                self.block_speed = BLOCK_SPEED
                self.game_loop()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_n]:
                self.map.new()
                self.is_new_game = True

    def game_loop(self):
        make_sound(2)

        # main loop
        while not self.game_over:
            pygame.time.delay(50)
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # pygame.quit()
                    sys.exit()

            # create new block
            if self.is_new_block:
                self.is_new_block = False
                self.n_blocks += 1
                if self.n_blocks % 20 == 0:
                    self.n_level += 1
                    self.block_speed *= 0.8
                self.current_block = Block(self.surface, speed=self.block_speed, map=self.map, draw_pos=GRID_POS)
                self.current_block.copy(self.next_block)
                self.next_block.init_block()
                # check is game is over
                if self.map.check_collision(self.current_block):
                    self.current_block.draw()
                    # game is over
                    self.print_central_text('press "N" for a new game')
                    pygame.display.update()
                    self.is_new_game = False
                    self.game_over = True
                    break
                else:
                    self.current_block.start()

            self.current_block.movement()
            self.check_block_collisions()

            # redraw game objects
            self.redraw()

    def check_block_collisions(self):
        self.is_new_block = self.current_block.is_collision
        if self.is_new_block:
            self.map.put_block(self.current_block)
            self.current_block = None

            self.map.check_lines()

    def redraw(self):  # redraw game objects
        # draw grid
        self.surface.blit(self.grid_surface, (0, 0))

        # draw next block
        self.next_block_surface.fill(BLACK)
        self.next_block.draw()

        # draw fixed blocks
        self.map.draw()

        # draw current block
        if self.current_block is not None:
            self.surface.blit(self.next_block_surface, RIGHT_PANEL_POS)
            self.current_block.draw()

            # draw text 'Pause' if pause key is pressed
            if self.current_block.isPause:
                self.print_central_text('Pause')

        # draw text level number
        if self.game_over:
            self.print_central_text('Game over', is_head=True)
        else:
            self.print_central_text(f'Level {self.n_level}', is_head=True)

        pygame.display.update()
        # pygame.display.flip()

    def print_central_text(self, text, is_head=False):
        text = myfont.render(text, True, (255, 255, 0))
        if is_head:
            self.surface.blit(text,
                              ((self.surface.get_width() - text.get_width()) / 2,
                               10 + text.get_height()/2))
        else:
            self.surface.blit(text,
                              ((self.surface.get_width() - text.get_width()) / 2,
                               (self.surface.get_height() - text.get_height()) / 2))
