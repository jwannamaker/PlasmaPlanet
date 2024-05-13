# PlasmaPlanet

####  Here, you'll find a series of progress reports as I embark on a journey of self discovery via video game development. Proceed with curiosity (and caution), and witness my software development skills rapidly grow right before your eyes! I genuinely don't know if this endeavor will turn into an actual playable game that you can enjoy, so you'll just have to stay tuned in order to find out! (Essentially a dev blog?) Honestly, it's gonna be messy at times, but it's an accurate representation of my journey, the skills I'm picking up, what isues I'm working on, and all sorts of nitty-gritty-witty crap.

> I'm a new follower in the cult of ![done](https://www.youtube.com/watch?v=bJQj1uKtnus).

---

### Status Report: Tuesday 4/23/24
    
- I decided I want this game to have that special ***Polished Aesthetics Deal*** which means a few things:

1. Palette
	- There's a big emphasis on this when it comes to how a game looks and feels.
	- I looked to Lospec to guide me, and added the colors I enjoyed to `palette.json`

2. Art style
    - Pixel art!
    - Stick to my new mantra: KISS (Keep it simple, stupid).
    - Pixel art is *cool*. It lets me make *simple* things ***awesome***.
    - Upon the realization that hand drawing (or even computer aided) would be FAR too tedious I did what any good programmer does best--I wrote up `pixel_art_generator.py`, a script that generates sprite sheet and images for regular polygons using the color palettes I defined in a separate file. Pictured here is the encouraging results of that endeavor!

		![Sample spritesheet showcasing the different polygons](<src/resources/images/sample-spritesheet-(132x132).png>)

---

### Status Report: Thursday 5/2/24
    
- Lots of project restructuring since last week.
- Still working through Pyglet's [in-depth asteroids tutorial](https://pyglet.readthedocs.io/en/latest/programming_guide/examplegame.html#making-the-player-and-asteroid-sprites).
        
- Palette
    - Finished a swatch generator in `PixelArtist` (which is now located in the `asset_manager` submodule of `game`).
    - Planning to have the palette name, each color name, and color code included in the image in future implementation.    
    - Mixing opacities would be helpful as well, so I can produce more possible gradients.
    - For the implementation, I ended up using `itertools.permutations` to get a list of each possible background and foreground, and then to get the size of the `.png` to create, I separated the list of tuples into a dict, where each key is the name of the background color, and the value is the slice of the permutations list where the background color appears first in the pair.

- Style
    - Turning my focus towards introducing an isometric grid to the game, which means more methods in PixelArtist to generate isometric images.
    - Looking at buying [Aseprite $19.99](https://www.aseprite.org/), the tool of choice for *literally* every pixel artist on YouTube, for the cases where it's more effort to proceedurally generate the pixel art instead of just drawing it. Additionally, proceedurally generating the art implies that I've already decided on final designs; I'm finding it more difficult to repeatedly tweak a method, run it in a somewhat isolated submodule of my game, save the *.png into the now behemoth of a folder that `resources` has become, rinse and repeat if I want to see a minor difference in the drawing.

    	![Twilight 5 Palette Swatch](<src/resources/images/twilight5-swatch-84x84.png>)
		*Palette swatch generated from [Twilight 5](https://lospec.com/palette-list/twilight-5) using my `PixelArtist`*

    	![Cryptic Ocean Palette Swatch](<src/resources/images/cryptic-ocean6-swatch-84x84.png>)
		*Palette swatch generated from [Cryptic Ocean](https://lospec.com/palette-list/cryptic-ocean) using my `PixelArtist`*
  
**Moving Forward**

---

### Status Report: Monday 5/6/24

- I decided that no matter how exciting the finished result is in my mind, it will be 1000000% better if I can plan out my steps methodically and thoughtfully. That's how I'll maximize productivity: by first having a clear vision of where I want to go.

- ~Palette~ Art & Design
	- Came across a $0.99/mo Asesprite clone for iPad/iPhone called ![Resprite](https://resprite.fengeon.com/doc) and it's been working out really well!
	- This morning I created a font as a horizonatal spritesheet in Resprite, and as of right now, I'm able to render that font onto the game screen which is extremely gratifying. I feel so cool just knowing that I drew all of the letters by *hand*.

![My Custom Pixel Art Font](<src/resources/images/large-palace-font-white.png>)
*My handrawn pixel art font.*
 
		
![My Custom Pixel Art Font in black](<src/resources/images/large-palace-font-black.png>)
*My handrawn pixel art font (in black).*

- I had a one night stand with Godot in a deserate attempt to just *see* my cute little cubes on the screen in an isometric grid... It worked of course, but at what cost? I decided to come crawling back to Pyglet because I want to have my hand in every single aspect of the game that I'm creating. It wasn't as simple of a process as I perceived it to be, and in the end I just felt... wrong. Like I'd betrayed a fundamental element of this game making journey. I want my game to look the absolute best that I can produce ***on my own***. My goal is to showcase the  skills that I have built up in all of this time since I started coding. Yes, I have high expectations, but that's only because the push towards something greater than where I currently reside *drives* me.

So, ***onward and upward***
   
---

### Status Report: Thrusday 5/9/24

- I still need to determine a definitive direction that I'm trying to go with this. When I close my eyes, what is it that I see? What game do I want to play? Does the end result even matter in this case if my true goal is to simply grow my skills and build my portfolio?
- Reinvigorated by the need to have something I can playtest, I went back to Pyglet's Asteroid example and added any relevant files from the examples subdirectory of that ![repo](https://github.com/pyglet/pyglet.git). I'm sorta caught between this desire to make everything OOP, and dreading the impending data coupling. It almost feels... unneccessary right now? I can do without OOP, I could even benefit from treating the code base more modularly, if I can just get over what school has drilled in me so far about obsessively abstracting.
- Putting the possibility of publishing my game online on the table! More on that later.
- Sometimes it's difficult to make sure I get everything I can into this report!
- I realized that the real crux of this project is going to be the mechanism that takes in a 3D object (rather, the digital representation of it, such as a unit tetrahedron), allows me to manipulate that object (ex: 30 degree rotation along the z axis), and finally outputs the modified 3D object, creating the experience of being immersed in a pixelated, isometric world.

> That's.... what rendering.... is...? (mini facepalm)

![Game screenshot](<src/resources/images/screenshot 5-7-24.png>)
*Screenshot of custom font loaded into the game Tuesday.*

- I had such a beautiful moment when I just automatically created a new virtual environment for a file, without having to look anything up or think about it, I just knew already what I had to do and then it was done. This is the ultimate superpower in the cult of done, I think.

	Done is the engine of more.
- I'm picking up a lot of skills that I know will lead me somewhere grand. Like image manipulation, on-the-fly creating an asset that needs to be loaded into the project in real-time? Yeah, honestly, it sounds more and more to me like I'm working towards entering the video game industry as a technical artist all of the time! Exciting!

---

### Status Report: Sunday 5/11/24

- Spending most of my time tackling the Isometric rendering aspect of the game. Which means
	- Trigonometry
	- Linear Algebra/Matrix Transformations
	- Quaternions
...have all come up in the past dozen or so hours of my studies.
- A series of very, very helpful websites that I've come across:
	- [Isometric Projection](http://www.gandraxa.com/isometric_projection.xml)
	- [Isometric Tiling](http://www.gandraxa.com/isometric_tiling.xml)
	- [Linear Algebra for Programmers](https://www.linearalgebraforprogrammers.com/blog/isometric_projection)
	- [Isometric Pixel Art Blog](https://www.slynyrd.com/blog/2022/11/28/pixelblog-41-isometric-pixel-art)

---

### Status Report: Monday 5/12/24

- Making (another) side project which, at its core, is really just a custom tool for this game. Its purpose is to speed up the process of creating isometric renders of polyhedra (vertices uploaded from a .json) by allowing me to view the renders (via matplotlib) and permute the order of the vertices/faces drawn in real time. I'm breaking SOLID programming principles by having it include a second purpose though, which is palette/gradient synthesis via choosing Color A, Color B, and viewing the interpolated results as color blocks. Once everything looks good, the results can be exported as a .json of the colors, a .json of the (correctly) ordered polyhedra vertices, and .png images of both.
