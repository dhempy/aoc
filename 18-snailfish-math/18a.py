#! /usr/local/bin/python3
filename = "in-full"
filename = "in-1"
filename = "in-7"

# debug = False
debug = True

import math
import numpy
import json
import sys
import jsbeautifier
import os
from os.path import exists
import time

time_start = time.time()
last_start = time_start

numpy.set_printoptions(linewidth=400)

def time_log(m, force=False):
  global time_start, last_start
  now = time.time()
  total_elapsed = int(now - time_start)
  elapsed = int(now - last_start)
  last_start = now
  log (f"{m} (+{elapsed}s => {total_elapsed}s)", force)

def log(m, force=False):
  if debug or force: print(m)

class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename
    self.slurp()

  def slurp(self):
    self.addends = []
    for line in open(filename):
      self.addends.append(eval(line))

    if exists(f"{filename}-answer"):
      # self.expected_sum =           open(f"{filename}-answer").read()
      self.expected_sum = self.to_s(open(f"{filename}-answer").read())
    else:
      self.expected_sum = False

    if exists(f"{filename}-magnitude"):
      self.expected_magnitude = int(open(f"{filename}-magnitude").read())
    else:
      self.expected_magnitude = False

  def reduce(self, num):
    log(f'\n  reduce({num}) TODO:')
    return num

  def add(self, a, b):
    log(f'\n add({a}, {b}) ')
    a = self.reduce(a)
    b = self.reduce(b)
    return [a,b]

  def sum(self):
    log('sum()...')
    sum = False
    for a in self.addends:
      if sum:
        sum = self.add(sum, a)
      else:
        sum = a
    self.final_sum = sum
    return self.to_s(sum)

  def magnitude(self, item = False):
    # The magnitude of a pair is 3 times the magnitude of its left element
    # plus 2 times the magnitude of its right element. The magnitude of a
    # regular number is just that number.
    item = item or self.final_sum
    # print(f'type of item is {type(item)} ')
    if type(item) == int:
      return item
    log(f'magnitude({item}) ')
    left, right = item[0:2]
    log(f'adding 3*{left} and 2*{right}...')
    mag = 3*self.magnitude(left) + 2*self.magnitude(right)
    log(f' ... to get: {mag}')
    return mag

  def to_s(self, s):
    return str(s).replace(' ','')

  def dump(self):
    log(f'\nBoard: count:{len(self.addends)}')
    log("Addends:")
    for row in self.addends:
      log(f'  {row}')
    log(f"expected_sum: {self.expected_sum}")
    log(f"expected_magnitude: {self.expected_magnitude}")
    log('')

def main():
  board = Board(filename)
  board.dump()
  sum = board.sum()
  magnitude = board.magnitude()
  print(f"               sum: {sum} \a")
  print(f"board.expected_sum: {board.expected_sum} \a")
  print(f"               magnitude: {magnitude} \a")
  print(f"board.expected_magnitude: {board.expected_magnitude} \a")


  if board.expected_sum:
    assert sum == board.expected_sum, f"NOPE! the sum should be {board.expected_sum}, not {sum}"

  if board.expected_magnitude:
    assert magnitude == board.expected_magnitude, f"NOPE! the magnitude should be {board.expected_magnitude}, not {magnitude}"
main()

