#! /usr/local/bin/python3
# filename = "input-15"
filename = "input-solo"
# filename = "input"

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
    self.map = self.slurp()
    self.rows = len(self.map)
    self.cols = len(self.map[0])
    self.dump()

  def slurp(self):
    # self.lines = open(self.filename).read().split()
    return numpy.loadtxt(self.filename, dtype = numpy.str)

  def find_lows(self):
    for x in range(self.rows):
      for y in range(self.cols):
        self.test_for_low(x, y)

  def test_for_low(self, x, y):
    this_cell = self.map[x][y]
    log(f'test_for_low {x},{y} => {this_cell} ')

    for delta_x in range(-1,2):
      for delta_y in range(-1,2):
        if (delta_x != 0 or delta_x != 0):
          row = y + delta_y
          col = x + delta_x
          if row >= 0 and col >= 0 and row < self.rows and col < self.cols:
            that_cell = self.map[row][col]
            log(f'             {row},{col} => {that_cell} ')

            if this_cell >= that_cell:
              log(f'             NOPE!')
              return 0
    # no neighbors were greater....
    log(f'LOW SPOT at {x},{y} => {this_cell} ')



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
  lows = board.find_lows()
  answer = 123
  log(f"Total score: {answer} ")


  target = int(filename.split('-')[-1])
  assert answer == target, f"NOPE! the answer should be {target}, not {answer}"

main()

