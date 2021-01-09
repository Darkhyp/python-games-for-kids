import turtle as t
import threading
import time
from common.sound import make_sound
from tennis.CONFIGS import *


class Ball(threading.Thread):
    def __init__(self, step, position, obstacles):
        threading.Thread.__init__(self)

        self.obstacles = obstacles
        self.dx = self.dy = step  # object shift (velocity)
        self.x, self.y = position[0], position[1]  # object position
        self.o_turtle = t.Turtle()
        self.o_turtle.penup()
        self.o_turtle.shape("circle")
        self.o_turtle.turtlesize(BALL_SIZE)
        self.o_turtle.color(BALL_COLOR)
        self.o_turtle.goto(self.x, self.y)

        self.score_turtle = None
        self.print_score()

        self.isPause = False

        self.daemon = True  # close thread correctly!!!

    def print_score(self):
        if self.score_turtle is not None:
            self.score_turtle.clear()
        self.score_turtle = t.Turtle()
        self.score_turtle.hideturtle()
        self.score_turtle.penup()
        self.score_turtle.color(SCORE_COLOR)
        style = ('Arial', 14, 'bold')
        self.score_turtle.setposition(0, HEIGHT / 2 - SCORE_POS)
        self.score_turtle.write("{} : {}".format(self.obstacles[0].score, self.obstacles[1].score), font=style,
                                align='center')

    def move(self):
        self.check_boundaries()

        self.x += self.dx
        self.y += self.dy
        self.o_turtle.setx(self.x)
        self.o_turtle.sety(self.y)

    def check_boundaries(self):
        # reflection from the obstacles
        for obs in self.obstacles:
            if -BALL_SPEED / 2 < obs.ix + obs.dx0 - self.x < BALL_SPEED / 2 \
                    and -ROCKET_HEIGHT * TKTURTLE_DX / 2 < self.y - obs.iy < ROCKET_HEIGHT * TKTURTLE_DX / 2:
                self.dx = -self.dx
                make_sound(4)

        # reach from the left or right sides
        if self.x + self.dx < -WIDTH / 2 or self.x + self.dx > WIDTH / 2:
            make_sound(3)
            for obs in self.obstacles:
                if self.x * obs.ix < 0:
                    obs.score += 1  # give a score ball
            self.dx = -self.dx
            self.print_score()  # update a score
            # return a ball to a start position
            self.x = 0
            self.y = 0
        # reflection from the upper and bottom sides
        if self.y + self.dy < -HEIGHT / 2 or self.y + self.dy > HEIGHT / 2:
            make_sound(1)
            self.dy = -self.dy

    def run(self):
        while True:
            try:
                time.sleep(BALL_DT)
            except Exception as e:
                print(e)
            if not self.isPause:
                self.move()
            t.update()
