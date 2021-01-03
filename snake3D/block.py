from ursina import Entity, Vec3, SmoothFollow

from snake3D.CONFIGS import IS_SNAKE_SMOOTH, MAP_SIZE_X, MAP_SIZE_Y


class Block(Entity):
    def __init__(self, is_head=False,  **kwargs):
        self.is_head = is_head
        self.direction = kwargs.get('direction')

        if IS_SNAKE_SMOOTH:
            super().__init__(**kwargs)
            self.follower = Entity(model='sphere', **kwargs)
            self.follower.add_script(SmoothFollow(speed=30, target=self, offset=(0, 0, 0)))

            if self.is_head:
                # ( 90, 90, 90) - left (-1, 0, 0)
                # (-90, 90, 90) - right (1, 0, 0)
                # (0, 90, 90) - down (0, -1, 0)
                # (180, 90, 90) - up (0, 1, 0)
                self.follower.rotation = ((self.direction[1] * (self.direction[1] + 1) - self.direction[0]) * 90, 90, 90)
        else:
            super().__init__(model='sphere', **kwargs)

    def move(self, direction):
        self.direction = direction
        if self.is_head:
            self.follower.rotation = ((self.direction[1] * (self.direction[1] + 1) - self.direction[0]) * 90, 90, 90)

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

