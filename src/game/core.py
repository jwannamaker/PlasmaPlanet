""" 
This file is mainly organizational, so that all the concrete data can be loaded 
into the project at once and referenced throughout the project in a more
elegant, standardized manner.
"""
import json
from dataclasses import dataclass
from enum import Enum

import pyglet
from pyglet.gl import *

from game.hud import LabelFactory
from game.asset_manager import PixelArtist

# Allows images to load with their alpha values blended? 
# I definitely need to learn how OpenGL works. (Eventually)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

window = pyglet.window.Window()
main_batch = pyglet.graphics.Batch()
text_batch = pyglet.graphics.Batch()
background = pyglet.graphics.Group(order=1)
foreground = pyglet.graphics.Group(order=2)

window.set_fullscreen()
clock = pyglet.clock.get_default()

WINDOW_WIDTH = window.width   # on my laptop == 1792
WINDOW_HEIGHT = window.height   # on my laptop == 1120

@window.event
def on_draw():
    window.clear()
    main_batch.draw()
    text_batch.draw()


# Basic utility functions.
def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image


def build_asset_from_json(filename):
    # TODO: Needs to be more fleshed out in order to actually be useful?
    with open(filename) as f:
        return json.load(f)


@dataclass(init=True, kw_only=True)
class SpriteSpecs:
    width: int = 32
    height: int = 32
    radius: int = 32
    border: int = 1
    
    def get_size(self) -> tuple[int, int]:
        return round((self.RADIUS + SpriteSpecs.BORDER) * 2), round((self.RADIUS + SpriteSpecs.BORDER) * 2)
    
    def get_center(self) -> tuple[int, int]:
        return self.RADIUS + SpriteSpecs.BORDER, self.RADIUS + SpriteSpecs.BORDER


class PlatonicSolidSpecifications(Enum):
    TETRA = pyglet.resource.file('tetrahedron.json')
    HEXA = pyglet.resource.file('cube.json')
    OCTA = pyglet.resource.file('octahedron.json')
    DODECA = pyglet.resource.file('dodecahedron.json')
    ICOSA = pyglet.resource.file('icosahedron.json')
    SNUB_DODECA = pyglet.resource.file('snub dodecahedron.json')
    PENTA_BIPYR = pyglet.resource.file('pentagonal bipyramid.json')


class PolygonSpriteSpecs(Enum):
    TRIANGLE = {'n': 3, 'fill_color': 'tangerine', 'border_color': 'yellow'}
    SQUARE = {'n': 4, 'fill_color': 'pine', 'border_color': 'seafoam'}
    PENTAGON = {'n': 5, 'fill_color': 'muted-red', 'border_color': 'pastel-pink'}
    HEXAGON = {'n': 6, 'fill_color': 'dusk', 'border_color': 'lavender'}
    OCTAGON = {'n': 8, 'fill_color': 'tangerine', 'border_color': 'yellow'}
    

# Initializing the path Pyglet will search first to find resources for the application.
pyglet.resource.path = ['../resources', '../resources/images', '../resources/data']
pyglet.resource.reindex()

palette = pyglet.resource.file('palette.json') 
font = pyglet.resource.image('large-palace-font-white.png')
tilemap = pyglet.resource.file('tilemap.json')

TILE_SIZE = 32, 16  # Unit tile size. Corresponds to the top of the cubes.
WORLD_SIZE = 5, 5  # In tiles.

# Creating a new PixelArtist instance for the project.
artist = PixelArtist(palette_file=palette, font_file=font, tilemap_file=tilemap)


# All the images!
player_choice_image = pyglet.resource.image('sample spritesheet (132x132).png')
title_card = pyglet.resource.image('title-card-GEODESICDOOM-900x64.png')
blank_image = pyglet.resource.image('blank-128x128.png')


# Creating the labels for the HUD and positioning them on the screen
# TODO: The label factory should already know what size the font is being rendered at,
# and simply adjust the height when adding a new line.
# Basically --> I shouldn't have to pass in concrete data for these calls
label_manager = LabelFactory(WINDOW_WIDTH, WINDOW_HEIGHT, text_batch)
hiscore = label_manager.create_updatable('HiScore', 0)
label_manager.set_xy(hiscore, 0, WINDOW_HEIGHT - 36 - 128)

score = label_manager.create_updatable('Score', 0)
label_manager.set_xy(score, 0, WINDOW_HEIGHT - 2*(36) - 128)

level = label_manager.create_updatable('Level', 0)
label_manager.set_xy(level, 0, WINDOW_HEIGHT - 3*(36) - 128)

display_clock = label_manager.create_updatable('Time', 0)
label_manager.set_xy(display_clock, 0, WINDOW_HEIGHT- 4*(36) - 128)