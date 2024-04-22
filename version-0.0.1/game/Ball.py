import pyglet.sprite


class Ball(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(img=pyglet.resource.image('plasmaball.png'))

        self.velocity_x, self.velocity_y = 0.0, 0.0

    def update(self, dt):
        self.x = self.velocity_x * dt
        self.y = self.velocity_y * dt
