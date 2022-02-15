"""
Copyright(c) 2022 SoftFish

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and / or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import w
import c
import argparse
from datetime import date

# Set up argument parser
parser = argparse.ArgumentParser(
  description='A barebones CLI Wordle clone, using official Wardle solutions. Also a Wordle cheating tool. You have been warned.'
  )
parser.add_argument('day',    nargs="?",           type=int, help="Wordle day number")
parser.add_argument('-l',     metavar="solution",            help="look up the day of a given solution")
parser.add_argument('-d',     metavar="day",       type=int, help="look up the solution of a given day")
parser.add_argument('-g',     metavar="guesses",   type=int, help="number of guesses")
parser.add_argument('--word', metavar="wotd",                help="force a particular word")
parser.add_argument('--nonsense', action='store_true',       help="allow nonsensical guesses")
parser.add_argument('--hard',     action='store_true',       help="enable hard mode (wip)")
# TODO: Implement hard mode properly (more than just a *)

# Parse the args
args = parser.parse_args()

# Handle the args
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
    print ("Wordle {}: {}".format(w.Answers.index(l), l))
  else:
    print ("{} is not a Wordle (yet?)".format(args.l))
  exit(0)

#   d is for "Find this day's answer"
if args.d != None:
  # Look up the answer
  if args.d < len(w.Answers):
    print (w.Answers[args.d])
  else:
    print ("No Solution")
  exit(0)

#   g is for "maximum guesses"
if args.g:
  max_guesses = abs(args.g)
else:
  max_guesses = 6

#   Get today's word
if args.word:
  solution = args.word
  # Indicate a non-standard word
  d = args.word
  # If solution not in words list, enable nonsense
  if solution not in w.Words + w.Answers:
    args.nonsense = True
else:
  if d >= len(w.Answers):
    d = len(w.Answers) - 1
  solution = w.Answers[d]
# End arg parsing

# ! The game is below this point

# Box characters!
boxes = ["⬛", "🟨", "🟩"]
#        gray bg    yellow bg  green bg   white fg  black bg
colors= [0x13a3a3c, 0x1b59f3b, 0x1538d4e, 0xd7dadc, 0x1121213]

# Guesses go here
guesses = []

# Letter is in boxes
def wordbox(word, showword = 0):
  output = ""
  line = [0] * len(word)
  guess = list(word)
  sol   = list(solution)
  # Green pass
  for i in range(len(word)):
    if guess[i] == sol[i]:
      # Mark the letter 'green' (2)
      line[i] = 2
      # Remove letter from solution and guess
      sol[i] = guess[i] = 0
  # Yellow pass
  for i in range(len(word)):
    if guess[i] and word[i] in sol:
      # Mark the letter 'yellow' (1)
      line[i] = 1
      # Remove letter from solution and guess
      sol[sol.index(word[i])] = guess[i] = 0
  # Turn blocks into a string, and print it
  if showword:
    for i in range(len(word)):
      #output += c.c(7,0,1) + (c.c(2,1) if line[i] == 2 else c.c(3,1) if line[i] == 1 else c.c(0,1,1)) + word[i].upper() + " " + c.reset
      output += c.c24(colors[3]) + c.c24(colors[line[i]]) + " " + word[i].upper() + " " + c.reset
  else:
    for i in line:
      #output += c.c(7, 0, 1) + (c.c(2, 1) if i == 2 else c.c(3, 1) if i == 1 else c.c(0, 1, 1)) + boxes[i] + c.reset
      output += c.c24(colors[3]) + c.c24(colors[i]) + boxes[i] + c.reset
  print(output)

def game():
  spaces = " " * (2-(len(str(d))//2))
  print(c.reset + "[ " + spaces + "Wordle {}{}".format(d, "*" if args.hard else " ") + spaces + "]")
  words = w.Words + w.Answers
  guess = 0
  while guess < max_guesses:
    # lol i should probably use curses
    user_input = input("    [     ]\b\b\b\b\b\b").lower()
    if len(user_input) == 5 and (user_input in words or args.nonsense):
      # Add guesses to the guessed list, and put the word in boxes
      guesses.append(user_input)
      wordbox(user_input, 1)
      # win condition
      if (user_input == solution):
        win(True)
        return
      else:
        guess += 1
    else:
      # Allow the user to make it stop
      if user_input == "exit":
        exit()
      print ("Not in word list")
  # lose
  win(False)

def win(won):
  print("\nWordle {} {}/{}{}\n".format(d, len(guesses) if won else "X", max_guesses, "*" if args.hard else ""))
  for gi in guesses:
    wordbox(gi)
  print()

game()