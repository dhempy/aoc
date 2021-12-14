#! /usr/local/bin/python3
filename = "input-1588"
# filename = "input"

from collections import Counter
import re

# debug = False
debug = True

max_days = 3

import math
def log(m):
  if debug: print(m)

class Rule:
  def __init__(self, target, insert):
    # log(f"Rule.init({name})")
    self.target = target
    self.insert = insert
    # self.dump()

  def dump(self):
    log(self.summary())

  def summary(self):
    f" {self.target} gets {self.insert}"


class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    self.today = 0
    self.slurp()
    # self.dump()

  def slurp(self):
    file = open(self.filename)

    self.word = file.readline().rstrip()
    log(f'STARTING WORD: {self.word}')
    file.readline()

    self.rules = []
    for line in file:
      target, insert = line.rstrip().split(' -> ')
      self.rules.append(Rule(target, insert))

  def dump(self):
    log(self.summary())
    for rule in self.rules:
      rule.dump()

  def summary(self):
    return f"Board {self.filename}:"

  def advance(self):
    log(f"================================== advance from day {self.today}:")
    self.today += 1
    next_word = []
    print(f"{self.today}:  PRE: {self.word}")

    for i in range(len(self.word)-1):
      pair = self.word[i:i+2]
      # log(f' pair: {pair}')
      # log(f' append frst {pair[0]} ')
      next_word.append(pair[0])
      for rule in self.rules:
        if pair == rule.target:
          log(f'    {rule.target} -> {rule.insert}')
          next_word.append(rule.insert)
          break

    next_word.append(self.word[-1])
    self.word = ''.join(next_word)
    print(f"{self.today}: POST: {self.word}")

def main():
  board = Board(filename)

  for day in range(max_days):
    board.advance()

  score = board.score()
  print(f"\nScore: {score}")

  target = int(filename.split('-')[-1])
  assert score == target, f"NOPE! the score should be {target}, not {score}"

main()

