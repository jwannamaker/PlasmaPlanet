import string

import pyglet
from pyglet.sprite import Sprite
from pyglet.image import TextureGrid, ImageGrid

from . import resources


def font():
    parse_chars = [*string.ascii_uppercase, *string.digits, ' ']
    font_textures = TextureGrid(ImageGrid(resources.font, 6, 6))
    
    # Not adding these into a batch or group YET
    font_sprites = [Sprite(char_tex) for char_tex in font_textures]
    font_sprites.append(resources.blank_image.get_texture())
    
    return {k: v for k, v in zip(parse_chars, font_sprites)}