import sys
import math
import random

import pyglet
from pyglet import gl
from pyglet.window import key, mouse

from game.util import window, main_batch, text_batch, background, foreground

# Allows images to load with their alpha values blended? 
# I definitely need to learn how OpenGL works. (Eventually)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)


@window.event
def on_draw():
    window.clear()
    main_batch.draw()
    text_batch.draw()


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
        label_manager.update('score', random.randint(0, 10))
    if button == mouse.RIGHT:
        print('nah man. do not right click on this shit rn. stop it.')


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    print(f'i see that scrolling mouse @{x},{y}. you better stop.')

clock.schedule_interval(func=label_manager.update, interval=1.0, 
                        label_name='time')

artist.render_font('GEODESIC DOOM')
title_card.blit(0, window.height-128)
player_choice_image.blit(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)


if __name__ == '__main__':
    print(sys.modules)
    pyglet.app.run()
    # pixel_artist.create_title_card('GEODESICDOOM', (900, 64))
    # print(list(pixel_artist.draw_platonic_solid(PlatonicSolidFiles.TETRA)))
    #
    # print(list(pixel_artist.draw_platonic_solid(PlatonicSolidFiles.HEXA)))
