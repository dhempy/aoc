#! /usr/local/bin/python3
# filename = "input-test.txt"
# filename = "input-solo.txt"
filename = "input.txt"

debug = False
# debug = True

def log(m):
  if debug: print(m)

def find_winner(draws, boards):
  for draw in draws:
    for board in boards:
      if board.play(draw): return board
  return None

def find_loser(draws, boards):
  for draw in draws:
    for board in reversed(boards): # reversed so removing doesn't foobar iteration.
      if board.play(draw):
        log(f"ELIMINATED: {board.summary()}")
        if len(boards) > 1:
          log("ANOTHER REMAINS...")
          boards.remove(board)
        else:
          log("WE HAVE A WINNER!")
          return board
  return None

class Board:
  def __init__(self, name, lines):
    log(f"Board.init({name}, {lines})...")
    self.name = name
    self.lines = lines
    self.last_hit = 0

  def dump(self):
    if not debug: return
    log(f"Board {self.name}: last_hit:{self.last_hit} score={self.score()}")
    for line in self.lines:
      log(f"  {line}")

  def score(self):
    return self.last_hit * sum(sum(self.lines[0:5], [])) # only the rows, not the (redundant) columns

  def summary(self):
    return f"Board {self.name}: score={self.score()}"


  # plays a number (draw) on the board.
  # returns true if that draw was a winner.
  def play(self, draw):
    log(f"Play {draw} on board {self.name}: ")
    self.dump()

    winner = False
    for line in self.lines:
      if draw in line:
        line.remove(draw)
        self.last_hit = draw
        if not line: winner = True # but still need to remove draw from the other line.
    return winner

def slurp(filename):
  file = open(filename)
  draws = [int(i) for i in file.readline().split(',')]
  file.readline()
  log(f"draws: {draws}")

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

def main():
  draws, boards = slurp(filename)
  loser = find_loser(draws, boards)

  loser.dump()

  print(f"\nThe losing board: ")
  print(loser.summary())
  assert loser.score == 1924, "NOPE! Winning score should be 1924"

main()

