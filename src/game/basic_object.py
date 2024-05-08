import pyglet

from game.core import WINDOW_WIDTH, WINDOW_HEIGHT


class BasicObject(pyglet.sprite.Sprite):
    def __init__(self, texture, *args, **kwargs):
        self._texture = texture
        # self.image = pyglet.image.create(kwargs[width], kwargs[height], pyglet.image.)
        super().__init__(texture, *args, **kwargs)
        # self.color = (255, 255, 255)
        # self.opacity = 255
        self.x = 0
        self.y = 0
        self.visible = False
        self.velocity_x = 0.0
        self.velocity_y = 0.0

    def set_xy(x, y):
        super().position = x, y
        super().visible = True
    
    def update(self, dt):
        # self.x += self.velocity_x * dt
        # self.y += self.velocity_y * dt
        self.check_bounds()
    
    def get_texture(self):
        return self._texture
    
    def check_bounds(self):
        min_x = 0
        max_x = WINDOW_WIDTH
        
        min_y = 0
        max_y = WINDOW_HEIGHT

        if self.x > max_x:
            self.x = max_x
            self.velocity_x *= -0.9
        elif self.x < min_x:
            self.x = min_x
            self.velocity_x *= -0.9

        if self.y > max_y:
            self.y = max_y
            self.velocity_y *= -0.9
        elif self.y < min_y:
            self.y = min_y
            self.velocity_y *= -0.9
