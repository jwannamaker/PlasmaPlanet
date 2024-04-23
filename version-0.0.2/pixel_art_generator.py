import sys
import json
from enum import Enum
from pathlib import Path

from PIL import Image, ImageDraw

CURR_DIR = Path.joinpath(Path.cwd(), 'version-0.0.2')

MARGIN = 2
RADIUS = 64
SIZE = round((RADIUS+MARGIN)*2), round((RADIUS+MARGIN)*2)
CENTER = RADIUS+MARGIN, RADIUS+MARGIN

def load_palette(file) -> dict:
    with open(Path.joinpath(CURR_DIR, file)) as f:
        return json.load(f)
    
MASTER_PALETTE = load_palette('palettes.json')

def get_color_code(palette, color) -> tuple[int, int, int]:
    for palette_color in list(MASTER_PALETTE[palette].keys()):
        if color in palette_color:
            return (MASTER_PALETTE[palette][palette_color][0], 
                    MASTER_PALETTE[palette][palette_color][1], 
                    MASTER_PALETTE[palette][palette_color][2])


class PolygonSprite(Enum):
    TRIANGLE = {'n': 3, 'fill_color': 'tangerine', 'border_color': 'yellow'}
    SQUARE = {'n': 4, 'fill_color': 'pine', 'border_color': 'seafoam'}
    PENTAGON = {'n': 5, 'fill_color': 'muted-red', 'border_color': 'pastel-pink'}
    HEXAGON = {'n': 6, 'fill_color': 'dusk', 'border_color': 'lavender'}
    OCTAGON = {'n': 8, 'fill_color': 'tangerine', 'border_color': 'yellow'}



def create_sprite(shape: PolygonSprite, rotation: float) -> Image:
    bounding_circle = CENTER, RADIUS
    out = Image.new('RGBA', SIZE)
    drawing_context = ImageDraw.Draw(out)
    drawing_context.regular_polygon(bounding_circle, shape.value['n'], rotation, 
                                    fill=get_color_code('plasma8', shape.value['fill_color']),
                                    outline=get_color_code('plasma8', shape.value['border_color']), 
                                    width=1)
    drawing_context.regular_polygon((CENTER, RADIUS-(MARGIN*5)), shape.value['n'], rotation,
                                    fill=(0, 0, 0, 0),
                                    outline=get_color_code('plasma8', shape.value['border_color']))
    return out

def create_sprite_sheet(shape: PolygonSprite, steps: int):
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
        sprite = create_sprite(shape, current_angle)
        sprite_sheet.paste(sprite, (i*SIZE[0], j*SIZE[1]))
        current_angle += increment
        # if i + 1 == 10:
        #     i = 0
        #     j += 1
        # else:
        #     i += 1
        i += 1
        
    # sprite_sheet_path = Path.joinpath(CURR_DIR, 'sprite sheets', shape.name.lower(), shape.value['fill_color'])
    sprite_sheet.save((shape.value['fill_color'] + ' ' + shape.name.lower() + ' spritesheet (' + str(SIZE[0]) + 'x' + str(SIZE[1]) + ').png'), 'PNG')

def create_sample_sheet(shapes: list[PolygonSprite]):
    """ Note that a complete version of this function would include a swatch, the color codes and names on the sheet. """
    sample_sheet_size = SIZE[0]*len(shapes), SIZE[1]
    sample_sheet = Image.new('RGBA', sample_sheet_size, get_color_code('plasma8', 'black'))
    
    for i, shape in enumerate(shapes):
        sprite = create_sprite(shape, 0)
        sample_sheet.paste(sprite, (i*SIZE[0], 0))
    
    sample_sheet.save(('sample spritesheet (' + str(SIZE[0]) + 'x' + str(SIZE[1]) + ').png'), 'PNG')
        

if __name__ == '__main__':
    create_sample_sheet([i for i in PolygonSprite])
        
    sys.exit()