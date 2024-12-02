#! /usr/local/bin/python3
# filename = "inputb-8"
# filename = "input-40"
filename = "input-full"
# filename = "input-janine"

debug = False
# debug = True

import math
import numpy
import json
import sys
import jsbeautifier
import os
import time

time_start = time.time()
last_start = time_start

numpy.set_printoptions(linewidth=400)

def time_log(m):
  now = time.time()
  total_elapsed = int(now - time_start)
  elapsed = int(now - last_start)
  last_start = now
  log (f"{m} (+{elapsed}s => {total_elapsed}s)")

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
    self.seen = numpy.full((self.rows, self.cols), 0, dtype=int)
    self.safest = sys.maxsize
    try:
      self.load_wip()
    except:
      print("No wip files to load. Zero out paths for ({self.rows},{self.cols}):")
      self.safest_to_here = numpy.full((self.rows, self.cols), sys.maxsize, dtype=int)
    self.dump(True)

  def slurp(self):
    return numpy.loadtxt(self.filename, dtype = str)

  def save_wip(self):
    try:
      os.mkdir(f'{self.filename}.data_foreward', 0o755 )
    except FileExistsError:
      'ok'

    print(f"Saving distance wip to {self.filename}.data_foreward/distances.{self.safest}")
    numpy.savetxt(f"{self.filename}.data_foreward/distances", self.safest_to_here, fmt='%3i')
    numpy.savetxt(f"{self.filename}.data_foreward/distances.{self.safest}", self.safest_to_here, fmt='%3i')
    if self.seen.any(): # don't save an empty seen array
      print(f"Saving path wip to {self.filename}.data_foreward/path.{self.safest}")
      numpy.savetxt(f"{self.filename}.data_foreward/path", self.seen, fmt='%i')
      numpy.savetxt(f"{self.filename}.data_foreward/path.{self.safest}", self.seen, fmt='%i')


  def load_wip(self):
    self.safest_to_here = numpy.loadtxt(f"{self.filename}.data_foreward/distances")

  # def study(self):
  #   changed = True
  #   self.safest_to_here[0][0] = 0  # first hit's free.

  #   while changed:
  #     time_log(f'study all risks. Final risk is currently {self.map[-1][-1]}')
  #     changed = False
  #     for row, r in enumerate self.map:
  #       time_log(f' study row {r}.')
  #       for cell, c in enumerate row:
  #         new_risk = cell + self.safest_neighbor(r,c)
  #         if new_risk < self.safest_to_here[r][c]:
  #           changed = True
  #           self.safest_to_here[r][c] = new_risk
  #   time_log(f'\nFINISHED studying all risks. Final risk is {self.map[-1][-1]}')


  def safest_neighbor(self, r, c):
    return min([ risk_at(r+1, c), risk_at(r, c+1), risk_at(r-1, c-1)])

  def risk_at(serlf, r, c):
    if r < self.rows and c < self.cols and r >= 0 and c >= 0:
      return self.map[r][c]
    else:
      return sys.maxsize


    # try:
    #   this_cell = int(self.map[r][c])
    #   self.seen[r][c] = this_cell

    #   if risk == 'init':  # Don't count the origin cell
    #     new_risk = risk = 0
    #   else:
    #     new_risk = risk + this_cell
    #   # log(f'path from {r},{c} ({this_cell}) with risk {risk}+{this_cell} => {new_risk} will compare with safest {self.safest}...')

    #   if new_risk > self.safest_to_here[r][c]:
    #     # This is probably not legit.
    #     # Perhaps an expensive early path allows for a cheaper later path?
    #     log(f'  {new_risk} exceeds safest subrisk.')
    #     return sys.maxsize

    #   self.safest_to_here[r][c] = new_risk
    #   log(f' new safest subpath to {r},{c}: {new_risk}')



  def study2(self):
    self.greedy = True

    # Build greedily from the end:
    # answer = self.find_safest_path()

    print(f"Build greedily, by trailing row and column:...")
    for d in range(self.rows, 0, -1):
      self.safest = sys.maxsize
      print(f" study starting at {d},{d}")
      self.find_safest_path(d, d)
    self.save_wip() # For restarts, and part B of the problem!
    global time_start, last_start
    elapsed = int(time.time() - last_start)
    last_start = time.time()
    total_elapsed = int(time.time() - time_start)
    print(f"Finished studying  (+{elapsed}s => {total_elapsed}s)")
    self.safest = sys.maxsize # expected to be too low

    # # Build greedily, incrementally by grid, limited by length:
    # grid_step = 10
    # ceiling = grid_step * grid_step  * 9   # 9 is max risk per cell
    # answer = ceiling
    # print(f"Look for a path shorter than {ceiling}...")
    # self.safest = ceiling # expected to be too low
    # for r in range(self.rows, 0, -grid_step):
    #   for c in range(self.cols, 0, -grid_step):
    #     print(f" study starting at {r},{c} up to {ceiling} long")
    #     self.safest = sys.maxsize
    #     self.find_safest_path(r, c, r+grid_step, c+grid_step)
    #     self.save_wip()
    # self.safest = sys.maxsize

    # Build greedily, incrementally from origin, limited by length:
    # ceiling = 10
    # answer = ceiling
    # while ceiling == answer:
    #   ceiling += 10
    #   log(f"Look for a path shorter than {ceiling}...")
    #   self.safest = ceiling # expected to be too low
    #   answer = self.find_safest_path()
    #   self.save_wip() # For restarts, and part B of the problem!
    #   global time_start, last_start
    #   elapsed = int(time.time() - last_start)
    #   last_start = time.time()
    #   total_elapsed = int(time.time() - time_start)
    #   print(f"The safest path shorter than {ceiling} was {answer} (+{elapsed}s => {total_elapsed}s)")

    # don't trust the GREEDY result:
    self.safest = sys.maxsize
    self.greedy = False

    print(f"\nSTUDYING FOUND SOLUTION: {answer} ")
    return answer


  def find_safest_path(self, r=0, c=0, max_r=False, max_c=False, risk='init'):
    max_r = max_r or self.rows
    max_c = max_c or self.cols

    if c >= max_c or r >= max_r or c < 0 or r < 0:
      # log(f'  {r},{c} out of bounds!')
      return sys.maxsize
    log(f'{r},{c} ({self.safest_to_here[r][c]})')

    if self.seen[r][c]:
      # log(f'  seen.')
      return sys.maxsize

    try:
      this_cell = int(self.map[r][c])
      self.seen[r][c] = this_cell

      if risk == 'init':  # Don't count the origin cell
        new_risk = risk = 0
      else:
        new_risk = risk + this_cell
      # log(f'path from {r},{c} ({this_cell}) with risk {risk}+{this_cell} => {new_risk} will compare with safest {self.safest}...')

      if new_risk > self.safest_to_here[r][c]:
        # This is probably not legit.
        # Perhaps an expensive early path allows for a cheaper later path?
        log(f'  {new_risk} exceeds safest subrisk.')
        return sys.maxsize

      self.safest_to_here[r][c] = new_risk
      log(f' new safest subpath to {r},{c}: {new_risk}')

      if new_risk >= self.safest:
        # log(f'  safest risk exceeded!')
        return sys.maxsize
      log(f'path from {r},{c} with risk {risk} + {this_cell} => {new_risk} is LESS THAN {self.safest}')

      steps_left = (self.rows - r) + (self.cols - c)
      if r == self.rows-1 and c == self.cols-1:
        self.new_solution(new_risk)
        return new_risk

      self.find_safest_path(r+1,   c, max_r, max_c, new_risk)
      self.find_safest_path(r,   c+1, max_r, max_c, new_risk)
      self.find_safest_path(r-1,   c, max_r, max_c, new_risk)
      self.find_safest_path(r,   c-1, max_r, max_c, new_risk)

      return self.safest

    finally:
      self.seen[r][c] = False

  def new_solution(self, risk):
    global time_start
    elapsed = int(time.time() - time_start)
    print(f'  ^^ NEW SOLUTION: {risk} {elapsed}s')
    self.safest = risk
    self.save_wip() # For restarts, and part B of the problem!


  def dump(self, force=False):
    global debug
    debug_was = debug
    if force:
      debug = True

    log('')
    log(f'Board: cols:{self.cols} rows:{self.rows}')
    log("map:")
    for row in self.map:
      log(row)
    # log("seen:")
    # for row in self.seen:
    #   log(row)
    log("safest_to_here:")
    for row in self.safest_to_here:
      log(row)
    log('')
    debug = debug_was

  def summary(self):
    return f"Board {self.filename}: lines:{len(self.lines)}"

def main():
  board = Board(filename)
  board.dump()

  try:
    # answer = board.study()
    answer = board.find_safest_path()
  except KeyboardInterrupt:
    board.save_wip()




  log(f"answer: {answer} ")

  print('\a') # bell


  target = int(filename.split('-')[-1])
  assert answer == target, f"NOPE! the answer should be {target}, not {answer}"

main()

