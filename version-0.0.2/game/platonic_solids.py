# import math
import json

import PIL
import numpy as np
import fresnel


# Golden Ratio
PHI = (1 + np.sqrt(5)) / 2.0

TETRA = np.array([[1, 1, 1],
                  [1, -1, -1],
                  [-1, 1, -1],
                  [-1, -1, 1]])

HEXA = np.array([[1, 1, 1],
                 [-1, 1, 1],
                 [-1, -1, 1],
                 [1, -1, 1],
                 [1, 1, -1],
                 [-1, 1, -1],
                 [-1, -1, -1],
                 [1, -1, -1]])

OCTA = np.array([[1, 0, 0],
                 [-1, 0, 0],
                 [0, 1, 0],
                 [0, -1, 0],
                 [0, 0, 1],
                 [0, 0, -1]])

ICOSA = np.array([[0, 1, PHI],
                  [0, -1, PHI],
                  [0, 1, -PHI],
                  [0, -1, -PHI],
                  [1, PHI, 0],
                  [-1, PHI, 0],
                  [1, -PHI, 0],
                  [-1, -PHI, 0],
                  [PHI, 0, 1],
                  [-PHI, 0, 1],
                  [PHI, 0, -1],
                  [-PHI, 0, -1]])


scene = fresnel.Scene()
geometry = fresnel.geometry.Sphere(scene, N=1, radius=10)
geometry.position[:] = [1, 1, 1]
geometry.material = fresnel.material.Material(color=fresnel.color.linear([0.25,0.5,0.9]),
                                              roughness=0.8)

# Setup the camera.
scene.camera = fresnel.camera.Orthographic.fit(scene)

# Render the scene.
out = fresnel.preview(scene)
image = PIL.Image.fromarray(out[:], mode='RGBA')
image.save('fresnel-test.png')

color_1 = fresnel.color.linear([0.70, 0.87, 0.54])*0.8
color_2 = fresnel.color.linear([0.65, 0.81, 0.89])*0.8
colors = {8: color_1, 3: color_2}
poly_info = fresnel.util.convex_polyhedron_from_vertices(ICOSA)
for id, face_sides in enumerate(poly_info['face_sides']):
    poly_info['face_color'][id] = colors[face_sides]
geometry = fresnel.geometry.ConvexPolygon(scene, poly_info, N=1)
geometry.position[:] = [[1, 1, 1]]
