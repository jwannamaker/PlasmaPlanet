import sys
import json
import itertools
from pathlib import Path

import pyglet
from PIL import Image, ImageDraw

from game import assets


class PixelArtist:
    """ Generates all of the assets that I may need for a particular video game. 
    I'm aware that I can optimize a lot of things within this class, such as 
    image caching, and presorting the palettes by value/tone.
    
    curr_dir: The current working directory for the clientside.
    palette_dir: The directory with the palette file (a .json).
    output_dir: The directory where to output the images to (.png format).
    """
    def __init__(self, palette):
        self.palette = {}
        self.load_palette(palette)
    
    def load_palette(self, palette) -> dict:
        # with open(Path.joinpath(self.curr_dir, file)) as f:
            # return json.load(f)
        self.palette = json.load(palette)
        

    def get_color_code(self, palette_name, color) -> tuple[int, int, int]:
        for palette_color in list(self.palette[palette_name].keys()):
            if color in palette_color:
                return (self.palette[palette_name][palette_color][0], 
                        self.palette[palette_name][palette_color][1], 
                        self.palette[palette_name][palette_color][2])

    def get_all_combinations(self, palette) -> list[int]:
        
        print('Get all valid combinations of 2 background and foreground colors.')

    def create_solid_color_box(self, color, border_color) -> Image:
        out = Image.new('RGB', assets.SIZE)
        drawing_context = ImageDraw.Draw(out)
        # drawing_context.rounded_rectangle(((0, 0), SIZE), radius=10, 
        #                                   fill=color, outline=border_color,
        #                                   width=10)
        drawing_context.rectangle((0, 0), fill=color, outline=border_color, width=assets.BORDER)
        
        return out
    
    def get_swatch_color_grid(self, palette_name):
        color_list = list(self.palette[palette_name].items())
        color_combos = list(itertools.permutations(color_list, 2))
        
        color_grid = dict.fromkeys(list(self.palette[palette_name].keys()))
        print(color_grid)
        print(len(color_grid.keys()))
        for key in list(color_grid.keys()):
            row = []
            for background, foreground in color_combos:
                if background[0] == key:
                    row.append([background[0], foreground[0]])
            print(row)
            print(len(row))
            print()
            color_grid[key] = row
        return color_grid
    
    def create_color_swatch(self, palette_name):
        
        color_grid = self.get_swatch_color_grid(palette_name)
        swatch_size = assets.SIZE[0] * (len(color_grid) - 1), assets.SIZE[1] * len(color_grid)
        swatch = Image.new('RGB', swatch_size)
        drawing_context = ImageDraw.Draw(swatch)
        
        i, j = 0, 0
        for row in color_grid:
            print()
            print(row)
            
            i = 0
            for box in color_grid[row]:
                topleft = i * assets.SIZE[0], j * assets.SIZE[1]
                bottomright = topleft[0] + assets.SIZE[0], topleft[1] + assets.SIZE[1]
                drawing_context.rectangle((topleft, bottomright), 
                                        fill=self.get_color_code(palette_name, box[1]), 
                                        outline=self.get_color_code(palette_name, box[0]), 
                                        width=assets.BORDER * 2)
                i += 1
            j += 1
                
        swatch_path = f'resources/{palette_name}-swatch-{assets.SIZE[0]}x{assets.SIZE[1]}.png'
        swatch.save(swatch_path, 'PNG')
        return swatch_path
        

    def create_sprite(self, shape: assets.PolygonSprite, rotation: float) -> Image:
        out = Image.new('RGBA', assets.SIZE)
        drawing_context = ImageDraw.Draw(out)
        drawing_context.regular_polygon((assets.CENTER, assets.RADIUS), shape.value['n'], rotation, 
                                        fill=self.get_color_code('plasma8', shape.value['fill_color']),
                                        outline=self.get_color_code('plasma8', shape.value['border_color']), 
                                        width=1)
        drawing_context.regular_polygon((assets.CENTER, assets.RADIUS-assets.WIDTH), shape.value['n'], rotation,
                                        fill=(0, 0, 0, 0),
                                        outline=self.get_color_code('plasma8', shape.value['border_color']))
        return out

    def create_sprite_sheet(self, shape: assets.PolygonSprite, steps: int) -> str:
        exterior_angle = 360.0 / shape.value['n']
        start_angle = (180.0 - exterior_angle) / 2.0
        current_angle = start_angle
        increment = 360.0 / steps
        stop_angle = start_angle + 360.0
        
        # Creating an image large enough to contain every sprite, including a margin.
        sprite_sheet_size = assets.SIZE[0]*steps, assets.SIZE[1]
        sprite_sheet = Image.new('RGB', sprite_sheet_size)
        i = 0
        j = 0
        # Create each sprite image and paste it onto the sprite sheet.
        while current_angle != stop_angle:
            sprite = self.create_sprite(shape, current_angle)
            sprite_sheet.paste(sprite, (i*assets.SIZE[0], j*assets.SIZE[1]))
            current_angle += increment
            # if i + 1 == 10:
            #     i = 0
            #     j += 1
            # else:
            #     i += 1
            i += 1
            
        image_path = f"{shape.value['fill_color']}-{shape.name.lower()}-spritesheet-{assets.SIZE[0]}x{assets.SIZE[1]}.png"
        sprite_sheet.save(image_path, 'PNG')
        return image_path

    def create_sample_sheet(self, shapes: list[assets.PolygonSprite]):
        """ Note that a complete version of this function would include a swatch, the color codes and names on the sheet. """
        sample_sheet_size = assets.SIZE[0]*len(shapes), assets.SIZE[1]
        sample_sheet = Image.new('RGBA', sample_sheet_size, self.get_color_code('plasma8', 'black'))
        
        for i, shape in enumerate(shapes):
            sprite = self.create_sprite(shape, 0)
            sample_sheet.paste(sprite, (i*assets.SIZE[0], 0))
        
        sample_sheet.save(('sample spritesheet (' + str(assets.SIZE[0]) + 'x' + str(assets.SIZE[1]) + ').png'), 'PNG')