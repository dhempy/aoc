#! /usr/local/bin/python3
filename = "input-10"
filename = "input-19"
filename = "input-226"
# filename = "input"

from collections import Counter

# debug = False
debug = True


max_days = 1000

import math
def log(m):
  if debug: print(m)

class Tunnel:
  def __init__(self, board, line):
    log(f"Tunnel.init({line})")
    self.raw_line = line
    self.board = board
    self.src, self.dest = line.split('-')
    self.dump()

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




  def dump(self):
    log(f"  Tunnel: {self.src} -- {self.dest}  (input: {self.raw_line}) ")

class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    self.tunnels = {}
    self.path_count = 123
    self.today = 0
    self.slurp()
    # self.area = len(self.flat)
    # self.size = int(math.sqrt(self.area))
    # self.octopii = []
    # self.daily_paths = [0] * max_days
    # for pos, power in enumerate(self.flat):
    #   print(f"power:{power} pos:{pos} ({type(pos)})")
    #   self.octopii.append(Tunnel(self, pos, power))
    # for o in self.octopii:
    #   o.init_neighbors()
    #   o.dump()

  def slurp(self):
    for line in open(self.filename):
      line = line.rstrip()
      self.tunnels[line] = Tunnel(self, line)

  def dump(self):
    if not debug: return
    log(Board.summary)

  # def path_count(self):
  #   return self.last_hit * sum(sum(self.lines[0:5], [])) # only the rows, not the (redundant) columns

  def summary(self):
    return f"Board {self.filename}: path_count={self.path_count()}"

  # def flashed(self):
  #   self.path_count += 1
  #   # print(f"today is {self.today}")
  #   self.daily_paths[self.today] += 1
  #   if self.daily_paths[self.today] == self.area:
  #     print(f"ALL FLASHING ON DAY {self.today} <<<<<<<<<<<<<<<<< ")
  #     exit()


  # def advance(self):
  #   log(f"================================== advance from day {self.today}:")
  #   self.today += 1
  #   for o in self.octopii:
  #     o.energize()
  #   print(f"On day {self.today}, {self.daily_paths[self.today]} paths occurred. <<<< ")

def main():

  board = Board(filename)
  board.dump()

  # for day in range(max_days):
  #   board.advance()


  print(f"\nNumber of paths: {board.path_count}")

  target = filename.split('-')[-1]
  assert board.path_count == target, f"NOPE! the total should be {target}, not {board.path_count}"

main()

