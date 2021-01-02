from snake3D.CONFIGS import SNACK_COLOR, MAP_SIZE_X, MAP_SIZE_Y
from random import randrange
from ursina import Vec3, Entity


class Snack(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='sphere',  color=SNACK_COLOR,  **kwargs)

    def random_position(self):
        self.position = Vec3(randrange(MAP_SIZE_X), randrange(MAP_SIZE_Y), 0)

