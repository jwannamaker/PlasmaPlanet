import random
import math

import pyglet


def distance(a, b):
    return math.dist(a, b)

def polygons(num_polygons: int, player_position: list[int], 
             window_width: int, window_height: int):
    polygons = []
    
    for i in range(num_polygons):
        polygon_position = random.randint(0, window_width), random.randint(0, window_height)
        
        while distance(polygon_position, player_position) < 100:
            polygon_position = random.randint(0, window_width), random.randint(0, window_height)