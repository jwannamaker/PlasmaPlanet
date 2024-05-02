from enum import Enum

import pyglet


pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

palette = pyglet.resource.file('palettes.json')
WIDTH = 5
BORDER = 10
RADIUS = 32
SIZE = round((RADIUS+BORDER)*2), round((RADIUS+BORDER)*2)
CENTER = RADIUS+BORDER, RADIUS+BORDER

def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


class PolygonSprite(Enum):
    TRIANGLE = {'n': 3, 'fill_color': 'tangerine', 'border_color': 'yellow'}
    SQUARE = {'n': 4, 'fill_color': 'pine', 'border_color': 'seafoam'}
    PENTAGON = {'n': 5, 'fill_color': 'muted-red', 'border_color': 'pastel-pink'}
    HEXAGON = {'n': 6, 'fill_color': 'dusk', 'border_color': 'lavender'}
    OCTAGON = {'n': 8, 'fill_color': 'tangerine', 'border_color': 'yellow'}


class ButtonSprite(Enum):
    SMALL_BUTTON = 20, 60
    MEDIUM_BUTTON = 30, 90
    BIG_BUTTON = 40, 120


class Asset(pyglet.sprite.Sprite):
    def __init__(self, filename, shape, position: tuple[float, float]):
        self.shape = shape
        self.x = position[0]
        self.y = position[1]
        self.velocity = [0.0, 0.0]

        # Anchor the image to the center and transparent the alphas.
        self.image = pyglet.image.load(filename)
        # self.image.anchor
        
    def change_colors(self, brightness: int):
        print(f'Change sprite palette to make it brightness {brightness}')
        print('Will probably use a greyscale base image and layover that at different times.')
