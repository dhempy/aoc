#! /usr/local/bin/python3
filename = "input-36"
filename = "input-103"
filename = "input-3509"
filename = "input"

from collections import Counter

# debug = False
debug = True


max_days = 1000

import math
def log(m):
  if debug: print(m)

class Tunnel:
  def __init__(self, board, src, dest):
    log(f"Tunnel.init({src, dest})")
    self.board = board
    self.src = src
    self.dest = dest
    self.dump()

  # def inverse(self):
  #   reverse_line = f"{self.dest}-{self.src}"
  #   Tunnel(self.board, reverse_line)

  def dump(self):
    log(f"  Tunnel: {self.src} -- {self.dest}   ")

class Cave:
  def __init__(self, name):
    log(f"Cave.init({name})")
    self.name = name
    self.tunnels = []
    self.big = self.name.isupper()
    self.times_seen = 0
    self.dump()

  def add_tunnel(self, tunnel):
    log(f"add_tunnel({tunnel})")
    assert(self.name == tunnel.src)
    self.tunnels.append(tunnel)
    log("TODO: add reverse tunnels")

  def dump(self):
    log(f"Cave {self.name}: {'BIG' if self.big else 'small'} tunnel_count={len(self.tunnels)}")
    for tunnel in self.tunnels:
      tunnel.dump()


class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    self.tunnels = []
    self.caves = {}
    self.path_count = 0
    self.slurp_tunnels()
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

  def slurp_tunnels(self):
    for line in open(self.filename):
      src, dest = line.rstrip().split('-')
      self.tunnels.append(Tunnel(self, src, dest))
      self.tunnels.append(Tunnel(self, dest, src))

  def dig_caves(self):
    for tunnel in self.tunnels:
      log(f"dig caves for tunnel {tunnel}")
      log(f"dig cave {tunnel.src}")
      log(f"dig cave {tunnel.dest}")
      if tunnel.src not in self.caves.keys():
        self.caves[tunnel.src] = Cave(tunnel.src)
      if tunnel.dest not in self.caves.keys():
        self.caves[tunnel.dest] = Cave(tunnel.dest)
      self.caves[tunnel.src].add_tunnel(tunnel)

  def count_paths(self, src, final_dest, bonus_used=False, depth=0):
    # bonus_used means we already double-hit a small.
    # if depth > 10: # small boards only.
    #   log(f" >>>>>>>>>>>>>>>>>>> Max Depth ({depth}) exceeded!")
    #   return 0

    here = self.caves[src]

    if here.times_seen > 0 and src == 'start': # this is hacky, I know.
        # log(f"{'|' * depth}  Backing out from {src} because START IS SPECIAL.")
        return 0

    if here.times_seen > 0 and not here.big and bonus_used:
        # log(f"{'|' * depth}  Backing out from {src} because we've been here.")
        return 0

    log(f"{'|' * depth} count_paths({src}, {final_dest}, {bonus_used}, {depth} )... (been_here is {here.times_seen})")

    if src == final_dest:
      # self.path_count += 1
      # return self.path_count
      log(f"{'|' * depth}  TERMINUS! +1")
      return 1



    path_count = 0
    prior_count = here.times_seen
    here.times_seen += 1

    for tunnel in here.tunnels:
      if here.big:
        path_count += self.count_paths(tunnel.dest, final_dest, bonus_used, depth+1)
      elif prior_count == 0:
        path_count += self.count_paths(tunnel.dest, final_dest, bonus_used, depth+1)
      elif prior_count == 1 and not bonus_used:
        path_count += self.count_paths(tunnel.dest, final_dest, True, depth+1)

    here.times_seen -= 1
    log(f"{'|' * depth} count_paths({src}, {final_dest}) returning {path_count}")
    return path_count


  def dump(self):
    log('')
    log(self.summary())
    for cave in self.caves.values():
      cave.dump()
    log('')

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
  total = board.count_paths('start', 'end', False)
  print(f"\nNumber of paths: {total}")

  target = int(filename.split('-')[-1])
  assert total == target, f"NOPE! the total should be {target}, not {total}"

main()

