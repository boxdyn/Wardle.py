"""
Copyright(c) 2022 SoftFish

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and / or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# ui.py: ANSI Escape Sequence colors

import sys

ANSI_S = "\033[s"
ANSI_U = "\033[u"

CLEAR  = "\033[2J"


#   directions
UP    = NORTH = 'A'
DOWN  = SOUTH = 'B'
RIGHT = EAST  = 'C'
LEFT  = WEST  = 'D'

size = [0,0]

# init: Initialize the "screen" and ensure the appropriate area is on screen and cleared
def init(width, height, x=0, y=0):
   size[0], size[1] = width, height
   for i in range(y,y+height):
      uprint(x,i," "*width)
   uprint(x,height+y,f"{m(0, -height)}{ANSI_S}")
   clear()

def clear(x = 0, y = 0, behavior = 0):
   uprint(x, y, f"\x1b[{behavior}J")

# ANSI Escape Sequence Generators:
#   unless otherwise specified, return strings containing ANSI escape characters

# Move the cursor relatively on the screen
def m(x = 0, y = 0):
   # move on the y axis, followed by the x axis
   s = f"{m_dir(UP,   abs(y)) if y < 0 else m_dir(DOWN,  y) if y > 0 else ''}" + \
       f"{m_dir(LEFT, abs(x)) if x < 0 else m_dir(RIGHT, x) if x > 0 else ''}"
   return s

#   Move the cursor relatively on the screen in a given direction
def m_dir(dir, steps=1):
   if ord('A') <= ord(dir) <= ord('D') :
      return f"\033[{steps}{dir}"
   return ""

#  Position the cursor absolutely on the screen (0-index)
def m_abs(x, y):
   return f"\033[{y+1};{x+1}H"

# print/input wrappers
#   uprint: call print at a given x,y position, relative to the cursor
def uprint(x, y, *args, **kwargs):
   print(f"{ANSI_S}{m(x, y)}", end='')
   print(*args, **kwargs, end='')
   print(ANSI_U, end='')
   sys.stdout.flush()

#   uinput: call input at a given x,y position, relative to the cursor
#     returns: string containing user input
def uinput(x, y, *args, **kwargs):
   print(f"{ANSI_S}{m(x, y)}", end='')
   r = input(*args, **kwargs)
   print(ANSI_U, end='')
   sys.stdout.flush()
   return r
