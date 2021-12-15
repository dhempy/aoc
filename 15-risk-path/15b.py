#! /usr/local/bin/python3
# filename = "inputb-8"
filename = "input-40"
# filename = "input"

debug = False
# debug = True

import math
import numpy
import sys

def log(m):
  if debug: print(m)


class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    try:
      self.load()
    except:
      self.total_risk = 0
      self.map = self.slurp()
      self.rows = len(self.map)
      self.cols = len(self.map[0])
      self.seen = numpy.full((self.rows, self.cols), False, dtype=bool)
      self.safest_to_here = numpy.full((self.rows, self.cols), sys.maxsize, dtype=int)
    self.dump()

  def slurp(self):
    # self.lines = open(self.filename).read().split()
    return numpy.loadtxt(self.filename, dtype = numpy.str)

  def json_filename():
    return f"{self.filename}.json"

  def save(self):
    file = open(json_filename(), "w")
    file.write(json.JSONEncoder().encode())

  def load(self):
    file = open(json_filename(), "r")
    json.JSONDecoder.decode(file.read())

  def find_safest_path(self, safest=sys.maxsize, r=0, c=0, risk='init'):
    if c >= self.cols or r >= self.rows or c < 0 or r < 0:
      # log(f'  {r},{c} out of bounds!')
      return sys.maxsize
    log(f'{r},{c} ({self.safest_to_here[r][c]})')

    if self.seen[r][c]:
      # log(f'  seen.')
      return sys.maxsize

    try:
      this_cell = int(self.map[r][c])
      self.seen[r][c] = True

      if risk == 'init':  # Don't count the origin cell
        new_risk = risk = 0
      else:
        new_risk = risk + this_cell
      # log(f'path from {r},{c} ({this_cell}) with risk {risk}+{this_cell} => {new_risk} will compare with safest {safest}...')

      if new_risk > self.safest_to_here[r][c]:
        # This is probably not legit.
        # Perhaps an expensive early path allows for a cheaper later path?
        log(f'  {new_risk} exceeds safest subrisk.')
        return sys.maxsize

      self.safest_to_here[r][c] = new_risk
      log(f' new safest subpath to {r},{c}: {new_risk}')

      if new_risk >= safest:
        # log(f'  safest risk exceeded!')
        return sys.maxsize
      log(f'path from {r},{c} with risk {risk} + {this_cell} => {new_risk} is LESS THAN {safest}')

      steps_left = (self.rows - r) + (self.cols - c)
      if r == self.rows-1 and c == self.cols-1:
        print(f'  SOLUTION ON EXIT: {new_risk}')
        return new_risk

      final_risk = self.find_safest_path(safest, r+1, c, new_risk)
      if final_risk < safest:
        safest = final_risk

      final_risk = self.find_safest_path(safest, r, c+1, new_risk)
      if final_risk < safest:
        safest = final_risk

      final_risk = self.find_safest_path(safest, r-1, c, new_risk)
      if final_risk < safest:
        safest = final_risk

      final_risk = self.find_safest_path(safest, r, c-1, new_risk)
      if final_risk < safest:
        safest = final_risk

      return safest

    finally:
      self.seen[r][c] = False

  def dump(self):
    log('')
    log(f'Board: cols:{self.cols} rows:{self.rows}')
    log("map:")
    for row in self.map:
      log(row)
    # log("seen:")
    # for row in self.seen:
    #   log(row)
    log('')

  def summary(self):
    return f"Board {self.filename}: lines:{len(self.lines)}"

def main():
  board = Board(filename)
  board.dump()

  answer = board.find_safest_path()

  # ceiling = board.rows + board.cols
  # answer = ceiling
  # while ceiling == answer:
  #   ceiling *= 2
  #   log(f"Look for a path shorter than {ceiling}...")
  #   answer = board.find_safest_path(ceiling)
  #   log(f"The safest path shorter than {ceiling} was {answer}")

  log(f"answer: {answer} ")

  print('\a') # bell

  board.save() # For Part B of the problem!

  target = int(filename.split('-')[-1])
  assert answer == target, f"NOPE! the answer should be {target}, not {answer}"

main()

