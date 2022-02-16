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
def end():
   ui.clear()
   exit()

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
parser.add_argument('-g',     metavar="guesses",   type=int, help="number of guesses (limited by terminal size)")
parser.add_argument('--word', metavar="solution",            help="force a particular word")
parser.add_argument('--list', metavar="wordlist",            help="use a custom wordlist")
parser.add_argument('--classic',  action='store_true',       help="use the classic Wordle word list")
parser.add_argument('--nonsense', action='store_true',       help="allow nonsensical guesses")
parser.add_argument('--hard',     action='store_true',       help="enable hard mode (wip)")
parser.add_argument('--center', action='store_true',         help="center the screen")
# TODO: Implement hard mode properly (more than just a *)

# Parse the args
args = parser.parse_args()

# Handle the args
#   Select the correct word list
Words, Answers, data = [], [], {"name":"", "version":"", "guesses":-1, "launch":(1970,1,1)}
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
# End arg parsing


# ! The game is below this point

# Good data structures to have
#   Box characters!
GRAY, YELLOW, GREEN, WHITE, BLACK = range(5)
boxes = ["⬛",     "🟨",      "🟩",     "  ",     "  "]
colors= [0x13a3a3c, 0x1b59f3b, 0x1538d4e, 0xd7dadc, 0x1121213]
#   Guesses go here
guesses = []
letters = [4] * 27


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
         letters[letter_num(word[i])] = GREEN
         # Remove letter from solution and guess
         sol[i] = guess[i] = GRAY
   # Yellow pass
   for i in range(len(word)):
      if guess[i] and word[i] in sol:
         # Mark the letter 'yellow' (1)
         line[i] = YELLOW
         letters[letter_num(word[i])] = YELLOW
         # Remove letter from solution and guess
         sol[sol.index(word[i])] = guess[i] = GRAY
   # Gray pass
   for i in range(len(word)):
      if line[i] == GRAY:
         letters[letter_num(word[i])] = GRAY
   # Turn blocks into a string, and print it
   output = ""
   if showword:
      # Move up to replace the input box
      output += ui.m(0,-1)
      for i in range(len(word)):
         output += f"{c.c24(colors[WHITE])}{c.c24(colors[line[i]])} {word[i].upper()} {c.RESET}"
         #output += c.c24(colors[3]) + c.c24(colors[line[i]]) + " " + word[i].upper() + " " + c.RESET
   else:
      for i in line:
         output += f"{c.c24(colors[WHITE])}{c.c24(colors[i])}{boxes[i]}{c.RESET}"
   return output

def letter_num(char):
   if ord('a') <= ord(char.lower()) <= ord('z'):
      return ord(char.lower()) - ord('a')
   return 26

def keeb(x, y):
   def colorify(string):
      s = ""
      for char in string:
         s += c.c24(colors[letters[letter_num(char)]]) + " " + char + " " + c.RESET
      return s
   S = ["qwertyuiop", "asdfghjkl", "zxcvbnm"+u"\u23CE"]
   for i in range(len(S)):
      ui.uprint(x-(3*len(S[i])//2), y+i, colorify(S[i]))


#   intro: Print the intro text
def intro():
   title  = f"{data['name']} {d}{'*' if args.hard else ''}"
   center = ui.m(-len(title)//2,0)
   #spaces = ' ' * ((14 - len(title)) // 2)
   # [  Wordle 100* ]
   intro  = f"{c.RESET}{center}{title}"
   return intro

def game():
   x = ui.size[0]//2
   ui.uprint(x, 0, intro())
   words = Words + Answers
   guess = 0
   keeb(x, 3 + max_guesses)
   while guess < max_guesses:
      # lol i should probably use curses
      user_input = ui.uinput(x-(len(solution)//2), len(guesses) + 2, c.clear()).lower()
      # This provides some leniency for multiple-length-word lists,
      # by first checking if the input is the length of the solution,
      # and discarding without penalty otherwise.
      if len(user_input) is len(solution) and (user_input in words or args.nonsense):
         # Add guesses to the guessed list, and put the word in boxes
         guesses.append(user_input)
         ui.uprint(x-(len(solution)*3//2), len(guesses) + 2, wordbox(user_input, 1))
         # Print the new keyboard
         keeb(x+1, 3 + max_guesses)
         # win condition
         if (user_input == solution):
            win(True)
            return
         else:
            guess += 1
      else:
         # Allow the user to make it stop
         if user_input == "exit":
            end()
         # Alert the user that the word was not found in the list, and wait for them to read it
         ui.uprint (x-(3*len(solution)*3//2), len(guesses) + 2, "not in word list.")
         sleep(1.5)
   # lose
   win(False)

def win(won):
   used_guesses = len(guesses) if won else "X"
   share = f"{data['name']} {d} {used_guesses}/{max_guesses}{'*' if args.hard else ''}\n"
   for gi in guesses:
      share += f"\n{wordbox(gi)}"
   # ui.move to the end of the screen, and print the sharable boxes
   print(f"{ui.m(0, ui.size[1] + 1)}{share}", end="")


if (args.center):
   w, h, stty = max(30, 3*len(solution)), 7 + max_guesses, get_terminal_size()
   # You can init a "screen" 'anywhere'!

   ui.init(w, h, (stty.columns - w) // 2, 0)
else:
   ui.init(max(30, 3*len(solution)), 7 + max_guesses)
game()