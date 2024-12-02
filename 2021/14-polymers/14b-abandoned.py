#! /usr/local/bin/python3
filename = "input-1588"
# filename = "input-2x40"
# filename = "input"

from collections import Counter
import re

# debug = False
debug = True

max_days = 10

import math
def log(m):
  if debug: print(m)

class Rule:
  def __init__(self, target, insert):
    # log(f"Rule.init({name})")
    self.target = target
    self.insert = insert
    self.new_pairs = Counter(''.join())
    # self.replace = "{target[0,-2]}{insert}" # Don't include target[1]...the next match will get it.
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
    self.pairs = Counter()
    self.init_pairs
    self.foresites = {}
    self.foresites_init()
    self.dump()

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
    log(f'counts: {self.pairs} ')

  def summary(self):
    return f"Board {self.filename}:"

  def init_pairs(self):
    word = f"{self.word}$" # '$' to protect last character
    for i in range(len(word)-1):
      self.pairs += self.word[i:i+2]

  def advance(self):
    log(f"================================== advance from day {self.today}:")
    self.today += 1
    # print(f"{self.today}:  PRE: {self.word}")

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

    # next_word.append(self.word[-1])
    # self.word = ''.join(next_word)
    # print(f"{self.today}: POST: {len(self.word)}  {self.word}")

  def score(self):
    log(self.pairs)
    max = self.pairs.most_common()[0][1]
    min = self.pairs.most_common()[-1][1]
    return max - min

def main():
  board = Board(filename)
  board.dump()

  print(f"0: POST: {len(board.word)}  {board.word}")

  for day in range(max_days):
    board.advance()

  score = board.score()
  print(f"\nScore: {score}")

  target = int(filename.split('-')[-1])
  assert score == target, f"NOPE! the score should be {target}, not {score}"

main()

