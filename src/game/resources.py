import pyglet


# Initializing the path Pyglet will search first to find resources for the application.
pyglet.resource.path = ['../resources', '../resources/images', '../resources/data']
pyglet.resource.reindex()

palette = pyglet.resource.file('palette.json') 
font = pyglet.resource.image('large-palace-font-white.png')
tilemap = pyglet.resource.file('tilemap.json')

# All the images!
player_choice_image = pyglet.resource.image('sample spritesheet (132x132).png')
title_card = pyglet.resource.image('title-card-GEODESICDOOM-900x64.png')
blank_image = pyglet.resource.image('blank-128x128.png')