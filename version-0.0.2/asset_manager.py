import sys
import json
import itertools
from enum import Enum
from pathlib import Path

import pyglet
from PIL import Image, ImageDraw

# CURR_DIR = Path.joinpath(Path.cwd(), 'version-0.0.2')

# pyglet.resource.path = ['../resources']
# pyglet.resource.reindex()

def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

# ball_image = pyglet.resource.image('plasmaball.png')
# sample_image = pyglet.resource.image('sample-spritesheet-(132x132).png')
# pyglet.resource.reindex()

# center_image(ball_image)
# center_image(sample_image)

WIDTH = 5
BORDER = 10
RADIUS = 32
SIZE = round((RADIUS+BORDER)*2), round((RADIUS+BORDER)*2)
CENTER = RADIUS+BORDER, RADIUS+BORDER

class PolygonSprite(Enum):
    TRIANGLE = {'n': 3, 'fill_color': 'tangerine', 'border_color': 'yellow'}
    SQUARE = {'n': 4, 'fill_color': 'pine', 'border_color': 'seafoam'}
    PENTAGON = {'n': 5, 'fill_color': 'muted-red', 'border_color': 'pastel-pink'}
    HEXAGON = {'n': 6, 'fill_color': 'dusk', 'border_color': 'lavender'}
    OCTAGON = {'n': 8, 'fill_color': 'tangerine', 'border_color': 'yellow'}

class ButtonSprite(Enum):
    SMALL_BUTTON = 20, 60
    MEDIUM_BUTTON = 30, 90
    BIG_BUTTON = 40, 120

class Asset(pyglet.sprite.Sprite):
    def __init__(self, filename, shape, position: tuple[float, float]):
        self.shape = shape
        self.x = position[0]
        self.y = position[1]
        self.velocity = [0.0, 0.0]

        # Anchor the image to the center and transparent the alphas.
        self.image = pyglet.image.load(filename)
        # self.image.anchor
        
    def change_colors(self, brightness: int):
        print(f'Change sprite palette to make it brightness {brightness}')
        print('Will probably use a greyscale base image and layover that at different times.')


class PixelArtGenerator:
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
        out = Image.new('RGB', SIZE)
        drawing_context = ImageDraw.Draw(out)
        # drawing_context.rounded_rectangle(((0, 0), SIZE), radius=10, 
        #                                   fill=color, outline=border_color,
        #                                   width=10)
        drawing_context.rectangle((0, 0), fill=color, outline=border_color, width=BORDER)
        
        return out
        
    def create_color_swatch(self, palette_name):
        color_list = list(self.palette[palette_name].items())
        color_swatch = list(itertools.permutations(color_list, 2))
        
        swatch_size = SIZE[0] * len(color_swatch), SIZE[1] * 2
        swatch = Image.new('RGB', swatch_size)
        drawing_context = ImageDraw.Draw(swatch)
        
        i, j = 0, 0
        for background, foreground in color_swatch:
            print()
            print(background[0])
            print(foreground[0])
            topleft = i * SIZE[0], j * SIZE[1]
            bottomright = topleft[0] + SIZE[0], topleft[1] + SIZE[1]
            drawing_context.rectangle((topleft, bottomright), 
                                      fill=(foreground[1][0], foreground[1][1], foreground[1][2]), 
                                      outline=(background[1][0], background[1][1], background[1][2]), 
                                      width=BORDER)
            
            i += 1
            if i >= len(color_list):
                i = 0
                j += 1
                
        swatch_path = f'{palette_name}-swatch-{SIZE[0]}x{SIZE[1]}.png'
        swatch.save(swatch_path, 'PNG')
        return swatch_path
        

    def create_sprite(self, shape: PolygonSprite, rotation: float) -> Image:
        out = Image.new('RGBA', SIZE)
        drawing_context = ImageDraw.Draw(out)
        drawing_context.regular_polygon((CENTER, RADIUS), shape.value['n'], rotation, 
                                        fill=self.get_color_code('plasma8', shape.value['fill_color']),
                                        outline=self.get_color_code('plasma8', shape.value['border_color']), 
                                        width=1)
        drawing_context.regular_polygon((CENTER, RADIUS-WIDTH), shape.value['n'], rotation,
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
        """ Note that a complete version of this function would include a swatch, the color codes and names on the sheet. """
        sample_sheet_size = SIZE[0]*len(shapes), SIZE[1]
        sample_sheet = Image.new('RGBA', sample_sheet_size, self.get_color_code('plasma8', 'black'))
        
        for i, shape in enumerate(shapes):
            sprite = self.create_sprite(shape, 0)
            sample_sheet.paste(sprite, (i*SIZE[0], 0))
        
        sample_sheet.save(('sample spritesheet (' + str(SIZE[0]) + 'x' + str(SIZE[1]) + ').png'), 'PNG')
            

if __name__ == '__main__':
    # asset_manager = PixelArtGenerator('resources/palettes.json')
    # asset_manager.create_color_swatch('plasma8')
    
    
    sys.exit()