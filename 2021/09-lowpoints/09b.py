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


class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    self.total_risk = 0
    self.map = self.slurp()
    self.rows = len(self.map)
    self.cols = len(self.map[0])
    # self.seen = numpy.full_like(self.map, False)
    self.seen = numpy.full((self.rows, self.cols), False, dtype=bool)
    # self.seen.fill(False)
    # numpy.full((2,2), True, dtype=bool)

    self.basins = []
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

  def find_basins(self):
    for r in range(self.rows):
      for c in range(self.cols):
        self.explore_basin(r, c)
    self.basins = list(reversed(sorted(self.basins)))

  def explore_basin(self, r, c, record_basin = True):
    this_cell = self.map[r][c]
    log(f' explore_basin {r},{c} => {this_cell} ')

    if self.seen[r][c]:
      log(f'   btdt')
      return 0
    self.seen[r][c] = True

    if '9' == this_cell:
      log(f'   border')
      return 0

    basin_size = 1 + self.basin_neighbors(r, c)

    if record_basin:
      log(f'  BASIN FOUND: {r},{c} => {basin_size} ')
      self.basins.append(basin_size)

    return basin_size

  def basin_neighbors(self, r, c):
    basin_size = 0
    log(f'  basin_neighbors {r},{c}')

    if r > 0:
      basin_size += self.explore_basin(r-1, c  , False)
    if c > 0:
      basin_size += self.explore_basin(r  , c-1, False)
    if r+1 < self.rows:
      basin_size += self.explore_basin(r+1, c  , False)
    if c+1 < self.cols:
      basin_size += self.explore_basin(r  , c+1, False)

    log(f'basin_neighbors at {r},{c} => {basin_size} ')
    return basin_size

  def basin_score(self):
    if len(self.basins) > 2:
      return self.basins[0] * self.basins[1] * self.basins[2]

  def dump(self):
    log('')
    log(f'Board: cols:{self.cols} rows:{self.rows}')
    log("map:")
    for row in self.map:
      log(row)
    log("seen:")
    for row in self.seen:
      log(row)
    log("basins:")
    for row in self.basins:
      log(row)
    log(f"basin score: {self.basin_score()} ")
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

