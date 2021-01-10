"""
main class for "snake" classical game in 3D using ursina module
01/01/2021
Author A.V.Korovin [a.v.korovin73@gmail.com]
"""
import os
from ursina import camera, Ursina, window, color, Light, Entity, scene, print_on_screen, invoke, mouse, \
    distance, clamp, Grid, Sky, audio, Shader

from snake3D.CONFIGS import MAP_SIZE_X, MAP_SIZE_Y, DISPLAY_WIDTH, DISPLAY_HEIGHT
from snake3D.snake import Snake
from snake3D.snack import Snack

# game_sound = Audio(clip=r'C:\Windows\Media\tada.wav', loop=False, autoplay=False)
game_sound = audio.Audio(clip=os.path.join(os.path.dirname(__file__), 'tada.wav'), loop=True, autoplay=True)


class Game(Ursina):
    """
    Main class for initializing the game engine and objects
    """
    score = [0]

    def __init__(self):
        """
        create a game engine
        """
        super().__init__()
        window.color = color.black
        window.fullscreen_size = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        # window.fullscreen = True

        window.fullscreen = False
        window.boardless = False
        # window.fps_counter.enabled = False
        # window.exit_button.visible = False
        window.title = 'Snake3D'

        Light(type='ambient', color=(0.25, 0.25, 0.25, 1))
        Light(type='directional', color=(0.5, 0.5, 0.5, 1), direction=(1, 1, 1))
        Sky(scale=150, double_side=True)

        self.start_new_game()

        # camera position
        camera.position = (MAP_SIZE_X/2, -20-MAP_SIZE_Y/2, -20)
        camera.rotation_x = -60

        self.game_over = True

    def create_map(self):
        """
        create game background
        """
        Entity(model='quad', scale=(MAP_SIZE_X, MAP_SIZE_Y),
               position=(MAP_SIZE_X/2 - 0.5, MAP_SIZE_Y/2 - 0.5, 0.51),
               color=color.dark_gray)
        Entity(model=Grid(MAP_SIZE_X, MAP_SIZE_Y),
               scale=(MAP_SIZE_X, MAP_SIZE_Y),
               position=(MAP_SIZE_X/2 - 0.5, MAP_SIZE_Y/2 - 0.5, 0.5),
               color=color.white)

    def start_new_game(self):
        """
        start a new game
        """

        # make start sound
        game_sound.play()

        # clear the last scene
        scene.clear()

        # create a map
        self.create_map()

        # put snack
        self.snack = Snack()
        self.snack.random_position()

        # create a snake
        self.snake = Snake()
        self.snake.isPause = False
        self.snake.start()

    def input(self, key):
        """
        check game events (keystrokes, mouse movements)
        """
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

    def update(self):
        """
        update main game loop
        """
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
            # self.snake.reset()
