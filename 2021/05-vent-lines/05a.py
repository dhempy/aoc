#! /usr/local/bin/python3
# filename = "inputb-8"
# filename = "inputb-1134"
filename = "input"

debug = False
debug = True

import math
import numpy

def log(m):
  if debug: print(m)

class Line:
  def __init__(self, x1, y1, x2, y2)
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2

  def dump():
    log(f'  ({x1},{y1}) -> ({x2},{y2})')

class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    self.slurp()
    self.rows = len(self.lines)
    self.cols = len(self.lines[0])

    self.basins = []
    self.dump()

  def slurp(self):
    self.lines = []

    for line in open(self.filename).read().split():
      (p1, p2) = line.split(' -> ')
      (x1, y1) = p1.split(',')
      (x2, y2) = p2.split(',')
      self.lines.append(Line(x1, y1, x2, y2))

  def find_lows(self):
    for r in range(self.rows):
      for c in range(self.cols):
        self.test_for_low(r, c)

  def test_for_low(self, r, c):
    this_cell = self.lines[r][c]
    # log(f'test_for_low {r},{c} => {this_cell} ')

    for delta_r in range(-1,2):
      for delta_c in range(-1,2):
        if (delta_r != 0 or delta_c != 0):
          row = r + delta_r
          col = c + delta_c
          if row >= 0 and col >= 0 and row < self.rows and col < self.cols:
            that_cell = self.lines[row][col]
            # log(f'             {row},{col} => {that_cell} ')

            if this_cell >= that_cell:
              # log(f'             NOPE!')
              return 0
    # no neighbors were greater....
    log(f'LOW SPOT at {r},{c} => {this_cell} ')
    risk = int(this_cell) + 1
    self.total_risk += risk

  def find_basins(self):
    for r in range(self.rows):
      for c in range(self.cols):
        self.explore_basin(r, c)
    self.basins = list(reversed(sorted(self.basins)))

  def basin_score(self):
    if len(self.basins) > 2:
      return self.basins[0] * self.basins[1] * self.basins[2]

  def dump(self):
    log('')
    log(f'Board: cols:{self.cols} rows:{self.rows}')
    log("lines:")
    for row in self.lines:
      log(row)
    log("Counts:")
    for row in self.seen:
      log(row)
    log('')

  def summary(self):
    return f"Board {self.filename}: lines:{len(self.lines)}"

def main():
  board = Board(filename)
  board.find_basins()
  board.dump()
  answer = board.basin_score()
  log(f"basin score: {answer} ")

  target = int(filename.split('-')[-1])
  assert answer == target, f"NOPE! the answer should be {target}, not {answer}"

main()

