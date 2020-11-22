import random
import tkinter
import tkinter.messagebox
import turtle as t

import pygame

from fturtle.fturtle import graphics_init
from .CONFIGS import *
from .snake import Snake
from .cube import Cube
from .grid import Grid


def message_box(subject, content):
    root = tkinter.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    tkinter.messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


class Game:
    score = []

    def __init__(self):
        graphics_init((DISPLAY_WIDTH, DISPLAY_HEIGHT))

        self.flag = True
        self.clock = pygame.time.Clock()

        self.grid = Grid((NROWS, NCOLS), (GRID_DX, GRID_DY))
        self.snake = Snake(SNAKE_POS0, SNAKE_COLOR)
        self.snack = Cube((random.randrange(NROWS), random.randrange(NROWS)), SNACK_COLOR)

        self.activate_keys()

    def activate_keys(self):
        t.listen()  # Déclenche l’écoute du clavier
        # Associe à une touche a une fonction:
        t.onkeypress(lambda: self.deplacer_key("Left"), "Left")
        t.onkeypress(lambda: self.deplacer_key("Right"), "Right")
        t.onkeypress(lambda: self.deplacer_key("Up"), "Up")
        t.onkeypress(lambda: self.deplacer_key("Down"), "Down")
        t.mainloop()  # Place le programme en position d’attente d’une action du joueur

    def mainloop(self):
        # main loop
        while self.flag:
            pygame.time.delay(150)
            self.clock.tick(10)

            # redraw game objects
            self.redraw()

            # snake eats snack
            if self.snake.head.pos == self.snack.pos:
                self.snake.addCube()
                while True:
                    snack_pos = (random.randrange(NROWS), random.randrange(NROWS))
                    if not (snack_pos in list(map(lambda x: x.pos, self.snake.body))):
                        break
                self.snack = Cube(self.win, snack_pos, SNACK_COLOR)

            # snake eats its tail
            if self.snake.self_eat():
                self.score.append(len(self.snake.body))
                msg = 'Your score is {0} [record is {1}]'.format(self.score[-1], max(self.score))
                message_box('You lost!', msg + '\nPlay again')
                self.snake.reset(SNAKE_POS0)
            else:
                # move snake
                self.snake.move()

    def redraw(self): # redraw game objects
        self.grid.draw()
        self.snack.draw()
        self.snake.draw()
        pygame.display.update()
