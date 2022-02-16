"""
Copyright(c) 2022 SoftFish

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and / or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# c.py: ANSI Escape Sequence colors

# 'constants' -- feel free to change at runtime ;P
RESET = "\033[0m"

def esc(c):
   return f"\033[{c}m"# + str(c) + "m"


def clear(line=True):
   if line:
      return "\033[K"
   return "\033[2J"

# ANSI Colors
def c(c, bg=0, i=0):
   if(c < 8 and i < 2 and bg < 2):
      return esc(f"{c + 30 + i*60 + bg*10}")
   return RESET


# RGB6*6*6 colors
def rgb8(r, g, b, bg=0):
   return esc(f"{38 + 10*(bg&1)};5;{16 + 36*r + 6*g + b}")
   #return esc(str(38 + 10*(bg&1)) + ";5;" + str(16 + 36*r + 6*g + b))

def rgb24(r, g, b, bg=0):
   # Generate terminal escape string
   return esc(f"{38 + 10*(bg & 1)};2;{str(r)};{str(g)};{str(b)}")

# 24-bit color in the terminal!
# 0x bg rr gg bb
def c24(color):
   # Set up arguments for the color printer
   args24 = {"r": (color >> 16 & 0xff), "g": (color >> 8  & 0xff), "b": (color >> 0  & 0xff), "bg":(color >> 24 & 0x01)}
   args8 = dict(args24); args8["r"] //= 43; args8["g"] //= 43; args8["b"] //= 43
   # Convert to 256-color as fallback, but append 24-bit color selector to end
   return f"{rgb8(**args8)}{rgb24(**args24)}"

# use c24 -> it will handle backwards-compat
#def c8(color):
#   bg = color >> 12 & 0x01
#   r  = color >> 8  & 0x07
#   g  = color >> 4  & 0x07
#   b  = color >> 0  & 0x07
#   print (r, g, b, bg)
#   return rgb8(r if r < 6 else 5, g if g < 6 else 5, b if b < 6 else 5, bg)

