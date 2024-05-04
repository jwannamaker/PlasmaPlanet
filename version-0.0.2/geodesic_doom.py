import math
from enum import Enum
from pathlib import Path

import glooey
import pyglet
from pyglet.gl import *

from game import hud, asset_manager


pyglet.resource.path = ['resources']
pyglet.resource.reindex()
palette = pyglet.resource.file('data/palettes.json')


class PlatonicSolid(Enum):
    TETRA = pyglet.resource.file('data/tetrahedron.json')
    HEXA = pyglet.resource.file('data/cube.json')
    OCTA = pyglet.resource.file('data/octahedron.json')
    DODECA = pyglet.resource.file('data/dodecahedron.json')
    ICOSA = pyglet.resource.file('data/icosahedron.json')


glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

window = pyglet.window.Window()
window.set_fullscreen()
clock = pyglet.clock.get_default()

label_maker = hud.LabelFactory(window.width, window.height)
title = label_maker.create_title(' G E O D E S I C  DOOM ')
hiscore = label_maker.create_updatable('HiScore', 0)
score = label_maker.create_updatable('Score', 0)
level = label_maker.create_updatable('Level', 0)

label_maker.set_xy(title, 0, window.height)
label_maker.set_xy(hiscore, 0, window.height - 36)
label_maker.set_xy(score, 0, window.height - 72)
label_maker.set_xy(level, 0, window.height - 108)

pixel_artist = asset_manager.PixelArtist(palette)

player_choice_image = pyglet.resource.image('images/sample spritesheet (132x132).png')
asset_manager.center_image(player_choice_image)


@window.event
def on_draw():
    window.clear()
    hud.Hud.draw()
    player_choice_image.blit(window.width / 2, window.height / 2)


if __name__ == '__main__':
    pyglet.app.run()
