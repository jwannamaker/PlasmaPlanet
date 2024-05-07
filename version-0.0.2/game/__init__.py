WINDOW_WIDTH = 1792
WINDOW_HEIGHT = 1120

# All measurements provided in pixels unless otherwise specified.
TILE_SIZE = 32, 16  # Unit tile size. Corresponds to the top of the cubes.
WORLD_SIZE = 5, 5  # In tiles.

SPRITE_WIDTH = 32
SPRITESHEET_BORDER = 10  # Border between sprites in spritesheets.
SPRITE_RADIUS = 32  # For polygons.
SIZE = round((SPRITE_RADIUS + SPRITESHEET_BORDER) * 2), round((SPRITE_RADIUS + SPRITESHEET_BORDER) * 2)
CENTER = SPRITE_RADIUS + SPRITESHEET_BORDER, SPRITE_RADIUS + SPRITESHEET_BORDER


from . import load
from . import basic_object
from . import asset_manager
from . import hud
