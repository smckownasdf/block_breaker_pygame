"""
-------------
Requirements:
-------------
Libraries:
- Python3 (Currently only tested with Python 3.6.8) and the included CSV module
- pygame (python3 -m pip install -U pygame --user)
- pygame_textinput (found here: https://github.com/Nearoo/pygame-text-input)

File Assets:
- bblevels.py (should have been downloaded with this file, 
from https://github.com/smckownasdf/block_breaker_pygame)
- ball.png (can be any png image with that title, preferably one depicting a ball on a black background)
-------------
Regarding File Locations: 
bblevels.py, ball.png, and pygame_textinput.py should be placed in the same folder 
in which you store and run block_breaker_pygame.py

A file called highscore.csv, which acts as a save file for the top 5 high score results,
will be created automatically if it does not already exist.

--------------------
Why did I make this?
--------------------

For fun, of course. And self-education.
After taking a course using C# and Unity to develop games,
I found myself disappointed with how much Unity does for you behind the scenes.
I wanted a more in-depth understanding of how different elements work together 
to create an interactive experience, but as a relatively 'green' programmer
I still wanted the language and building blocks to be relatively accessible.
After doing some research, the pygame module seemed like a great balance for what 
I wanted - and it's native to the language I'm most comfortable using.

Given this project is a means of continuing my education in Python3 using OOP,
I gladly welcome critical eyes. If you spot any errors, things that could be written 
better, or oversights (of which I'm sure there are many) I would love to hear / see 
your corrections / suggestions.

Feel free to modify bblevels.py to add more levels or create your own (explained in 
simple terms below), or to modify and take from this code as you see fit.

Thank you for taking the time to look at this, and if you're learning too, I hope 
that something here helps with that process. 

---------------------------
How to make your own levels
---------------------------

bblevels.py can be opened with any text or code editor.
Changing the extension from .py to .txt temporarily 
might make opening it easier with certain programs / operating systems.

Level layouts within bblevels file are 26 characters wide (between quotes)
and 26 lines high.

Only one ball and one paddle are allowed currently.
Their position within layout does not actually matter.

Be sure to add corresponding entries to "bonus_time" within bblevels.py. 
Integer values refer to milliseconds.

----------

For each of the the following elements added, 
you must delete a space within same line of the template:

1 - will create a single-hit (orange) block
2 - will create a double-hit (blue) block
3 - will create a triple-hit (seafoam) block

---------

Each of the following elements will change the required character length
of their respective line within the template:

/ - will create half a character length to offset blocks. Must be used in pairs.
  - Each pair of / will add one character to required line length
X - will create an extra large three-hit block
  - Does not actually require different character length within its line, 
  - but will overlap any blocks placed immediately after or below it
  - To avoid overlap make sure the characters to the left and below are both spaces

---------
Template:
---------

Copy and paste this template, replacing "#" with the number of the level you want 
this template to become.

Be sure to avoid incorrect or duplicate level names, such as a level titled "levle4", 
or two layouts titled "level4". This might result in unwanted behaviour.

If you wish to overwrite my default level1, level2, or level3, simply do so. 
They're not masterpieces by any means.

Finally, the template:

	"level#":
	[
		"               B          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"                          ",
		"          P               ",
		"                          ",
	],

Thank you for your time and interest!

Scott McKown

"""
