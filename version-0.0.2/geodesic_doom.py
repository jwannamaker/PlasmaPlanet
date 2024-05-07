import math
import random
from enum import Enum
from pathlib import Path

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

from game import *

# Allows images to load with their alpha values blended? 
# I definitely need to learn how OpenGL works. (Eventually)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

window = pyglet.window.Window()
main_batch = pyglet.graphics.Batch()
text_batch = pyglet.graphics.Batch()
main_group = pyglet.graphics.Group()

window.set_fullscreen()
clock = pyglet.clock.get_default()

# Initializing the path Pyglet will search first to find resources for the application.
pyglet.resource.path = ['resources', 'resources/images', 'resources/data']
pyglet.resource.reindex()

# A simple class to keep track of the asset paths using Pyglet built-in resource management system.
class PlatonicSolidFiles(Enum):
    TETRA = pyglet.resource.file('tetrahedron.json')
    HEXA = pyglet.resource.file('cube.json')
    OCTA = pyglet.resource.file('octahedron.json')
    DODECA = pyglet.resource.file('dodecahedron.json')
    ICOSA = pyglet.resource.file('icosahedron.json')
    SNUB_DODECA = pyglet.resource.file('snub dodecahedron.json')
    PENTA_BIPYR = pyglet.resource.file('pentagonal bipyramid.json')

# Create a PixelArtist instance
palette = pyglet.resource.file('palettes.json')
font = pyglet.resource.image('large-palace-font-white.png')
tilemap = pyglet.resource.file('tilemap.json')
pixel_artist = asset_manager.PixelArtist(palette, font, text_batch, main_group, tilemap)

player_choice_image = pyglet.resource.image('sample spritesheet (132x132).png')  # take out images/
asset_manager.center_image(player_choice_image)

title_card = pyglet.resource.image('title-card-GEODESICDOOM-900x64.png')


# Creating the labels for the HUD and positioning them on the screen
label_maker = hud.LabelFactory(window.width, window.height, text_batch, main_group)
hiscore = label_maker.create_updatable('HiScore', 0)
label_maker.set_xy(hiscore, 0, window.height - 36 - 128)

score = label_maker.create_updatable('Score', 0)
label_maker.set_xy(score, 0, window.height - 2*(36) - 128)

level = label_maker.create_updatable('Level', 0)
label_maker.set_xy(level, 0, window.height - 3*(36) - 128)

display_clock = label_maker.create_updatable('Time', 0)
label_maker.set_xy(display_clock, 0, window.height - 4*(36) - 128)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.P:
        pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')

@window.event
def on_mouse_press(x, y, button, modifiers):
    """ Possible values:
        pyglet.window.mouse.LEFT
        pyglet.window.mouse.MIDDLE
        pyglet.window.mouse.RIGHT
    """
    if button == mouse.LEFT:
        label_maker.update('score', random.randint(0, 10))
    if button == mouse.RIGHT:
        print('nah man. do not right click on this shit rn. stop it.')


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    print(f'i see that scrolling mouse @{x},{y}. you better stop.')

clock.schedule_interval(func=label_maker.update, interval=1.0, 
                        label_name='time')

pixel_artist.render_font('GEODESIC DOOM')


@window.event
def on_draw():
    window.clear()
    event = window.dispatch_events()
    
    title_card.blit(0, window.height-128)
    text_batch.draw()
    main_batch.draw()
    
    player_choice_image.blit(window.width/2, window.height/2)


if __name__ == '__main__':
    pyglet.app.run()
    # pixel_artist.create_title_card('GEODESICDOOM', (900, 64))
    # print(list(pixel_artist.draw_platonic_solid(PlatonicSolidFiles.TETRA)))
    #
    # print(list(pixel_artist.draw_platonic_solid(PlatonicSolidFiles.HEXA)))
