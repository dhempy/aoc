#! /usr/local/bin/python3
# filename = "input-1588"
# filename = "input-2188189693529"
# filename = "input-2x40"
# filename = "input-8x5"
filename = "input"

from collections import Counter
import re

debug = False
# debug = True

max_days = 40

import math
def log(m):
  if debug: print(m)

class Rule:
  def __init__(self, target, insert):
    # log(f"Rule.init({name})")
    self.target = target
    self.insert = insert
    new_chars = [target[0], insert, target[1]]
    log(f"rule.new_chars: {new_chars}")
    self.new_pairs = [''.join(new_chars[0:2]), ''.join(new_chars[1:3])]
    log(f"rule.pairs: {self.new_pairs}")

  # def new_pairs(self, qty):
  #   return Counter({self.pairs[0]: qty, self.pairs[1]: qty})

  def dump(self):
    log(self.summary())

  def summary(self):
    return f" {self.target} spawns {self.new_pairs}"



class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    self.today = 0
    self.slurp()
    self.pairs = Counter()
    self.init_pairs()
    self.dump()

  def slurp(self):
    file = open(self.filename)

    self.word = file.readline().rstrip()
    log(f'STARTING WORD: {self.word}')
    file.readline()

    self.rules = []
    for line in file:
      log(line)
      target, insert = line.rstrip().split(' -> ')
      self.rules.append(Rule(target, insert))

  def dump(self):
    log('')
    log(self.summary())
    for rule in self.rules:
      rule.dump()
    log(f'counts: {self.pairs} ')
    log('')

  def summary(self):
    return f"Board {self.filename}:"

  def init_pairs(self):
    log('\ninit_pairs()...')
    word = f"{self.word}$" # '$' to protect last character
    log(f'word:{word}')
    for i in range(len(word)-1):
      pair = word[i:i+2]
      self.pairs[pair] += 1

    log(f'self.pairs:{self.pairs}')

  def find_rule(self, pair):
    matches = [rule for rule in self.rules if rule.target == pair]
    if matches:
      return matches[0]
    return False

  def advance_pair(self, old_pair, qty):
    log(f' advance_pair({old_pair}, {qty})... old_pair is {type(old_pair)}')
    rule = self.find_rule(old_pair)
    if not rule:
      log('  preserve')
      return
    rule.dump()

    log(f'  self.pairs: {self.pairs}')
    for new_pair in rule.new_pairs:
      log(f'   increment {new_pair} by {qty}')
      self.pairs[new_pair] += qty

    log(f'  self.pairs: {self.pairs}')
    log(f'   decrement {old_pair} by {qty}')
    self.pairs[old_pair] -= qty
    log(f'  self.pairs: {self.pairs}')

  def advance(self):
    log(f"================================== advance from day {self.today}:")
    self.today += 1
    # print(f"{self.today}:  PRE: {self.word}")

    new_pairs = Counter()
    for pair, count in self.pairs.most_common():
      self.advance_pair(pair, count)

  def score(self):
    print('\nscore():')
    print(self.pairs)
    letters = Counter()
    for pair, qty in self.pairs.most_common():
      letters[pair[0]] += qty
    print(letters)
    max = letters.most_common()[0]
    min = letters.most_common()[-1]
    score = max[1] - min[1]
    print(f' {max} - {min} => {score}')
    return score

def main():
  board = Board(filename)

  print(f"0: POST: {len(board.word)}  {board.word}")

  for day in range(max_days):
    board.advance()

  score = board.score()
  print(f"\nScore: {score}")

  target = int(filename.split('-')[-1])
  assert score == target, f"NOPE! the score should be {target}, not {score}"

main()

