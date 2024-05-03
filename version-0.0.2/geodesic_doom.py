import math
from pathlib import Path

import pyglet
from pyglet.gl import *

from game import hud, asset_manager, assets


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

#-------------------------------------------------------------------------------
pixel_artist = asset_manager.PixelArtist(assets.palette)
hexagon_image_path = pixel_artist.create_sprite_sheet(assets.PolygonSprite.HEXAGON, 1)
swatch_image_path = pixel_artist.create_color_swatch('tangerine4')


player_choice_image = pyglet.resource.image('sample spritesheet (132x132).png')
hexagon_image = pyglet.image.load(hexagon_image_path)

assets.center_image(player_choice_image)
assets.center_image(hexagon_image)
#-------------------------------------------------------------------------------
@window.event
def on_draw():
    window.clear()
    hud.Hud.draw()
    player_choice_image.blit(window.width / 2, window.height / 2)
    hexagon_image.blit(window.width / 2, window.height - 200)
    # color_swatch_image.blit(window.width / 2, window.height - 1000)
        
if __name__ == '__main__':
    pyglet.app.run()