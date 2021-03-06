import time
import turtle as t
from common import make_sound
from .ball import Ball
from .racket import Racket
from .CONFIGS import *


class Game:
    """
    Main class for initializing the game engine and objects
    """
    def __init__(self):
        self.turtle_init()

        self.left_racket = Racket('left', ROCKET_SPEED, (-WIDTH/2+ROCKETS_DXPOS,0),ROCKET1_COLOR)
        self.right_racket = Racket('right', ROCKET_SPEED, (WIDTH/2-ROCKETS_DXPOS,0),ROCKET2_COLOR)

        self.ball = Ball(BALL_SPEED, (0, 0), (self.left_racket, self.right_racket))
        self.message_turtle = None

        t.update()
        make_sound(4)

    @staticmethod
    def turtle_init():
        t.title("Game - Tennis")
        t.tracer(0, 0)
        t.hideturtle()
        t.bgcolor(BGCOLOR)
        t.setup(height=HEIGHT,width=WIDTH)

    def activate_keys(self):
        t.listen()  # Déclenche l’écoute du clavier
        # Associe à une touche a une fonction:
        t.onkeypress(lambda: self.left_racket.deplacer_up(ROCKET1_KEY_UP), ROCKET1_KEY_UP)
        t.onkeypress(lambda: self.left_racket.deplacer_down(ROCKET1_KEY_DOWN), ROCKET1_KEY_DOWN)
        t.onkeypress(lambda: self.right_racket.deplacer_up(ROCKET2_KEY_UP), ROCKET2_KEY_UP)
        t.onkeypress(lambda: self.right_racket.deplacer_down(ROCKET2_KEY_DOWN), ROCKET2_KEY_DOWN)
        t.onkeypress(lambda: self.pause(), PAUSE_KEY)
        t.onkeypress(lambda: self.restart(), RESTART_KEY)

        self.ball.start()
        t.mainloop()  # Place le programme en position d’attente d’une action du joueur

    def pause(self):
        self.ball.isPause = not self.ball.isPause
        if self.ball.isPause:
            self.print_message('Pause')
        else:
            self.message_turtle.clear()

    def restart(self):
        self.right_racket.score = self.left_racket.score = 0
        self.ball.x = 0
        self.ball.y = 0
        self.ball.print_score()
        self.ball.move()
        t.update()
        self.print_message('Restart game')

        time.sleep(1)
        self.message_turtle.clear()

    def print_message(self,msg):
        self.message_turtle = t.Turtle()
        self.message_turtle.hideturtle()
        self.message_turtle.penup()
        self.message_turtle.color(MESSAGE_COLOR)
        style = ('Arial', 14, 'bold')
        self.message_turtle.setposition(0, 0)
        self.message_turtle.write(msg, font=style, align='center')
