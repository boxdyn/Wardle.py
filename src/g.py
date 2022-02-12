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
parser.add_argument('--hard', action='store_true',           help="enable hard mode")
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
    print ("{} is not a Wordle (yet)".format(args.l))
  exit(0)

# d is for "Find this day's answer"
if args.d != None:
  # Look up the answer
  if args.d < len(w.Answers):
    print (w.Answers[args.d])
  else:
    print ("No Solution")
  exit(0)

if args.g:
  max_guesses = args.g
else:
  max_guesses = 6

# Get today's word
wotd = w.Answers[d]

# Box characters!
a = ["⬛", "🟨", "🟩"]

# Guesses go here
g = []

# Hits/Misses go here
h = ""
m = ""

#        C  R  A  N  E
hints = [0, 0, 0, 0, 0]

def wordbox(word):
  b = ""
  global h, m
  wordlist = list(wotd)
  for i in range(len(word)):
    if word[i] == wotd[i]:
      # Mark as hinted (right place)
      hints[i] = 2
      # Remove letter from wordlist
      wordlist[i] = 0
      # add "🟩" to line
      b += a[2]
      # Mark the hit
      h += word[i]
    elif word[i] in wordlist:
      # Mark as hinted (wrong place)
      hints[wordlist.index(word[i])]= 1
      # Remove letter from wordlist
      wordlist[wordlist.index(word[i])] = 0
      # Add "🟨" to line
      b += a[1]
      # Mark the hit
      h += word[i]
    else:
      # Add "⬛" to line
      b += a[0]
      m +=word[i]
  print(b)

def game():
  print("[   Wordle {}{}  ]".format(d, "*" if args.hard else " "))
  words = w.Words + w.Answers
  guess = 0
  while guess < max_guesses:
    ui = input().lower()
    if len(ui) == 5 and ui in words:
      g.append(ui)
      wordbox(ui)
      if (ui == wotd):
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
  print("\nWordle {} {}/{}{}\n".format(d, len(g) if won else "X", max_guesses, "*" if args.hard else ""))
  for gi in g:
    wordbox(gi)

game()