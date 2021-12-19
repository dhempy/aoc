#! /usr/local/bin/python3
filename = "in-full"
filename = "explode-2"
# filename = "in-13"

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
import re

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


  def magnitude(self, item):
    # The magnitude of a pair is
    #   3 times the magnitude of its left element
    #   plus
    #   2 times the magnitude of its right element.
    # The magnitude of a regular number is just that number.

    # print(f'type of item is {type(item)} ')
    if type(item) == int:
      return item
    log(f'magnitude({item}) ')
    left, right = item[0:2]
    # log(f'adding 3*{left} and 2*{right}...')
    mag = 3*self.magnitude(left) + 2*self.magnitude(right)
    # log(f' ... to get: {mag}')
    return mag




  def sum(self):
    log('sum()...')
    sum = False
    for a in self.addends:
      log(f' sum(): a = {a}')
      if sum:
        log(' sum().adding...')
        sum = self.add(sum, a)
      else:
        log(' sum().intializing...')
        sum = self.reduce_number(a)
    self.final_sum = sum
    return self.to_s(sum)


  def add(self, a, b):
    log(f'\n add({a}, {b}) ')

    a = self.reduce_number(a)
    b = self.reduce_number(b)
    return [a,b]

  def reduce_number(self, number):
    current_number = number
    while True:
      log(f' current: {current_number}')
      reduced = self.reduce_item_exploder(current_number) or \
                self.reduce_item_splitter(current_number)
      if not reduced:
        break
      current_number = reduced
    return current_number


  def reduce_item_exploder(self, item, depth=0, src=False):
    # To reduce a snailfish number, you must repeatedly do the first action
    # in this list that applies to the snailfish number:
    #  - If any pair is nested inside four pairs, the leftmost such pair explodes.
    #  - If any regular number is 10 or greater, the leftmost such regular number splits.
    #
    # If nothing reduced, it returns false.
    # Else it returns a replacement for the *entire* number (not just this item) (as a deep array of items)

    src = src or item

    if type(item) == int:
      return False

    # log(f'\n  reduce_item_exploder({item}, depth=>{depth}, src=>{src})')

    if depth >= 4:
      return self.explode(item, depth, src)

    # log(f'             item: "{item}" ')
    return self.reduce_item_exploder(item[0], depth+1, src) or \
           self.reduce_item_exploder(item[1], depth+1, src)

  def reduce_item_splitter(self, item, src=False):
    #  - If any regular number is 10 or greater, the leftmost such regular number splits.
    #
    # If nothing reduced, it returns false.
    # Else it returns a replacement for the *entire* number (not just this item) (as a deep array of items)

    log(f'  reduce_item_splitter({item})...')

    src = src or item

    if type(item) == int:
      if item >= 10:
        return self.split(item, depth)
      else:
        return False

  def split(self, item):
    # To split a regular number, replace it with a pair;
    # the left element of the pair should be the regular number divided by two and rounded down,
    # while the right element of the pair should be the regular number divided by two and rounded up.
    # For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
    log(f'   TOO HIGH! {item}...SPLIT!')
    return f'split-{item}'

  def explode(self, item, depth, src):
    # To explode a pair, the pair's left value is added to the first regular
    # number to the left of the exploding pair (if any), and the pair's
    # right value is added to the first regular number to the right of the
    # exploding pair (if any). Exploding pairs will always consist of two
    # regular numbers. Then, the entire exploding pair is replaced with the
    # regular number 0.
    # item is an array (typ. exactly one pair of ints.)
    # returns an array, which is the new entire number from src, after item is exploded.

    # log(f'   TOO DEEP...EXPLODE! {item}, depth=>{depth}, src=>{src}')
    item[0] = -item[0]  # negative to ensure a unique match. All legit input is positive.
    item[1] = -item[1]
    pre, post = self.to_s(src).split(f'[{item[0]},{item[1]}]')
    item[0] = -item[0]
    item[1] = -item[1]

    log(f' EXPLODE: {pre} <-- [{item[0]},{item[1]}] --> {post} ')


    matches = re.match(r'(.*)(\d+)(\D*)', pre)
    if matches:
      new_val = int(matches[2]) + int(item[0])
      pre = f'{matches[1]}{new_val}{matches[3]}'

    matches = re.match(r'(\D*)(\d+)(.*)', post)
    if matches:
      new_val = int(matches[2]) + int(item[1])
      post = f'{matches[1]}{new_val}{matches[3]}'

    log(f' EXPLODE: {pre} <--   0   --> {post} ')
    reduced_number = f'{pre}0{post}'
    return eval(reduced_number)


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
  print(f"\a")
  print(f"                     sum: {sum}")
  print(f"      board.expected_sum: {board.expected_sum}")
  magnitude = board.magnitude(board.final_sum)
  print(f"               magnitude: {magnitude}")
  print(f"board.expected_magnitude: {board.expected_magnitude}\n")

  if board.expected_sum:
    assert sum == board.expected_sum, f"NOPE! the sum should be \n  {board.expected_sum}, not \n  {sum}"

  if board.expected_magnitude:
    assert magnitude == board.expected_magnitude, f"NOPE! the magnitude should be \n  {board.expected_magnitude}, not \n  {magnitude}"

  print("NO ERRORS DETECTED!  :-D")
main()

