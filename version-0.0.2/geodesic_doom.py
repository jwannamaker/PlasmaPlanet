import math
import random
from enum import Enum
from pathlib import Path

import pyglet
from pyglet.gl import *

from game import *

# Initializing the path Pyglet will search first to find resources for the application.
pyglet.resource.path = ['resources', 'resources/images', 'resources/data']
pyglet.resource.reindex()
palette = pyglet.resource.file('palettes.json')
font = pyglet.resource.image('large-palace-font-white.png')
tilemap = pyglet.resource.file('tilemap.json')
pixel_artist = asset_manager.PixelArtist(palette, font, tilemap)

player_choice_image = pyglet.resource.image('sample spritesheet (132x132).png')  # take out images/
asset_manager.center_image(player_choice_image)

title_card = pyglet.resource.image('title-card-GEODESICDOOM-900x64.png')
# asset_manager.center_image(title_card)

# A simple class to keep track of the asset paths using Pyglet built-in resource management system.
class PlatonicSolidFiles(Enum):
    TETRA = pyglet.resource.file('data/tetrahedron.json')
    HEXA = pyglet.resource.file('data/cube.json')
    OCTA = pyglet.resource.file('data/octahedron.json')
    DODECA = pyglet.resource.file('data/dodecahedron.json')
    ICOSA = pyglet.resource.file('data/icosahedron.json')
    SNUB_DODECA = pyglet.resource.file('data/snub dodecahedron.json')
    PENTA_BIPYR = pyglet.resource.file('data/pentagonal bipyramid.json')


# Allows images to load with their alpha values blended? Seriously not a lot explained in the docs.
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

window = pyglet.window.Window()
main_batch = pyglet.graphics.Batch()
pixel_artist.fancy_write('GEODESIC DOOM', (0, window.height-32), main_batch)
main_group = pyglet.graphics.Group()

window.set_fullscreen()
clock = pyglet.clock.get_default()

# Creating the labels for the HUD.
label_maker = hud.LabelFactory(window.width, window.height)
hiscore = label_maker.create_updatable('HiScore', 0)
score = label_maker.create_updatable('Score', 0)
level = label_maker.create_updatable('Level', 0)
display_clock = label_maker.create_updatable('Time', 0)

# Placing each label at its screen position.
label_maker.set_xy(hiscore, 0, window.height - 36)
label_maker.set_xy(score, 0, window.height - 72)
label_maker.set_xy(level, 0, window.height - 108)
label_maker.set_xy(display_clock, 0, window.height - 144)


@window.event
def on_mouse_press(x, y, button, modifiers):
    """ Possible values:
        pyglet.window.mouse.LEFT
        pyglet.window.mouse.MIDDLE
        pyglet.window.mouse.RIGHT
    """
    label_maker.update('score', random.randint(0, 10))


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    print(f'scrolling mouse @{x},{y}')



@window.event
def on_draw():
    window.clear()

    main_batch.draw()
    title_card.blit(0, window.height-64)
    label_maker.update('time', clock.last_ts)
    hud.Hud.draw()

    player_choice_image.blit(window.width/2, window.height/2)


if __name__ == '__main__':
    pyglet.app.run()
    # pixel_artist.create_title_card('GEODESICDOOM', (900, 64))
    # print(list(pixel_artist.draw_platonic_solid(PlatonicSolidFiles.TETRA)))
    #
    # print(list(pixel_artist.draw_platonic_solid(PlatonicSolidFiles.HEXA)))
