import math
from pathlib import Path

import pyglet
from pyglet.gl import *

import hud
import asset_manager


glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

pyglet.resource.path = ['../resources']
palette = pyglet.resource.file('palettes.json')
pyglet.resource.reindex()

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
class BasicObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        
    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()
        
    def check_bounds(self):
        min_x = -self.image.width / 2
        max_x = window.width + self.image.width / 2
        
        min_y = -self.image.height / 2
        max_y = window.height + self.image.height / 2
        
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

#-------------------------------------------------------------------------------
player_choice_image = pyglet.resource.image('sample spritesheet (132x132).png')

pixel_artist = asset_manager.PixelArtGenerator(palette)
hexagon_image_path = pixel_artist.create_sprite_sheet(asset_manager.PolygonSprite.HEXAGON, 1)
swatch_image_path = pixel_artist.create_color_swatch('plasma8')

hexagon_image = pyglet.image.load(hexagon_image_path)
color_swatch_image = pyglet.image.load(swatch_image_path)

asset_manager.center_image(player_choice_image)
asset_manager.center_image(hexagon_image)
asset_manager.center_image(color_swatch_image)

@window.event
def on_draw():
    hud.Hud.draw()
    player_choice_image.blit(window.width / 2, window.height / 2)
    hexagon_image.blit(window.width / 2, window.height - 200)
    color_swatch_image.blit(window.width / 2, window.height - 1000)
        
if __name__ == '__main__':
    pyglet.app.run()