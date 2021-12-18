#! /usr/local/bin/python3
# filename = "inputb-8"
# filename = "input-hook"
# filename = "input-40"
filename = "input-full"
# filename = "input-janine"

debug = False
# debug = True

import math
import numpy
import json
import sys
import jsbeautifier
import os
import time

time_start = time.time()
last_start = time_start

numpy.set_printoptions(linewidth=400)

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
    self.map = self.slurp()

  def slurp(self):
    return numpy.loadtxt(self.filename, dtype = str)

  def dump(self):
    log('')
    log(f'Board: cols:{self.cols} rows:{self.rows}')
    log("map:")
    for row in self.map:
      log(row)
    # log("seen:")
    # for row in self.seen:
    #   log(row)
    log("safest_to_here:")
    for row in self.safest_to_here:
      log(row)
    log('')

  def summary(self):
    return f"Board {self.filename}: lines:{len(self.lines)}"

def main():
  board = Board(filename)
  board.dump()

  answer = board.find_safest_path()

  print(f"answer: {answer} \a")

  try:
    target = int(filename.split('-')[-1])
    assert answer == target, f"NOPE! the answer should be {target}, not {answer}"
  except Exception:
    'Ok'

main()

