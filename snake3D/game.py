"""
main class for "snake" classical game in 3D using ursina module
01/01/2021
Author A.V.Korovin [a.v.korovin73@gmail.com]
"""
import random

from ursina import camera, Ursina, window, color, Light, Entity, Grid, scene, print_on_screen, Wait, invoke, mouse, \
    distance, clamp

from snake3D.CONFIGS import SNAKE_POS0, MAP_SIZE_X, MAP_SIZE_Y, DISPLAY_WIDTH, DISPLAY_HEIGHT
from snake3D.snake import Snake
from snake3D.snack import Snack


class Game(Ursina):
    score = [0]

    def __init__(self):
        super().__init__()
        window.color = color.black
        window.fullscreen_size = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        window.fullscreen = True
        Light(type='ambient', color=(0.5, 0.5, 0.5, 1))
        Light(type='directional', color=(0.5, 0.5, 0.5, 1), direction=(1, 1, 1))

        self.start_new_game()

        # camera position
        camera.position = (MAP_SIZE_X/2, -20-MAP_SIZE_Y/2, -20)
        camera.rotation_x = -60

        self.game_over = True

    def create_map(self):
        Entity(model='quad', scale=(MAP_SIZE_X, MAP_SIZE_Y),
               position=(MAP_SIZE_X/2 - 0.5, MAP_SIZE_Y/2 - 0.5, 0.51),
               color=color.dark_gray)
        Entity(model=Grid(MAP_SIZE_X, MAP_SIZE_Y),
               scale=(MAP_SIZE_X, MAP_SIZE_Y),
               position=(MAP_SIZE_X/2 - 0.5, MAP_SIZE_Y/2 - 0.5, 0.5),
               color=color.white)

    def start_new_game(self):
        #     make_sound(2)
        scene.clear()

        # create map
        self.create_map()

        # put snack
        self.snack = Snack()
        self.snack.random_position()

        # snake
        self.snake = Snake(position=SNAKE_POS0)
        self.snake.isPause = False
        self.snake.start()


    def input(self, key):
        self.snake.check_keys(key)
        if key in ['mouse1', '2']:
            camera.position = (MAP_SIZE_X/2, MAP_SIZE_Y/2 - 0.5, -50)
            camera.rotation_x = camera.rotation_y = camera.rotation_z = 0
        elif key in ['mouse3', '3']:
            camera.position = (MAP_SIZE_X/2, -22, -20)
            camera.rotation_x = -57
        elif key == '-':
            camera.position = (camera.position[0], camera.position[1] + 3, camera.position[2])
        elif key == '+':
            camera.position = (camera.position[0], camera.position[1] - 3, camera.position[2])
        super().input(key)

    # main loop
    def update(self):
        camera.rotation_y += mouse.velocity[0] * 40
        camera.rotation_x -= mouse.velocity[1] * 40
        camera.rotation_x = clamp(camera.rotation_x, -90, 90)

        # snake eats snack
        if distance(self.snake.head.position, self.snack.position) < 0.1:
            # make_sound(1)
            self.score[-1] += 1
            msg = 'Your score is {0}'.format(self.score[-1])
            print_on_screen(msg, position=(-0.85, 0.45), scale=2, duration=1)
            self.snake.add_block()
            while True:
                self.snack.random_position()
                snack_pos = self.snack.position
                if not (snack_pos in list(map(lambda x: x.position, self.snake.body))):
                    break

        # snake eats its tail
        if self.snake.self_eat():
            # make_sound(3)
            self.score.append(len(self.snake.body))
            msg = 'You lost!\nYour score is {0}\n[record is {1}]'.format(self.score[-1], max(self.score))
            print_on_screen(msg, position=(-0.7, 0.15), scale=5, duration=2)
            self.snake.isPause = True
            invoke(self.start_new_game, delay=3)
