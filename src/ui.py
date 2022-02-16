"""
Copyright(c) 2022 SoftFish

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and / or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# ui.py: ANSI Escape Sequence colors



from time import sleep
import sys, re
import c

ANSI_S = "\033[s"
ANSI_U = "\033[u"

CLEAR  = "\033[2J"


#   directions
UP    = NORTH = 'A'
DOWN  = SOUTH = 'B'
RIGHT = EAST  = 'C'
LEFT  = WEST  = 'D'


def init(width, height):
   print(c.c24(0x00f0d0) + '0123456789ABCDE' + c.RESET)
   print(("A"*width + "\n")*(height-1))
   print(m(0,-height-1) + ANSI_S, end='')
   clear()

def clear(x = 0, y = 0, behavior = 0):
   uprint(x, y, "\x1b[%dJ"%behavior)

# Move the cursor relatively on the screen
def m(x = 0, y = 0):
   # TODO: implement relative x/y movement
   s = "{}{}".format(
       m_dir(UP,   abs(y)) if y < 0 else m_dir(DOWN,  y) if y > 0 else "",
       m_dir(LEFT, abs(x)) if x < 0 else m_dir(RIGHT, x) if x > 0 else "")
   return s

#   Move the cursor relatively on the screen
def m_dir(dir, steps=1):
   if ord('A') <= ord(dir) <= ord('D') :
      return "\033[{}{}".format(steps, dir)
   return ""

#  Position the cursor absolutely on the screen (0-index)
def m_abs(x, y):
   return "\033[{};{}H".format(y+1, x+1)

ui_input, ui_print = input, print

def uprint(x, y, *args, end='', **kwargs):
   ui_print(ANSI_S + m(x, y), end='')
   ui_print(*args, ANSI_U, **kwargs, end='')
   ui_print(ANSI_U, end=end)
   sys.stdout.flush()


def uinput(x, y, *args, **kwargs):
   ui_print(ANSI_S + m(x, y), end='')
   r = ui_input(*args, **kwargs)
   ui_print(ANSI_U, end='')
   sys.stdout.flush()
   return r
