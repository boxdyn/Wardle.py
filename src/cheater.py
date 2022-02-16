"""
Copyright(c) 2022 SoftFish

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and / or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import w
import argparse
import color as c
from time import sleep
from datetime import date, timedelta
from signal import signal
from signal import SIGINT
from os import get_terminal_size

# Provide a clean getaway


def end():
   exit()

# Set up sigint handler


def handler(signum, frame):
   if signum == SIGINT:
      end()


signal(SIGINT, handler)

# Set up argument parser
parser = argparse.ArgumentParser(
    description='A Wordle cheating tool. You have been warned.'
)
parser.add_argument('day',    nargs="?",         type=int, help="Wordle day number")
parser.add_argument('-l',     metavar="solution",          help="look up the day of a given solution")
parser.add_argument('-d',     metavar="day",     type=int, help="look up the solution of a given day")
parser.add_argument('--word', metavar="word",              help="Change the hint word")
parser.add_argument('--classic',  action='store_true',     help="use the classic Wordle word list")
# TODO: Implement hard mode properly (more than just a *)

# Parse the args
args = parser.parse_args()

# Handle the args
#   Select the correct word list
if args.classic:
   import w
else:
   import w2 as w

#   Get today's day number
if args.day is not None:
   # Ahoy-hoy, time traveller!
   d = args.day
else:
   # find num. days since Wordle launch
   d = (date.today() - date(2021, 6, 19)).days

#   l is for "Find this word in the answers list"
if args.l:
   l = args.l.lower()
   # Look up the answer's index
   if l in w.Answers and w.Answers.index(l) < d:
      print("Wordle {}: {}".format(w.Answers.index(l), l))
   else:
      print("{} is not a Wordle (yet?)".format(args.l))
   exit(0)

#   d is for "Find this day's answer"
if args.d != None:
   # Look up the answer
   if args.d < len(w.Answers):
      print(w.Answers[args.d])
   else:
      print("No Solution")
   exit(0)


def wordbox(word):

   #   Colors!
   #        gray bg    yellow bg  green bg   white fg  black bg
   COLORS = [0x13a3a3c, 0x1b59f3b, 0x1538d4e, 0xd7dadc, 0x1121213]


   output = ""
   line = [0] * len(word)
   guess = list(word)
   solution = list(w.Answers[d])
   # Green pass
   for i in range(len(word)):
      if guess[i] == solution[i]:
         # Mark the letter 'green' (2)
         line[i] = 2
         # Remove letter from solution and guess
         solution[i] = guess[i] = 0
   # Yellow pass
   for i in range(len(word)):
      if guess[i] and word[i] in solution:
         # Mark the letter 'yellow' (1)
         line[i] = 1
         # Remove letter from solution and guess
         solution[solution.index(word[i])] = guess[i] = 0
   # Turn blocks into a string, and print it
   # Move up to replace the input box
   for i in range(len(word)):
      output += f"{c.c24(COLORS[3])}{c.c24(COLORS[line[i]])} {word[i].upper()} {c.RESET}"
   return output

if not args.word:
   print(f"Wordle {d}:")
   print(f"Today is {date(2021, 6, 19) + timedelta(days=d)}")
   args.word = "crane"
print(f"Hint: {wordbox(args.word)}")
