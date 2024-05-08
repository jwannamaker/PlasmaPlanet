import math
import random

import pyglet
from pyglet.window import key, mouse

from game import core, asset_manager, hud

# Moved to game.core 
# --> May need to be moved back HERE... we'll see.
# Initializing the path Pyglet will search first to find resources for the application.
# pyglet.resource.path = ['resources', 'resources/images', 'resources/data']
# pyglet.resource.reindex()




@core.window.event
def on_key_press(symbol, modifiers):
    if symbol == key.P:
        pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')

@core.window.event
def on_mouse_press(x, y, button, modifiers):
    """ Possible values:
        pyglet.window.mouse.LEFT
        pyglet.window.mouse.MIDDLE
        pyglet.window.mouse.RIGHT
    """
    if button == mouse.LEFT:
        core.label_manager.update('score', random.randint(0, 10))
    if button == mouse.RIGHT:
        print('nah man. do not right click on this shit rn. stop it.')


@core.window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    print(f'i see that scrolling mouse @{x},{y}. you better stop.')

core.clock.schedule_interval(func=core.label_manager.update, interval=1.0, 
                        label_name='time')

core.artist.render_font('GEODESIC DOOM')
core.title_card.blit(0, core.window.height-128)
core.player_choice_image.blit(core.WINDOW_WIDTH/2, core.WINDOW_HEIGHT/2)


if __name__ == '__main__':
    pyglet.app.run()
    # pixel_artist.create_title_card('GEODESICDOOM', (900, 64))
    # print(list(pixel_artist.draw_platonic_solid(PlatonicSolidFiles.TETRA)))
    #
    # print(list(pixel_artist.draw_platonic_solid(PlatonicSolidFiles.HEXA)))
