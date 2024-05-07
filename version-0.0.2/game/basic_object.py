import pyglet

from . import WINDOW_WIDTH, WINDOW_HEIGHT

class BasicObject(pyglet.sprite.Sprite):
    def __init__(self, texture, *args, **kwargs):
        self.texture = texture
        super().__init__(self.texture, *args, **kwargs)
        self.color = (255, 255, 255)
        self.opacity = 255
        self.x = 0
        self.y = 0
        self.velocity_x = 0.0
        self.velocity_y = 0.0

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()

    def _draw(self, x, y):
        """ This is where I'll insert any additional things I'll want to do to the 
        sprite before actually rendering it. 
        
        Such as: 
        checking a state variable to see if the image needs to be converted to
            + greyscale or 
            + other color treatment options
        """
        self.x = x
        self.y = y
        self.draw()
    
    def get_texture(self):
        return self.texture
    
    def check_bounds(self):
        min_x = -self.image.width / 2
        max_x = WINDOW_WIDTH + self.image.width / 2

        min_y = -self.image.height / 2
        max_y = WINDOW_HEIGHT + self.image.height / 2

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
