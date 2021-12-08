#! /usr/local/bin/python3
# filename = "input-test.txt"
filename = "input-solo.txt"
# filename = "input.txt"

from collections import Counter

debug = False
debug = True

def log(m):
  if debug: print(m)

class Board:
  def __init__(self, name, lines):
    log(f"Board.init({name}, {lines})...")
    self.name = name
    self.lines = lines
    self.last_hit = 0

  def summary(self):
    return f"Board {self.name}: score={self.score()}"

  def dump(self):
    if not debug: return

    log(f"Board {self.name}: last_hit:{self.last_hit} score={self.score()}")
    for line in self.lines:
      log(f"  {line}")



def slurp(filename):
  file = open(filename)
  draws = [int(i) for i in file.readline().split(',')]
  file.readline()
  # log(f"draws: {draws}")

  boards = []
  index = 0
  for grid in file.read().split('\n\n'):
    # log(f"grid: \n{grid}\n")
    string = ' '.join(grid.split('\n'))
    # log(f"string: {string}\n")
    flat = [int(i) for i in string.split()]
    # log(f"flat: {flat}\n")
    rows = [flat[start:start+5] for start in range(0, 25, 5)]
    # log(f"rows: {rows}\n")
    cols = [flat[start::5] for start in range(0, 5)]
    # log(f"cols: {cols}\n")
    lines = rows + cols
    # log(f"lines: {lines}\n")
    boards.append(Board(index, lines))
    index += 1

  [board.dump() for board in boards]
  return draws, boards

def parse(line):
  log(f"decode: {line}")
  raw_clues, raw_display = line.split('|')
  log(f"raw_clues: {raw_clues}")
  log(f"raw_display: {raw_display}")
  clues = [c for c in raw_clues.split()]
  log(f"clues: {clues}")
  display = [d for d in raw_display.split()]
  log(f"display: {display}")
  return clues, display

def find_by_length(clues, length):
  log(f"find_by_length({clues}, {length})... ")
  return [clue for clue in clues if len(clue) == length]

def difference(a, b):
  diff = set(a) - set(b)
  log(f"{set(a)} - {set(b)} => {diff}")
  log(f"{a} - {b} => {diff}")
  return diff.pop()

def solve(clues):


  # lengths = {clue: len(clue) for clue in clues}
  # lengths = {len(clue): clue for clue in clues}
  # log(f"lengths: {lengths}")

  one = find_by_length(clues, 2)[0]
  seven = find_by_length(clues, 3)[0]
  four = find_by_length(clues, 4)[0]
  eight = find_by_length(clues, 7)[0]
  print(f"one: {one}")
  print(f"seven: {seven}")
  print(f"four: {four}")
  print(f"eight: {eight}")

  segment2 = difference(seven, one)
  print(f"segment2: {segment2}")

  key = { 'ab': 1, 'abc':7 }

  log(f"key: {key}")
  return key

def decode(line):
  clues, display = parse(line)
  key = solve(clues)
  return 1

def main():
  total = 0

  for line in open(filename):
    total += decode(line)

  print(f"\nTotal: {total}")
  # assert total == 4512, "NOPE! the total should be 61229"

main()

