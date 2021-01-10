"""
main class for "snake" classical game using pygame module
15/11/2020
Author A.V.Korovin [a.v.korovin73@gmail.com]
"""
import random
import sys
import pygame

from common import message_box, make_sound
from snake_pygame.CONFIGS import *
from snake_pygame.snake import Snake
from snake_pygame.cube import Cube
from snake_pygame.grid import Grid

pygame.font.init()
myfont = pygame.font.SysFont('monospace', 32)


class Game:
    """
    Main class for initializing the game engine and objects
    """
    score = []

    def __init__(self):
        self.surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('snake eats snacks')

        self.game_over = True
        self.clock = pygame.time.Clock()

        pygame.init()

        self.grid_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.grid = Grid(self.grid_surface, (N_ROWS, N_COLS), (GRID_DX, GRID_DY))
        self.grid.draw()

        self.snake = Snake(self.surface, SNAKE_POS0, SNAKE_COLOR)
        self.snack = Cube(self.surface, (random.randrange(N_ROWS), random.randrange(N_ROWS)), SNACK_COLOR)

    def mainloop(self):
        """
        main game loop
        """

        # make start sound
        make_sound(2)

        self.snake.start()

        # main loop
        while self.game_over:
            pygame.time.delay(50)
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # pygame.quit()
                    sys.exit()

            # redraw game objects
            self.redraw()

            # snake eats snack
            if self.snake.head.pos == self.snack.pos:
                make_sound(1)
                self.snake.addCube()
                while True:
                    snack_pos = (random.randrange(N_ROWS), random.randrange(N_ROWS))
                    if not (snack_pos in list(map(lambda x: x.pos, self.snake.body))):
                        break
                self.snack = Cube(self.surface, snack_pos, SNACK_COLOR)

            # snake eats its tail
            if self.snake.self_eat():
                make_sound(3)
                self.score.append(len(self.snake.body))
                msg = 'Your score is {0} [record is {1}]'.format(self.score[-1], max(self.score))
                message_box('You lost!', msg + '\nPlay again')
                self.snake.reset(SNAKE_POS0)
            else:
                # move snake
                self.snake.check_keys()

    def redraw(self):  # redraw game objects
        # self.grid.draw()
        self.surface.blit(self.grid_surface, (0, 0))
        self.snack.draw()
        self.snake.draw()

        # if pause is pressed
        if self.snake.isPause:
            text = myfont.render('Pause', True, (255, 255, 0))
            self.surface.blit(text,
                ((self.surface.get_width()-text.get_width())/2,
                 (self.surface.get_height()-text.get_height())/2))

        pygame.display.update()
