#! /usr/local/bin/python3
# filename = "input-solo-error"
# filename = "input-26397"
filename = "input"

max_size = 1310

import re
# debug = False
debug = True


max_days = 1000

import math
import numpy

def log(m):
  if debug: print(m)


class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    self.lines = []
    self.stack = []
    self.slurp()
    self.dump()

  def slurp(self):
    self.lines = open(self.filename).read().split()

  def compile(self):
    score = 0
    for line in self.lines:
      points = self.parse_line(line)
      log(f"  line score: {points} ")
      score += points

    return score

  def parse_line(self, line):
    log('parse_line')
    log(line)
    for c in line:
      # log(c)
      points = 0
      if c in '({[<':
        self.stack.append(c)
      elif c == ')':
        if self.stack.pop() != '(':
          return 3
      elif c == ']':
        if self.stack.pop() != '[':
          return 57
      elif c == '}':
        if self.stack.pop() != '{':
          return 1197
      elif c == '>':
        if self.stack.pop() != '<':
          return 25137

    return 0



  def dump(self):
    log('')
    log(self.summary())
    log(self.lines[0])
    log('(etc)\n')

  def summary(self):
    return f"Board {self.filename}: lines:{len(self.lines)}"

def main():
  board = Board(filename)
  answer = board.compile()
  log(f"Total score: {answer} ")


  target = int(filename.split('-')[-1])
  assert answer == target, f"NOPE! the answer should be {target}, not {answer}"

main()

