import math
import pathlib

import pyglet
from pyglet.window import key

from pyglet.gl import *

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


pyglet.resource.path = [pyglet.resource.get_script_home(), '../resources']
pyglet.resource.reindex()

window = pyglet.window.Window()
window.set_fullscreen()
keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)
clock = pyglet.clock.get_default()


HUD = pyglet.graphics.Batch()
background = pyglet.graphics.Group(order=0)
info_box = pyglet.shapes.BorderedRectangle(x=0, y=0, width=window.width, height=window.height//8,
                                           color=(35, 35, 35, 100), border_color=(100, 100, 100),
                                           border=10,
                                           batch=HUD, group=background)


def set_label_font(label):
    label.font_name = 'Menlo'
    label.font_size = 16


foreground = pyglet.graphics.Group(order=1)

score = pyglet.graphics.Batch()
score_label = pyglet.text.Label('Score',
                                x=0, y=window.height,
                                anchor_x='left', anchor_y='top',
                                batch=score, group=foreground)
set_label_font(score_label)
score_value_label = pyglet.text.Label('0',
                                      x=window.width, y=window.height,
                                      anchor_x='right', anchor_y='top',
                                      batch=score, group=foreground)
set_label_font(score_value_label)


level = pyglet.graphics.Batch()
level_label = pyglet.text.Label('Level',
                                x=0, y=window.height-16,
                                anchor_x='left', anchor_y='top',
                                batch=level, group=foreground)
set_label_font(level_label)
level_value_label = pyglet.text.Label('0',
                                      x=window.width, y=window.height-16,
                                      anchor_x='right', anchor_y='top',
                                      batch=level, group=foreground)
set_label_font(level_value_label)




def get_apothem(n, radius):
    """ Return the apothem for a polygon of given n (sides) and radius. """
    return radius * math.cos(math.pi / n)


shapes = pyglet.graphics.Batch()
# plasma_ball_image = pyglet.image.load('plasmaball.png')
# plasma_ball_image.anchor_x = 16
# plasma_ball_image.anchor_y = 16
# plasma_ball_image.scale = 3
# plasma_ball = pyglet.sprite.Sprite(plasma_ball_image, x=window.width//2, y=window.height//2, batch=shapes)
pentagon = pyglet.shapes.Star(x=300, y=300,
                              num_spikes=5, outer_radius=200, inner_radius=get_apothem(5, 200),
                              color=(230, 100, 100, 175),
                              batch=shapes, group=foreground)
hexagon = pyglet.shapes.Star(x=600, y=600,
                             num_spikes=6, outer_radius=200, inner_radius=get_apothem(6, 200),
                             color=(100, 100, 250, 175),
                             batch=shapes, group=foreground)
trigon = pyglet.shapes.Star(x=300, y=600,
                            num_spikes=3, outer_radius=200, inner_radius=get_apothem(3, 200),
                            color=(100, 35, 100, 175),
                            batch=shapes, group=foreground)


def rotate_shape(dt, shape, direction):
    theta = math.pi / shape.num_spikes
    shape.rotation += direction * theta * 0.01


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.Q:
        clock.schedule(func=rotate_shape, shape=pentagon, direction=-1)
    elif symbol == key.E:
        clock.schedule(func=rotate_shape, shape=pentagon, direction=1)

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.Q:
        clock.unschedule(rotate_shape)
    elif symbol == key.E:
        clock.unschedule(rotate_shape)

@window.event
def on_draw():
    window.clear()
    HUD.draw()
    score.draw()
    level.draw()
    shapes.draw()


if __name__ == '__main__':
    pyglet.app.run()
