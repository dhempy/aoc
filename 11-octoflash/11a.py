#! /usr/local/bin/python3

# --- Day 11: Dumbo Octopus ---
#
# You enter a large cavern full of rare bioluminescent dumbo octopuses!
# They seem to not like the Christmas lights on your submarine, so you
# turn them off for now.
# Like: Game of life. Matrix math.

# filename = "input-test.txt"
filename = "input-solo.txt"
# filename = "input.txt"

import math
# debug = False
debug = True

def log(m):
  if debug: print(m)

class Octopus:
  def __init__(self, board, pos, power):
    log(f"Board.init({filename}")
    self.board = board
    self.pos = pos
    self.power = power
    self.row = int(pos/board.size)
    self.col = pos - self.row * board.size
    self.neighbors = []
    # self.dump()

  def init_neighbors(self):
    log("\n init_neighbors... ")
    for r in range(-1,2):
      for c in range(-1,2):
        row = self.row + r
        col = self.col + c
        if (r != 0 or c != 0) and row >= 0 and col >= 0 and row < self.board.size and col < self.board.size:
          self.neighbors.append(row * self.board.size + col)

  def dump(self):
    log(f"  Octopus: {self.pos} at {self.row},{self.col} with power {self.power}")
    log(f"           {self.neighbors}")

class Board:
  def __init__(self, filename):
    log(f"Board.init({filename}")
    self.filename = filename
    self.flash_count = 0
    self.day = 0
    self.slurp()
    self.area = len(self.flat)
    self.size = int(math.sqrt(self.area))
    octopii = []
    for pos, power in enumerate(self.flat):
      print(f"power:{power} pos:{pos} ({type(pos)})")
      octopii.append(Octopus(self, pos, power))
    for o in octopii:
      o.init_neighbors()
      o.dump()

  def slurp(self):
    file = open(self.filename)
    raw = file.read()
    log(raw)
    grid = raw.split()
    log(grid)
    self.flat = ''.join(grid)
    log(f"flat: {self.flat}")


  def dump(self):
    if not debug: return
    log(Board.summary)

  def flash_count(self):
    return self.last_hit * sum(sum(self.lines[0:5], [])) # only the rows, not the (redundant) columns

  def summary(self):
    return f"Board {self.filename}: flash_count={self.flash_count()}"

  def advance(self):
    log(f"advance from day {self.day}")
    self.day += 1
    self.flash_count += 2

def main():
  board = Board(filename)
  board.dump()

  for day in range(5):
    board.advance()

  print(f"\nNumber of flashes: ")
  print(board.flash_count)
  # assert board.flash_count == 1656, "NOPE! Winning flash_count should be 1656"

main()

