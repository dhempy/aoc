#! /usr/local/bin/python3

# --- Day 11: Dumbo Octopus ---
#
# You enter a large cavern full of rare bioluminescent dumbo octopuses!
# They seem to not like the Christmas lights on your submarine, so you
# turn them off for now.
# Like: Game of life. Matrix math.

# filename = "input-test.txt"
# filename = "input-solo.txt"
# filename = "input-chain.txt"
filename = "input.txt"

max_days = 1000

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
    self.power = int(power)
    # self.yesterday_power = power
    self.reset_on_day = -1
    self.last_flash_day = -1
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
          self.neighbors.append(self.board.octopii[row * self.board.size + col])
          # self.neighbors.append(row * self.board.size + col)

  def flash(self):
    # log(f"oct({self.row},{self.col}) flashing on day {self.board.today}  POW!!!")
    self.board.flashed()
    self.last_flash_day = self.board.today
    self.reset_on_day = self.board.today + 1
    for o in self.neighbors:
      o.energize()

  def energize(self):
    # self.yesterday_power = power % 10
    if self.reset_on_day == self.board.today:
      self.power = 0
      # log(f"oct({self.row},{self.col}) RESETTING to {self.power}")
      self.reset_on_day = -1

    self.power += 1
    # log(f"oct({self.row},{self.col}) powered to {self.power}")

    if self.power > 9 and self.last_flash_day < self.board.today:
      self.flash()



# First, the energy level of each octopus increases by 1.

# Then, any octopus with an energy level greater than 9 flashes. This
# increases the energy level of all adjacent octopuses by 1,
# including octopuses that are diagonally adjacent. If this causes an
# octopus to have an energy level greater than 9, it also flashes.
# This process continues as long as new octopuses keep having their
# energy level increased beyond 9. (An octopus can only flash at most
# once per step.)

# Finally, any octopus that flashed during this step has its energy
# level set to 0, as it used all of its energy to flash.

# Adjacent flashes can cause an octopus to flash on a step even if it
# begins that step with very little energy. Consider the middle
# octopus with 1 energy in this situation:




  def dump(self):
    log(f"  Octopus: {self.pos} at {self.row},{self.col} with power {self.power}")
    log(f"           {self.neighbors}")

class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    self.flash_count = 0
    self.today = 0
    self.slurp()
    self.area = len(self.flat)
    self.size = int(math.sqrt(self.area))
    self.octopii = []
    self.daily_flashes = [0] * max_days
    for pos, power in enumerate(self.flat):
      print(f"power:{power} pos:{pos} ({type(pos)})")
      self.octopii.append(Octopus(self, pos, power))
    for o in self.octopii:
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

  # def flash_count(self):
  #   return self.last_hit * sum(sum(self.lines[0:5], [])) # only the rows, not the (redundant) columns

  def summary(self):
    return f"Board {self.filename}: flash_count={self.flash_count()}"

  def flashed(self):
    self.flash_count += 1
    # print(f"today is {self.today}")
    self.daily_flashes[self.today] += 1
    if self.daily_flashes[self.today] == self.area:
      print(f"ALL FLASHING ON DAY {self.today} <<<<<<<<<<<<<<<<< ")
      exit()


  def advance(self):
    log(f"================================== advance from day {self.today}:")
    self.today += 1
    for o in self.octopii:
      o.energize()
    print(f"On day {self.today}, {self.daily_flashes[self.today]} flashes occurred. <<<< ")


def main():
  board = Board(filename)
  board.dump()

  for day in range(max_days):
    board.advance()

  print(f"\nNumber of flashes: ")
  print(board.flash_count)
  assert board.flash_count == 1656, "NOPE! Winning flash_count should be 1656"

main()

