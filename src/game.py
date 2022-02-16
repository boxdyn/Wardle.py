"""
Copyright(c) 2022 SoftFish

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and / or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import ui
import color as c
import argparse
from time import sleep
from datetime import date
from signal import signal
from signal import SIGINT
from os import get_terminal_size, terminal_size

# Provide a clean getaway
def end(*args, **kwargs):
   ui.clear()
   exit(*args, **kwargs)

# Set up sigint handler
def handler(signum, frame):
   if signum == SIGINT:
      end()
signal(SIGINT, handler)

# Set up argument parser
parser = argparse.ArgumentParser(
   description='A barebones CLI Wordle clone, using official Wardle solutions. You have been warned.'
   )
parser.add_argument('day',    nargs="?",           type=int, help="Wordle day number")
parser.add_argument('-g',     metavar="guesses",   type=int, help="number of guesses (bounded by terminal size)")
parser.add_argument('--hard', metavar="0-3", \
                              nargs="?", const=2,  type=int, help="0:normal  1:~greenie  2:*hard  3:+greyless")
parser.add_argument('--word', metavar="solution",            help="force a particular word")
parser.add_argument('--list', metavar="wordlist",            help="use a custom wordlist")
parser.add_argument('--classic',    action='store_true',     help="use the classic Wordle word list")
#parser.add_argument('-c',           action='store_true',     help="enable colorblind mode") # TODO
parser.add_argument("--nokeyboard", action='store_true',     help="disable the keyboard")
parser.add_argument('--nonsense',   action='store_true',     help="allow nonsensical guesses")
parser.add_argument('--center',     action='store_true',     help="center the screen")

# Parse the args
args = parser.parse_args()

# Handle the args
#   Select the correct word list
Words, Answers, data = [], [], {"name":"", "version":"", "guesses":-1, "launch":(1970,1,1)}
default_data = {
   "name": "Wardle.py",
   "version": "-1",
   "guesses": 6,
   "launch": (2022, 2, 13),
   "boxes":  ["⬛",     "🟨",      "🟩",     "  ",     "  "],
   "colors": [0x13a3a3c, 0x1b59f3b, 0x1538d4e, 0xd7dadc, 0x1121213],
   "keyboard": ["qwertyuiop", "asdfghjkl", "zxcvbnm"+u"\u23CE"]
}
data = dict(default_data)
if not args.list:
   args.list = "w2"
args.list = "w" if args.classic else args.list
# lol everything's a good py
exec(f"from {args.list} import Words, Answers, Metadata as data")
#   Get today's day number
if args.day is not None:
   # Ahoy-hoy, time traveller!
   d = args.day
else:
   # find num. days since Wordle launch
   d = (date.today() - date(*data["launch"])).days
#   g is for "maximum guesses"
if args.g:
   max_guesses = min(get_terminal_size().lines - 10, abs(args.g))
else:
   max_guesses = data["guesses"]
#   Get today's word
if args.word:
   solution = args.word
   # Indicate a non-standard word
   d = "Custom"
   # If solution not in words list, enable nonsense
   if solution not in Words + Answers:
      args.nonsense = True
else:
   d = len(Answers) - 1 if d >= len(Answers) else 0 if d < 0 else d
   solution = Answers[d]

# Bound hardmode
if not args.hard:
   args.hard = 0
elif args.hard < 0:
   args.hard = 0
elif args.hard > 3:
   args.hard = 3
# End arg parsing


# ! The game is below this point

# Good data structures to have
# Load data
for key in default_data:
   if key not in data:
      data[key] = default_data[key]

#   Box characters!
GRAY, YELLOW, GREEN, WHITE, BLACK = range(5)
boxes = data["boxes"] if "boxes" in data else default_data["boxes"]
colors = data["colors"]

#   Guesses go here
guesses = []

# Letter is in boxes
def wordbox(word, showword = 0):
   line = [GRAY] * len(word)
   guess = list(word)
   sol   = list(solution)
   # Green pass
   for i in range(len(word)):
      if guess[i] == sol[i]:
         # Mark the letter 'green' (2)
         line[i] = GREEN
         if word[i] in letters:
            letters[word[i]] = GREEN
         # Remove letter from solution and guess
         sol[i] = guess[i] = GRAY
   # Yellow pass
   for i in range(len(word)):
      if guess[i] and word[i] in sol:
         # Mark the letter 'yellow' (1)
         line[i] = YELLOW
         if word[i] in letters:
            l = letters[word[i]]
            if l in (BLACK, GRAY): letters[word[i]] = YELLOW
         # Remove letter from solution and guess
         sol[sol.index(word[i])] = guess[i] = GRAY
   # Gray pass
   for i in range(len(word)):
      if word[i] in letters and \
         line[i] == GRAY and letters[word[i]] == BLACK:
         if word[i] in letters:
            letters[word[i]] = GRAY
   # Turn blocks into a string, and print it
   output = ""
   if showword:
      # Move up to replace the input box
      for i in range(len(word)):
         output += f"{c.c24(colors[WHITE])}{c.c24(colors[line[i]])} {word[i].upper()} {c.RESET}"
   else:
      for i in line:
         output += f"{c.c24(colors[WHITE])}{c.c24(colors[i])}{boxes[i]}{c.RESET}"
   return f"{output}\n"


letters = {}
keyboard = data["keyboard"]

def init_keeb():
   for s in keyboard:
      for char in s:
         letters[char] = BLACK
   return

def keeb(x, y):
   if args.nokeyboard:
      return
   def colorify(string):
      s = ""
      for char in string:
         s += c.c24(colors[letters[char]]) + " " + char + " " + c.RESET
      return s
   for i in range(len(keyboard)):
      ui.uprint(x-(3*len(keyboard[i])//2), y+i, colorify(keyboard[i]))

ORDINAL = ["1st", "2nd", "3rd", "4th", "5th"]

def hardmode(word, solution:str, level):
   # If hard mode disabled, Continue
   if not args.hard:
      return
   hints = {
      GREEN:  [],
      YELLOW: [],
      GRAY:   [],
      BLACK:  [],
   }
   # For each letter, record which state it has
   for letter in word:
      if letter not in letters:
         letters[letter] = BLACK
      hints[letters[letter]].append(letter)
   # Green pass
   if level >= 1:
      for l in hints[GREEN]:
         i = solution.find(l)
         if i >= 0 and word[i] is not l:
            ORDINAL = ["1st", "2nd", "3rd", "4th", "5th"]
            return f"{ORDINAL[i]} letter must be {l}"
   # Yellow pass
   if level >= 2:
      for l in hints[YELLOW]:
         if l not in word:
            return f"Guess must contain {l}"
   # Gray pass
   if level >= 3:
      for l in hints[GRAY]:
         if l in word:
            return f"Guess must not contain {l}"
   return


#   intro: Print the intro text
def intro(x, y):
   # Assemble the text
   HARDCHARS = [" ", "~", "*", "+"]
   title  = f"{data['name']} {d}{HARDCHARS[args.hard]}"
   # Center the text
   ui.uprint(x-(len(title)//2), y, f"{c.RESET}{title}")

def game():
   thicc = {"top":0, "intro": 2, "field":max_guesses+1, "keeb": 0 if args.nokeyboard else 3}
   x = ui.size[0]//2
   # Print the title (2 rows)
   intro(x,thicc["top"])
   # Field goes here (max_guesses+1) rows
   # Print the keyboard
   init_keeb()
   keeb(x, thicc["intro"] + thicc["field"])

   words = Words + Answers
   while len(guesses) < max_guesses:
      # Calculate board's starting depth
      health = 2 + len(guesses)
      # lol i should probably use curses
      user_input = ui.uinput(x-(len(solution)//2), health, f"{c.clear()}{c.c24(colors[WHITE])}").lower()
      # This provides some leniency for multiple-length word lists,
      # by first checking if the input is the length of the solution,
      # and discarding without penalty otherwise.

      if s := hardmode(user_input, solution, args.hard):
         ui.uprint(x-(len(s)//2), health, s)
         sleep(1)
      elif len(user_input) is len(solution)and (user_input in words or args.nonsense):
         # Add guesses to the guessed list, and put the word in boxes
         guesses.append(user_input)
         ui.uprint(x-(len(solution)*3//2), health, wordbox(user_input, 1))
         # update the keeb
         keeb(x, thicc["intro"] + thicc["field"])
         if (user_input == solution):
            # win
            win(True)
            return
      else:
         # Allow the user to make it stop
         if user_input == "exit":
            end()
         # Alert the user that the word was not found in the list, and wait for them to read it
         s = "Not in word list."
         ui.uprint (x-(len(s)//2), health, s)
         sleep(1)
   # lose
   win(False)

def win(won):
   used_guesses = len(guesses) if won else "X"
   share = f"{data['name']} {d} {used_guesses}/{max_guesses}{'*' if args.hard else ''}\n"
   for gi in guesses:
      share += f"{wordbox(gi)}"
   # ui.move to the end of the screen, and print the sharable boxes
   print(f"{ui.m(0, ui.size[1] + 1)}{share}", end="")

def init():
   h = 2 + max_guesses + 1 + (0 if args.nokeyboard else 4)
   if (args.center):
      w, stty = max(30, 3*len(solution)), get_terminal_size()
      # You can init a "screen" 'anywhere'!
      ui.init(w, h, (stty.columns - w) // 2, 0)
   else:
      ui.init(max(30, 3*len(solution)), h)