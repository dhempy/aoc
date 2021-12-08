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

def digits_with_length(clues, length):
  matches = [clue for clue in clues if len(clue) == length]
  log(f"digits_with_length({clues}, {length}) => {matches} ")
  return matches

def difference(a, b):
  diff = set(a) - set(b)
  # log(f"{a} - {b} => {diff}")
  return diff.pop()

def segments_not_in(s):
  not_in = set('abcdefg') - set(s)
  log(f"segments_not_in({s}) => {not_in}")
  return not_in

def digits_without(digits, c):
  log(f"digits_without({digits}, {c})...")
  matches = [digit for digit in digits if c not in digit]
  log(f"digits_without({digits}, {c})  => {matches}")
  return matches

def digits_with(digits, c):
  matches = [digit for digit in digits if c in digit]
  log(f"digits_with({digits}, {c})  => {matches}")
  return matches

def solve(clues):
  seg_count = Counter()
  for clue in clues:
    seg_count += Counter(clue)
  log(f"seg_count: {seg_count}")

  segment_by_count = {}
  for char, count in seg_count.items():
    log(f"item: {char}, {count}")
    if count in segment_by_count.keys():  # there's prob a Python idiom for this:
      segment_by_count[count].append(char)
    else:
      segment_by_count[count] = [char]

  # segment_by_count = { num: char for char, num in seg_count.items() }
  log(f"segment_by_count: {segment_by_count}")

  segments = {}
  digits = {}

  segments[1] = segment_by_count[6][0]
  segments[4] = segment_by_count[4][0]
  segments[5] = segment_by_count[9][0]

  digits[1] = digits_with_length(clues, 2)[0]
  digits[7] = digits_with_length(clues, 3)[0]
  digits[4] = digits_with_length(clues, 4)[0]
  digits[8] = digits_with_length(clues, 7)[0]

  segments[0] = difference(digits[7], digits[1])
  segments[2] = (set(segment_by_count[8]) - set([segments[0]])).pop()
  segments[6] = set(segment_by_count[7]) - segments_not_in(digits[4])
  segments[3] = set(segment_by_count[7]) - set(segments[6])
  # segments[0] = segment_by_count[8]
  # segments[2] = segment_by_count[8]

  digits[2] = digits_without(clues, segments[5])[0]

  two_and_five = set(digits_with(clues, segments[2])).intersection(set(digits_with(clues, segments[5])))
  log(f"two_and_five: {two_and_five}")

  digits[3] = set(digits_with_length(clues, 5)
                ).intersection(
                  two_and_five
                ).pop()

  todo text: digits[5]
  todo text: digits[5]
  todo text: digits[5]
  todo text: digits[5]
  todo text: digits[5]

  log(f"digits[3]: {digits[3]}")

  segments[2] = segments[2]
  segments[6] = segments[6].pop()
  segments[3] = segments[3].pop()

  log(f"segments: {segments}")
  # log(f"segments resolved: {sorted(segments)}")

  wires = { wire: segment for segment, wire in segments.items() }
  log(f"wires: {wires}")
  log(f"wires['c'] : {wires['c'] }")

  log(f"digits: {digits}")
  key = { s: n for n, s in digits.items() }
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

