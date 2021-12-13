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
    error_score = 0
    fix_scores = []

    for line in self.lines:
      points = self.parse_line(line)
      error_score += points
      if points > 0:
        pass
        # log(f"  error score: {points} ")
        # self.lines.remove(line)
      else:
        log(f'fix:{line} ')
        points = self.fix()
        log(f"  fix   score: {points} ")
        fix_scores.append(points)

    log(fix_scores)
    log(sorted(fix_scores))
    i = int((len(fix_scores) - 1)/2)
    log(i)
    mid_score = sorted(fix_scores)[i]
    log(mid_score)

    return error_score, mid_score

  def parse_line(self, line):
    # log(f'parse_line:{line} ')
    self.stack.clear()
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


  def fix(self):
    points = 0
    while self.stack:
      c = self.stack.pop()
      if c == '(':
        log(')')
        points = points * 5 + 1
      elif c == '[':
        log(']')
        points = points * 5 + 2
      elif c == '{':
        log("}")
        points = points * 5 + 3
      elif c == '<':
        log('>')
        points = points * 5 + 4
      # log(f"fixed {c}: points = {points} ")

    return points



  def dump(self):
    log('')
    log(self.summary())
    log(self.lines[0])
    log('(etc)\n')

  def summary(self):
    return f"Board {self.filename}: lines:{len(self.lines)}"

def main():
  board = Board(filename)
  log(f"========== Before compile, there are {len(board.lines)} lines.")
  error_score, fix_score = board.compile()
  log(f"========== After  compile, there are {len(board.lines)} lines.")
  log(f"error score: {error_score} ")
  log(f"  fix score: {fix_score} ")
  answer = fix_score


  target = int(filename.split('-')[-1])
  assert answer == target, f"NOPE! the answer should be {target}, not {answer}"

main()

