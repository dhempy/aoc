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
    self.total_risk = 0
    self.map = self.slurp()
    # self.map[0][0] = '0'  # first hit is free.
    self.rows = len(self.map)
    self.cols = len(self.map[0])
    self.seen = numpy.full((self.rows, self.cols), 0, dtype=int)
    self.safest = sys.maxsize
    self.safest_to_here = numpy.full((self.rows, self.cols), sys.maxsize, dtype=int)

  def slurp(self):
    return numpy.loadtxt(self.filename, dtype = str)

  def find_safest_path(self):
    changed = True
    while changed:
      time_log(f'study all risks. Final risk is currently {self.safest_to_here[-1][-1]}', True)
      changed = False
      for r, row in enumerate(self.map):
        time_log(f' study row {r}.')
        for c, cell in enumerate(row):
          if r == 0 and c == 0:
            cell = '0'
            prev_risk = 0
          else:
            prev_risk = self.safest_neighbor(r,c)
          new_risk = int(cell) + prev_risk
          log(f'({r},{c}) is {cell} + {prev_risk} => {new_risk} ')
          # log(f'Test changed will be: {new_risk < self.safest_to_here[r][c]} ')
          if new_risk < self.safest_to_here[r][c]:
            changed or log('SETTING changed to TRUE')
            changed = True
            self.safest_to_here[r][c] = new_risk
      self.dump()
      log(f'At end of while loop, changed is {changed}', True)

    final_risk = self.safest_to_here[-1][-1]
    time_log(f'\nFINISHED studying all risks. Final risk is {final_risk}', True)
    return final_risk

  def risk_at(self, r, c):
    if r < 0 or c < 0 or r >= self.rows or c >= self.cols:
      return sys.maxsize

    risk = self.safest_to_here[r][c]
    # if risk == sys.maxsize:
      # risk = int(self.map[r][c])
    return risk

  def safest_neighbor(self, r, c):
    return min([ self.risk_at(r+1, c), self.risk_at(r, c+1), self.risk_at(r, c-1), self.risk_at(r-1, c)])

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

