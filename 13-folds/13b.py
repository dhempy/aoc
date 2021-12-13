#! /usr/local/bin/python3
# filename = "input-17"
filename = "input"

max_size = 1310

import re
# debug = False
debug = True


max_days = 1000

import math
import numpy

def log(m):
  if debug: print(m)


class Board:
  def __init__(self, filename):
    log(f"Board.init({filename})")
    self.filename = filename

    self.dots = {}
    self.folds = []

    self.slurp()
    self.dump()

  def dot_count(self):
    return len(self.dots)

  def slurp(self):
    raw_dots, raw_folds = open(self.filename).read().split('\n\n')

    for point in raw_dots.split():
      self.dots[point] = 1


    fold_regex = re.compile("fold along")
    self.folds = list(filter(fold_regex.match,raw_folds.split('\n')))

  def fold_first(self):
    self.dump()
    self.fold(self.folds[0])
    self.dump()

  def fold_all(self):
    self.dump()
    for fold in self.folds:
      self.fold(fold)
      self.dump()



  def fold(self, fold):
    axis_value = fold.split()[-1]
    axis, value = axis_value.split('=')
    value = int(value)
    log(f">> fold {axis} at {value} ")
    if axis == 'x':
      self.fold_x(value)
    elif axis == 'y':
      self.fold_y(value)

  def fold_x(self, threshold):
    for old_dot in self.dots.copy().keys():
      x,y = old_dot.split(',')
      log(f"fold_x({threshold}) x is {x} ")
      val = int(x)
      if val > threshold:
        x = threshold - (val - threshold)
        new_dot = f"{x},{y}"
        self.dots[new_dot] = 1
        log(f'  create dot {new_dot}')
        self.kill(old_dot)
      elif val == threshold:
        log(f'  ignore dot {new_dot}')
        self.kill(old_dot)

  def fold_y(self, threshold):
    for old_dot in self.dots.copy().keys():
      x,y = old_dot.split(',')
      log(f"fold_y({threshold}) y is {y} ")
      val = int(y)
      if val > threshold:
        y = threshold - (val - threshold)
        new_dot = f"{x},{y}"
        self.dots[new_dot] = 1
        self.kill(old_dot)
      elif val == threshold:
        self.kill(old_dot)

  def kill(self, dot):
    log(f'  delete dot {dot}')
    del self.dots[dot]

  def display(self):
    max_x = 0
    max_y = 0
    for pair in self.dots.keys():
      x, y = pair.split(',')
      x = int(x)
      y = int(y)
      if x > max_x:
        max_x = x
      if y > max_y:
        max_y = y
    log(f"max_x:{max_x} max_y:{max_y} ")
    grid = numpy.zeros((max_x+1, max_y+1))

    for pair in self.dots.keys():
      x, y = pair.split(',')
      x = int(x)
      y = int(y)
      grid[x,y] = 1

    log(grid)
    grid = numpy.flip(grid)
    log(grid)
    grid = numpy.flip(grid, 0)
    log(grid)
    grid = numpy.flip(grid, 1)
    log(grid)

  def dump(self):
    log('')
    log(self.summary())
    log(self.dots)
    # log(self.folds)
    log('')

  def summary(self):
    return f"Board {self.filename}: dots: {len(self.dots)} folds: {len(self.folds)}"

def main():
  board = Board(filename)
  # board.fold_first()
  board.fold_all()
  board.display()
main()

