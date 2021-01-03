import turtle as t
from .CONFIGS import *


class Rocket:
    def __init__(self, side, step, position, color):
        # rocket position correction
        if side == 'left':
            self.dx0 = TKTURTLE_DX
        elif side == 'right':
            self.dx0 = -TKTURTLE_DX
        self.dx = self.dy = step  # object shif(velocity)
        self.ix, self.iy = position[0] + self.dx0, position[1]  # object position

        self.o_turtle = t.Turtle()
        self.o_turtle.penup()
        self.o_turtle.shape("square")
        self.o_turtle.turtlesize(stretch_len=ROCKET_WIDTH, stretch_wid=ROCKET_HEIGHT)
        self.o_turtle.color(color)
        self.o_turtle.goto(self.ix, self.iy)

        self.score = 0

    def move(self):
        if self.iy + self.dy < -HEIGHT / 2:
            self.dy = -self.dy
        if self.iy + self.dy > HEIGHT / 2:
            self.dy = -self.dy

        self.iy += self.dy

        self.o_turtle.sety(self.iy)

    def deplacer_up(self, key):
        t.onkeypress(None, key)  # Désactive la touche 'direction'
        # traitement associé à la flèche 'direction' appuyée par le joueur
        self.dy = -self.dy if self.dy < 0 else self.dy
        self.move()
        t.onkeypress(lambda: self.deplacer_up(key), key)  # Réassocie la touche 'direction' à la
        t.update()

    def deplacer_down(self, key):
        t.onkeypress(None, key)  # Désactive la touche 'direction'
        # traitement associé à la flèche 'direction' appuyée par le joueur
        self.dy = -self.dy if self.dy > 0 else self.dy
        self.move()
        t.onkeypress(lambda: self.deplacer_down(key), key)  # Réassocie la touche 'direction' à la
        t.update()
