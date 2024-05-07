import imghdr
import sys
import json
import string
import itertools
from pathlib import Path
from enum import Enum

import json
import PIL
from PIL import Image, ImageDraw, ImageFont
import pyglet
import numpy as np

from game import TILE_SIZE, WINDOW_HEIGHT, WORLD_SIZE, SPRITE_WIDTH, SPRITE_RADIUS, SPRITESHEET_BORDER, SIZE, CENTER
from game import basic_object

def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

def build_asset_from_json(filename):
    with open(filename) as f:
        return json.load(f)


class PolygonSprite(Enum):
    TRIANGLE = {'n': 3, 'fill_color': 'tangerine', 'border_color': 'yellow'}
    SQUARE = {'n': 4, 'fill_color': 'pine', 'border_color': 'seafoam'}
    PENTAGON = {'n': 5, 'fill_color': 'muted-red', 'border_color': 'pastel-pink'}
    HEXAGON = {'n': 6, 'fill_color': 'dusk', 'border_color': 'lavender'}
    OCTAGON = {'n': 8, 'fill_color': 'tangerine', 'border_color': 'yellow'}


class PixelArtist:
    """ Generates all assets that I may need for a particular video game.
    I'm aware that I can optimize a lot of things within this class, such as
    image caching, and presorting the palettes by value/tone.

    curr_dir: The current working directory for the clientside.
    palette_dir: The directory with the palette file (a .json).
    output_dir: The directory where to output the images to (.png format).
    """
    def __init__(self, palette_file, font_file, text_batch, subgroup, tilemap_file):
        self.palette = self.load_palette(palette_file)
        self.text_batch = text_batch
        self.group = subgroup
        self.font = self.load_font(font_file, self.text_batch, self.group)
        self.tilemap = self.load_tilemap(tilemap_file)

    def load_palette(self, palette_file) -> dict:
        self.palette = json.load(palette_file)
        return self.palette

    def load_font(self, font_file, batch, subgroup) -> dict:
        # characters = list(itertools.chain(string.ascii_uppercase, string.digits))
        # characters = list(itertools.batched(characters, 6))
        # ordered_characters =
        # for c in characters: #FUCK THIS. JUST hardcoding it for now.
        ordered_characters = ['5', '6', '7', '8', '9', '0',
                              'Y', 'Z', '1', '2', '3', '4',
                              'S', 'T', 'U', 'V', 'W', 'X',
                              'M', 'N', 'O', 'P', 'Q', 'R',
                              'G', 'H', 'I', 'J', 'K', 'L',
                              'A', 'B', 'C', 'D', 'E', 'F', ' ']
        character_texture_regions = pyglet.image.ImageGrid(image=font_file, rows=6, columns=6)
        character_sprites = [basic_object.BasicObject(c, batch=batch, group=subgroup) for c in character_texture_regions]
        
        self.font = {k: v for k, v in zip(ordered_characters, character_sprites)}
        self.font[' '] = basic_object.BasicObject(pyglet.resource.image('blank-128x128.png'), batch=batch, group=subgroup) 
        # print(self.font)
        # check HERE if font is populated with the right stuff
        return self.font

    def render_font(self, text, x=0, y=WINDOW_HEIGHT-128):
        text_sprites = []
        for ch in text:
            print(f'rendering {ch} @ {x}, {y}')
            text_sprites.append(pyglet.sprite.Sprite(img=self.font[ch], x=x, y=y, batch=self.text_batch, group=self.group))
            x += 128
            

    
    def load_tilemap(self, tilemap_file):
        self.tilemap = json.load(tilemap_file)
        return self.tilemap

    def get_color_code(self, palette_name, color) -> tuple[int, int, int]:
        for palette_color in list(self.palette[palette_name].keys()):
            if color in palette_color:
                return (self.palette[palette_name][palette_color][0],
                        self.palette[palette_name][palette_color][1],
                        self.palette[palette_name][palette_color][2])

    def create_solid_color_box(self, color, border_color) -> Image:
        out = Image.new('RGB', SIZE)
        drawing_context = ImageDraw.Draw(out)
        # drawing_context.rounded_rectangle(((0, 0), SIZE), radius=10,
        #                                   fill=color, outline=border_color,
        #                                   width=10)
        drawing_context.rectangle((0, 0), fill=color, outline=border_color, width=SPRITESHEET_BORDER)

        return out

    def get_swatch_color_grid(self, palette_name):
        color_list = list(self.palette[palette_name].items())
        color_combos = list(itertools.permutations(color_list, 2))

        color_grid = dict.fromkeys(list(self.palette[palette_name].keys()))
        # print(color_grid)
        # print(len(color_grid.keys()))
        for key in list(color_grid.keys()):
            row = []
            for background, foreground in color_combos:
                if background[0] == key:
                    row.append([background[0], foreground[0]])
            # print(row)
            # print(len(row))
            # print()
            color_grid[key] = row
        return color_grid

    def create_color_swatch(self, palette_name):

        color_grid = self.get_swatch_color_grid(palette_name)
        swatch_size = SIZE[0] * (len(color_grid) - 1), SIZE[1] * len(color_grid)
        swatch = Image.new('RGB', swatch_size)
        drawing_context = ImageDraw.Draw(swatch)

        i, j = 0, 0
        for row in color_grid:
            # print()
            # print(row)
            i = 0
            for box in color_grid[row]:
                topleft = i * SIZE[0], j * SIZE[1]
                bottomright = topleft[0] + SIZE[0], topleft[1] + SIZE[1]
                drawing_context.rectangle((topleft, bottomright),
                                          fill=self.get_color_code(palette_name, box[1]),
                                          outline=self.get_color_code(palette_name, box[0]),
                                          width=SPRITESHEET_BORDER * 2)
                i += 1
            j += 1

        swatch_path = f'resources/{palette_name}-swatch-{SIZE[0]}x{SIZE[1]}.png'
        swatch.save(swatch_path, 'PNG')
        return swatch_path

    def create_title_card(self, title, card_size):
        out = Image.new('RGBA', card_size)
        drawing_context = ImageDraw.Draw(out)
        drawing_context.rounded_rectangle(((0, 0), card_size), radius=10,
                                          fill=self.get_color_code('cryptic-ocean6', 'seafoam'))
        drawing_context.rounded_rectangle(((8, 8), (card_size[0]-8, card_size[1]-8)), radius=10,
                                          fill=self.get_color_code('cryptic-ocean6', 'light-blue'))
        image_path = f'resources/images/title-card-{title}-{card_size[0]}x{card_size[1]}.png'
        out.save(image_path, 'PNG')
        return f'title-card-{title}-{card_size[0]}x{card_size[1]}.png'

    def create_sprite(self, shape: PolygonSprite, rotation: float) -> Image:
        out = Image.new('RGBA', SIZE)
        drawing_context = ImageDraw.Draw(out)
        drawing_context.regular_polygon((CENTER, SPRITE_RADIUS), shape.value['n'], rotation,
                                        fill=self.get_color_code('plasma8', shape.value['fill_color']),
                                        outline=self.get_color_code('plasma8', shape.value['border_color']),
                                        width=1)
        drawing_context.regular_polygon((CENTER, SPRITE_RADIUS - SPRITE_WIDTH), shape.value['n'], rotation,
                                        fill=(0, 0, 0, 0),
                                        outline=self.get_color_code('plasma8', shape.value['border_color']))
        return out

    def create_sprite_sheet(self, shape: PolygonSprite, steps: int) -> str:
        exterior_angle = 360.0 / shape.value['n']
        start_angle = (180.0 - exterior_angle) / 2.0
        current_angle = start_angle
        increment = 360.0 / steps
        stop_angle = start_angle + 360.0

        # Creating an image large enough to contain every sprite, including a margin.
        sprite_sheet_size = SIZE[0]*steps, SIZE[1]
        sprite_sheet = Image.new('RGB', sprite_sheet_size)
        i = 0
        j = 0
        # Create each sprite image and paste it onto the sprite sheet.
        while current_angle != stop_angle:
            sprite = self.create_sprite(shape, current_angle)
            sprite_sheet.paste(sprite, (i*SIZE[0], j*SIZE[1]))
            current_angle += increment
            # if i + 1 == 10:
            #     i = 0
            #     j += 1
            # else:
            #     i += 1
            i += 1

        image_path = f"{shape.value['fill_color']}-{shape.name.lower()}-spritesheet-{SIZE[0]}x{SIZE[1]}.png"
        sprite_sheet.save(image_path, 'PNG')
        return image_path

    def create_sample_sheet(self, shapes: list[PolygonSprite]):
        """ Note that a complete version of this function would include a swatch,
        the color codes and names on the sheet.
        """
        sample_sheet_size = SIZE[0]*len(shapes), SIZE[1]
        sample_sheet = Image.new('RGBA', sample_sheet_size, self.get_color_code('plasma8', 'black'))

        for i, shape in enumerate(shapes):
            sprite = self.create_sprite(shape, 0)
            sample_sheet.paste(sprite, (i*SIZE[0], 0))

        sample_sheet.save(('sample spritesheet (' + str(SIZE[0]) + 'x' + str(SIZE[1]) + ').png'), 'PNG')

    def create_platonic_solid_sprite(self, platonic_file):
        """ WILL EVENTUALLY:
        Take the points listed in the file,
        convert the 3d coordinates to an isometric projection.
        Draws that wireframe on an image,
        saves and returns it.
        """
        geometry_info = json.load(platonic_file.value)
        print(f'retrieved info: {geometry_info}')
        # transformation matrix
        # | a(x)î   c(y)ˆj |      | 1(x)(width/2)   0.5(y)(height/2) |
        # | b(x)î   d(y)ˆj |      | -1(x)(width/2)  0.5(y)(height/2) |
        a = 0.5*SIZE[0]  # i hat x component
        b = 0.25*SIZE[1]  # i hat y component
        c = -0.5*SIZE[0]  # j hat x component
        d = 0.25*SIZE[1]  # j hat y component
        isometric_projection = []
        for point in geometry_info['vertices']:
            x = point[0]
            y = point[1]
            z = point[2]  # I need to figure out how to make the height

            transformed = np.array([x*a + x*b, y*c + y*d])
            print(f'original: (\t{x}, \t{y}, \t{z})')
            print(f'transform: (\t{transformed[0]}, \t{transformed[1]})')
            yield transformed

    def create_tilemap(self):
        print(self.tilemap)
