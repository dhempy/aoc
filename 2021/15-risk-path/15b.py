# filename = "inputb-8"
# filename = "input-hook"
# filename = "input-40"
# filename = "input-13"
# filename = "input-315"
filename = "input-full"
# filename = "input-janine"

debug = False
# debug = True

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
    self.expand(5)
    self.rows = len(self.map)
    self.cols = len(self.map[0])
    self.seen = np.full((self.rows, self.cols), 0, dtype=int)
    self.safest = sys.maxsize
    self.safest_to_here = np.full((self.rows, self.cols), sys.maxsize, dtype=int)

  def slurp(self):
    print(f'\nslurp file: {self.filename} ')
    a = np.genfromtxt(self.filename, delimiter=1, dtype=int)
    print(np.matrix(a))
    return a

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

  def expand(self, factor):
    last_board = self.map
    stack = self.map.copy()
    src_rows = self.map.shape[0]
    src_cols = self.map.shape[1]

    for x in range(factor*2):
      new_board = last_board.copy()
      new_board = new_board % 9 + 1
      log(f"new_board: \n{np.matrix(new_board)}")
      stack = np.vstack((stack, new_board))
      log(f"stack: \n{np.matrix(stack)}")
      last_board = new_board

    log(f"stack: \n{np.matrix(stack)}")

    big_board = np.empty((factor*src_rows, 0)).reshape(src_rows*factor, 0)
    # log(f"big_board: (PRE)\n{np.matrix(big_board)}")
    for x in range(factor):
      new_col = stack[x*src_rows:(x+factor)*src_rows, 0:src_cols]
      # log(f"new_col: \n{np.matrix(new_col)}")
      big_board = np.hstack((big_board, new_col))
      # log(f"big_board: \n{np.matrix(big_board)}")

    self.map = big_board
    # print(f"big_board (FINALLY): \n{np.matrix(self.map)}")


  def dump(self):
    log('')
    log(f'Board: cols:{self.cols} rows:{self.rows}')
    log("map:")
    print(np.matrix(self.map))
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

