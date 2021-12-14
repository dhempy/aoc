#! /usr/local/bin/python3
filename = "input-1588"
# filename = "input"

from collections import Counter

# debug = False
debug = True


max_days = 10

import math
def log(m):
  if debug: print(m)

class Rule:
  def __init__(self, target, insert):
    # log(f"Rule.init({name})")
    self.target = target
    self.insert = insert
    self.dump()

  def dump(self):
    log(f" {self.target} gets {self.insert}")


class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    self.tunnels = []
    self.caves = {}
    self.path_count = 0
    self.slurp()
    self.dig_caves()
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
    self.dump()

  def slurp(self):
    file = open(self.filename)

    self.word = file.readline()
    log(f'STARTING WORD: {self.word}')
    file.readline()

    self.rules = []
    for line in file:
      target, insert = line.rstrip().split(' -> ')
      self.rules.append(Rule(target, insert))

  def dig_caves(self):
    for tunnel in self.tunnels:
      log(f"dig caves for tunnel {tunnel}")
      log(f"dig cave {tunnel.pre}")
      log(f"dig cave {tunnel.post}")
      if tunnel.pre not in self.caves.keys():
        self.caves[tunnel.pre] = Cave(tunnel.pre)
      if tunnel.post not in self.caves.keys():
        self.caves[tunnel.post] = Cave(tunnel.post)
      self.caves[tunnel.pre].add_tunnel(tunnel)

  def count_paths(self, pre, final_post):
    log(f"count_paths({pre}, {final_post})...")
    if pre == final_post:
      # self.path_count += 1
      # return self.path_count
      log(f" TERMINUS! +1")
      return 1

    here = self.caves[pre]
    if here.in_path and not here.big:
      log(f"  Backing out from {pre} because we've been here.")
      return 0

    here.in_path = True
    path_count = 0
    for tunnel in here.tunnels:
      path_count += self.count_paths(tunnel.post, final_post)

    here.in_path = False
    log(f"count_paths({pre}, {final_post}) returning {path_count}")
    return path_count


  def dump(self):
    log(self.summary())
    for cave in self.caves.values():
      cave.dump()

  def summary(self):
    return f"Board {self.filename}: path_count={self.path_count}"

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
  total = board.count_paths('start', 'end')
  print(f"\nNumber of paths: {total}")

  target = int(filename.split('-')[-1])
  assert total == target, f"NOPE! the total should be {target}, not {total}"

main()

