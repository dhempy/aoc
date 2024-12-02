#! /usr/local/bin/python3
# filename = "input-15"
# filename = "input-13"
filename = "input"

debug = False
debug = True

import math
import numpy

def log(m):
  if debug: print(m)


class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    self.total_risk = 0
    self.map = self.slurp()
    self.rows = len(self.map)
    self.cols = len(self.map[0])
    self.dump()

  def slurp(self):
    # self.lines = open(self.filename).read().split()
    return numpy.loadtxt(self.filename, dtype = numpy.str)

  def find_lows(self):
    for r in range(self.rows):
      for c in range(self.cols):
        self.test_for_low(r, c)

  def test_for_low(self, r, c):
    this_cell = self.map[r][c]
    # log(f'test_for_low {r},{c} => {this_cell} ')

    for delta_r in range(-1,2):
      for delta_c in range(-1,2):
        if (delta_r != 0 or delta_c != 0):
          row = r + delta_r
          col = c + delta_c
          if row >= 0 and col >= 0 and row < self.rows and col < self.cols:
            that_cell = self.map[row][col]
            # log(f'             {row},{col} => {that_cell} ')

            if this_cell >= that_cell:
              # log(f'             NOPE!')
              return 0
    # no neighbors were greater....
    log(f'LOW SPOT at {r},{c} => {this_cell} ')
    risk = int(this_cell) + 1
    self.total_risk += risk



  def dump(self):
    log('')
    log(f'Map: cols:{self.cols} rows:{self.rows}')
    for row in self.map:
      log(row)
    log('')

  def summary(self):
    return f"Board {self.filename}: lines:{len(self.lines)}"

def main():
  board = Board(filename)
  # answer = board.compile()
  board.find_lows()
  answer = board.total_risk
  log(f"Total risk: {answer} ")


  target = int(filename.split('-')[-1])
  assert answer == target, f"NOPE! the answer should be {target}, not {answer}"

main()

