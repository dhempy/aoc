#! /usr/local/bin/python3

# --- Day 11: Dumbo Octopus ---
#
# You enter a large cavern full of rare bioluminescent dumbo octopuses!
# They seem to not like the Christmas lights on your submarine, so you
# turn them off for now.
# Like: Game of life. Matrix math.

filename = "input-test.txt"
# filename = "input-solo.txt"
# filename = "input.txt"

# debug = False
debug = True

def log(m):
  if debug: print(m)

class Board:
  def __init__(self, filename):
    log(f"Board.init({filename}")
    self.filename = filename
    self.slurp()
    self.flash_count = 0
    self.day = 0

  def slurp(self):
    file = open(self.filename)
    self.flat = ''.join(file.read())
    log(f"flat: {self.flat}")

  def dump(self):
    if not debug: return
    log(Board.summary)

  def flash_count(self):
    return self.last_hit * sum(sum(self.lines[0:5], [])) # only the rows, not the (redundant) columns

  def summary(self):
    return f"Board {self.filename}: flash_count={self.flash_count()}"

  def advance(self):
    log(f"advance from day {self.day}")
    self.day += 1
    self.flash_count += 1

def main():
  board = Board(filename)
  board.dump()

  for day in range(100):
    board.advance()

  print(f"\nNumber of flashes: ")
  print(board.flash_count)
  # assert board.flash_count == 1656, "NOPE! Winning flash_count should be 1656"

main()

