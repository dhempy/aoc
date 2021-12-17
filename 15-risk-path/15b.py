#! /usr/local/bin/python3

# This program multiples an existing board into a 5x5 version of that board, with modifications.
# filename = "inputb-8"
# filename = "input-hook"
filename = "input-40"
# filename = "input-full"
# filename = "input-janine"

# debug = False
debug = True

import math
import numpy as np
import json
import sys
import jsbeautifier
import os
import time

time_start = time.time()
last_start = time_start

np.set_printoptions(linewidth=400)

def time_log(m, force=False):
  global time_start, last_start
  now = time.time()
  total_elapsed = int(now - time_start)
  elapsed = int(now - last_start)
  last_start = now
  log (f"{m} (+{elapsed}s => {total_elapsed}s)", force)

def log(m, force=False):
  if debug or force: print(m)

class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    self.total_risk = 0
    self.map = self.slurp()
    print(f'self.map => {self.map} ')
    print(self.map)
    print(f'self.map[0] => {self.map[0]} ')
    print(f'type(self.map[0]) => {type(self.map[0])} ')
    print(f'self.map[0][0] => {self.map[0][0]} ')
    print(f'10*self.map[0][0] => {10*self.map[0][0]} ')
    # self.map[0][0] = '0'  # first hit is free.
    self.rows = len(self.map)
    self.cols = len(self.map[0])
    self.safest = sys.maxsize # total risk of the safest complete path.
    self.safest_to_here = np.full((self.rows, self.cols), sys.maxsize, dtype=int)
    self.dump()
    exit()

  def slurp(self):
    # return np.loadtxt(self.filename, delimiter=1, dtype=int)
    # return numpy.loadtxt(self.filename, delimiter=1, dtype=int)
    # return np.loadtxt(self.filename, delimiter=1, dtype=int)

    a = np.loadtxt(self.filename, dtype=np.character)
    print(a)
    a = np.array(map(lambda x: map(int, x), a))
    print(a)
    return a

  def dump(self):
    log('')
    log(f'Board: cols:{self.cols} rows:{self.rows}')
    log("map:")
    for row in self.map:
      log(row)
    log("safest_to_here:")
    for row in self.safest_to_here:
      log(row)
    log('')

  def summary(self):
    return f"Board {self.filename}: lines:{len(self.lines)}"

  def expand(self, size)
    print("TODO: expand map by {size}")

def main():
  board = Board(filename)
  board.dump()

  answer = board.expand(5)

  print(f"answer: {answer} \a")

  try:
    target = int(filename.split('-')[-1])
    assert answer == target, f"NOPE! the answer should be {target}, not {answer}"
  except Exception:
    pass

main()

