import pyglet





class IsoGrid:
    """Here, I'm going to place all the logic for creating the isometric grid 'board' for the game.
    """
    def __init__(self, tile):
        self.tiles = [[tile for _ in range(WORLD_SIZE[0])] for _ in range(WORLD_SIZE[1])]
