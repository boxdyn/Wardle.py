"""
Copyright(c) 2022 SoftFish

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and / or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# c.py: ANSI Escape Sequence colors
from math import floor

def esc(c):
  return "\033[" + str(c) + "m"

# ANSI Colors
def c(c, bg=0, i=0):
  if(c < 8 and i < 2 and bg < 2):
    return esc(str(c + 30 + i*60 + bg*10))
  return reset


# RGB666 colors
def rgb666text(r, g, b, bg=0):
  return esc(str(38 + 10*(bg&1)) + ";5;" + str(16 + 36*r + 6*g + b))

def rgb888text(r, g, b, bg=0):
  sc=";"
  # Generate terminal escape string
  return esc(str(38 + 10*(bg&1)) + ";2;"+str(r)+sc+str(g)+sc+str(b))

# 24-bit color in the terminal!
# 0x bg rr gg bb
def c24(color):
  bg = (color >> 24 & 0x01)
  r  = (color >> 16 & 0xff)
  g  = (color >> 8  & 0xff)
  b  = (color >> 0  & 0xff)
  # Convert to 256-color as fallback, but append 24-bit color selector to end
  return rgb666text(r//43, g//43, b//43, bg) + rgb888text(r, g, b, bg)

def c8(color):
  bg = color >> 12 & 0x01
  r  = color >> 8  & 0x07
  g  = color >> 4  & 0x07
  b  = color >> 0  & 0x07
  print (r, g, b, bg)
  return rgb666text(r if r < 6 else 5, g if g < 6 else 5, b if b < 6 else 5, bg)

reset = "\033[0m"


