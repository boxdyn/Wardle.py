import w
import argparse
import sys
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
# Get today's day number
if args.day is not None:
  # Ahoy-hoy, time traveller!
  d = args.day
else:
  # find num. days since Wordle launch
  d = (date.today() - date(2021, 6, 19)).days

# l is for "Find this word in the answers list"
if args.l:
  l = args.l.lower()
  # Look up the answer's index
  if l in w.Answers and w.Answers.index(l) < d:
    print ("Wordle {}: {}".format(w.Answers.index(l), l))
  else:
    print ("{} is not a Wordle (yet?)".format(args.l))
  exit(0)

# d is for "Find this day's answer"
if args.d != None:
  # Look up the answer
  if args.d < len(w.Answers):
    print (w.Answers[args.d])
  else:
    print ("No Solution")
  exit(0)

# g is for "maximum guesses"
if args.g:
  max_guesses = abs(args.g)
else:
  max_guesses = 6

# Get today's word
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

# Guesses go here
guesses = []

def wordbox(word):
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
  for i in line:
    output += boxes[i]
  print(output)

def game():
  print("[   Wordle {}{}  ]".format(d, "*" if args.hard else " "))
  words = w.Words + w.Answers
  guess = 0
  while guess < max_guesses:
    ui = input().lower()
    if len(ui) == 5 and (ui in words or args.nonsense):
      guesses.append(ui)
      wordbox(ui)
      if (ui == solution):
        win(True)
        return
      else:
        guess += 1
    else:
      if ui == "exit":
        exit()
      print ("Not in word list")
  win(False)

def win(won):
  print("\nWordle {} {}/{}{}\n".format(d, len(guesses) if won else "X", max_guesses, "*" if args.hard else ""))
  for gi in guesses:
    wordbox(gi)
  print()

game()