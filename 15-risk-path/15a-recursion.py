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

  def study(self):
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



  # recursive solution: (SLOW!!!)
  def find_safest_path(self, r=0, c=0, max_r=False, max_c=False, risk='init'):
    max_r = max_r or self.rows
    max_c = max_c or self.cols

    if c >= max_c or r >= max_r or c < 0 or r < 0:
      # log(f'  {r},{c} out of bounds!')
      return sys.maxsize
    log(f'{r},{c} ({self.safest_to_here[r][c]})')

    if self.seen[r][c]:
      # log(f'  seen.')
      return sys.maxsize

    try:
      this_cell = int(self.map[r][c])
      self.seen[r][c] = this_cell

      if risk == 'init':  # Don't count the origin cell
        new_risk = risk = 0
      else:
        new_risk = risk + this_cell
      # log(f'path from {r},{c} ({this_cell}) with risk {risk}+{this_cell} => {new_risk} will compare with safest {self.safest}...')

      if new_risk > self.safest_to_here[r][c]:
        # This is probably not legit.
        # Perhaps an expensive early path allows for a cheaper later path?
        log(f'  {new_risk} exceeds safest subrisk.')
        return sys.maxsize

      self.safest_to_here[r][c] = new_risk
      log(f' new safest subpath to {r},{c}: {new_risk}')

      if new_risk >= self.safest:
        # log(f'  safest risk exceeded!')
        return sys.maxsize
      log(f'path from {r},{c} with risk {risk} + {this_cell} => {new_risk} is LESS THAN {self.safest}')

      steps_left = (self.rows - r) + (self.cols - c)
      if r == self.rows-1 and c == self.cols-1:
        self.new_solution(new_risk)
        return new_risk

      self.find_safest_path(r+1,   c, max_r, max_c, new_risk)
      self.find_safest_path(r,   c+1, max_r, max_c, new_risk)
      self.find_safest_path(r-1,   c, max_r, max_c, new_risk)
      self.find_safest_path(r,   c-1, max_r, max_c, new_risk)

      return self.safest

    finally:
      self.seen[r][c] = False

  def new_solution(self, risk):
    global time_start
    elapsed = int(time.time() - time_start)
    print(f'  ^^ NEW SOLUTION: {risk} {elapsed}s')
    self.safest = risk
    self.save_wip() # For restarts, and part B of the problem!


  def dump(self, force=False):
    # global debug
    # debug_was = debug
    # if force:
    #   debug = True

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
    # debug = debug_was

  def summary(self):
    return f"Board {self.filename}: lines:{len(self.lines)}"

def main():
  board = Board(filename)
  board.dump()

  answer = board.study()
  answer = board.find_safest_path()

  print(f"answer: {answer} \a")

  try:
    target = int(filename.split('-')[-1])
    assert answer == target, f"NOPE! the answer should be {target}, not {answer}"
  except Exception:
    'Ok'

main()

