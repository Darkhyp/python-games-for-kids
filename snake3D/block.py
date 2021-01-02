from ursina import Entity, Vec3, SmoothFollow

from snake3D.CONFIGS import IS_SNAKE_SMOOTH, MAP_SIZE_X, MAP_SIZE_Y


class Block(Entity):
    def __init__(self, **kwargs):
        if IS_SNAKE_SMOOTH:
            super().__init__(**kwargs)
            Entity(model='sphere', **kwargs).add_script(SmoothFollow(speed=30, target=self, offset=(0, 0, 0)))
        else:
            super().__init__(model='sphere', **kwargs)
        self.direction = kwargs.get('direction')

    def move(self, direction):
        self.direction = direction

        # is reached boundaries
        if direction[0] == -1 and self.position[0] <= 0:
            self.position = Vec3(MAP_SIZE_X - 1, self.position[1], self.position[2])
        elif direction[1] == -1 and self.position[1] <= 0:
            self.position = Vec3(self.position[0], MAP_SIZE_Y - 1, self.position[2])
        elif direction[0] == 1 and self.position[0] >= MAP_SIZE_X - 1:
            self.position = Vec3(0, self.position[1], self.position[2])
        elif direction[1] == 1 and self.position[1] >= MAP_SIZE_Y - 1:
            self.position = Vec3(self.position[0], 0, self.position[2])
        else:
            self.position = self.position + direction

