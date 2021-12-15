#! /usr/local/bin/python3
# filename = "input-1588"
# filename = "input"
filename = "input-2x40"
# filename = "input-tiny"

from collections import Counter
import re

debug = False
# debug = True

max_days = 40
study_days = 10

import math
def log(m):
  if debug: print(m)

class Rule:
  def __init__(self, target, insert):
    # log(f"Rule.init({target}, {insert})")
    self.target = target
    self.insert = insert
    # self.replace = "{target[0,-2]}{insert}" # Don't include target[1]...the next match will get it.
    # self.dump()

  def dump(self):
    log(self.summary())

  def summary(self):
    return f" {self.target} gets {self.insert}"


class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    self.today = 0
    self.slurp()
    self.foresites = {}
    self.foresites_init()

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

  def foresites_init(self):
    for rule in self.rules:
      self.foresites[rule.target] = [f"{rule.target[0]}{rule.insert}{rule.target[1]}"]

  def dump(self):
    log(self.summary())
    for rule in self.rules:
      rule.dump()
    if max_days > 5:
      log(f'foresites: {self.foresites} ')
    else:
      print(f'foresites: {self.foresites} ')

  def summary(self):
    return f"Board {self.filename}:"

  def build_foresite(self):
    log(f"build_foresite()...")
    for key, futures in self.foresites.items():
      self.study_pair(key, futures)
    self.dump()

  def study_pair(self, key, futures):
    log(f" build_foresite():  {key} -> {futures}")
    word = futures[-1]
    nextgen = self.advance_word(word)
    log(f" build_foresite(): Add {word}")
    futures.append(nextgen)
    # self.foresites[word].append(nextgen)

  def advance_word(self, word):
    log(f"  advance word {word}...")
    next_word = []
    # print(f"{self.today}:  PRE: {self.word}")

    for i in range(len(word)-1):
      pair = word[i:i+2]
      # log(f' pair: {pair}')
      # log(f' append frst {pair[0]} ')
      next_word.append(pair[0])
      for rule in self.rules:
        if pair == rule.target:
          log(f'    {rule.target} -> {rule.insert}')
          next_word.append(rule.insert)
          break

    next_word.append(word[-1])
    new_word = ''.join(next_word)
    # print(f"  POST: {len(new_word)}  {new_word}")
    return new_word

  def score(self):
    elements = Counter(self.word)
    log(elements)
    max = elements.most_common()[0][1]
    min = elements.most_common()[-1][1]
    return max - min

  def advance_pairs(self, old_word, max_days):
    # print(f"++++++ advance {old_word} by {max_days} days ...")
    next_word = []
    last_dangling = False
    # log(f"{self.today}:  PRE: {self.word}")

    for i in range(len(old_word)-1):
      pair = old_word[i:i+2]
      if pair in self.foresites:
        log(f" foresite[{pair}]: {self.foresites[pair]} ")
        next_word.append(self.foresites[pair][max_days-1])
        last_dangling = False
      else:
        next_word.append(pair[0])
        last_dangling = True
        # raise ValueError(f'pair not foreseen: {pair} ')

    if last_dangling:
      next_word.append(old_word[-1])

    new_word = ''.join(next_word)
    # print(f"{max_days} days later: {new_word}")
    return new_word

  def score_pairs(self, word):
    elements = Counter(word)
    log(elements)
    max = elements.most_common()[0][1]
    min = elements.most_common()[-1][1]
    return max - min

def main():
  board = Board(filename)
  for n in range(study_days):
    board.build_foresite()
  board.dump()

  # print(f'FINALLY: foresites: {board.foresites} ')

  # print(f"0: POST: {len(board.word)}  {board.word}")
  # board.advance_pairs(max_days)

  # for day in range(max_days):
  print(board.advance_pairs(board.word, 1))
  print(board.advance_pairs(board.word, 2))
  print(board.advance_pairs(board.word, 3))
  print(board.advance_pairs(board.word, 4))
  print(board.advance_pairs(board.word, 5))
  print(board.advance_pairs(board.word, 6))
  print(board.advance_pairs(board.word, 7))
  print(board.advance_pairs(board.word, 8))
  print(board.advance_pairs(board.word, 9))
  print(board.advance_pairs(board.word, 10))

  final_word = board.word
  print(" 5 days...")
  final_word = board.advance_pairs(final_word, 5)
  print("10 days...")
  final_word = board.advance_pairs(final_word, 5)
  print("15 days...")
  final_word = board.advance_pairs(final_word, 5)
  print("20 days...")
  final_word = board.advance_pairs(final_word, 5)
  print("25 days...")
  final_word = board.advance_pairs(final_word, 5)
  print("30 days...")
  final_word = board.advance_pairs(final_word, 5)
  print("35 days...")
  final_word = board.advance_pairs(final_word, 5)
  print("40 days...")
  final_word = board.advance_pairs(final_word, 5)
  print("DONE!")
  print(f"word len: {len(final_word)}")

  score = board.score_pairs(final_word)
  print(f"\nScore: {score}")
  # target = int(filename.split('-')[-1])
  # assert score == target, f"NOPE! the score should be {target}, not {score}"

main()

