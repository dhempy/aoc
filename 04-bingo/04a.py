#! /usr/local/bin/python3
# filename = "input-test.txt"
filename = "input-solo.txt"
# filename = "input.txt"

def find_winner(draws, boards):
  for draw in draws:
    for board in boards:
      if board.play_wins(draw): return board
  return None

class Board:
  def __init__(self, name, lines):
    print(f"Board.init({name}, {lines})...")
    self.name = name
    self.lines = lines

  def dump(self):
    print(f"Board {self.name}: score={self.score()}")
    for line in self.lines:
      print(f"  {line}")

  def score(self):
    return 987654321

  # plays a number (draw) on the board.
  # returns true if that draw was a winner.
  def play_wins(self, draw):
    print(f"Play {draw} on board {self.name}: ")
    self.dump()
    winner = False
    for line in self.lines:
      if draw in line:
        line.remove(draw)
        if not line: winner = True # but still need to remove draw from the other line.
    return winner

def slurp(filename):
  file = open(filename)
  draws = [int(i) for i in file.readline().split(',')]
  file.readline()
  # print(f"draws: {draws}")

  boards = []
  index = 0
  for grid in file.read().split('\n\n'):
    # print(f"grid: \n{grid}\n")
    string = ' '.join(grid.split('\n'))
    # print(f"string: {string}\n")
    flat = [int(i) for i in string.split()]
    # print(f"flat: {flat}\n")
    rows = [flat[start:start+5] for start in range(0, 25, 5)]
    # print(f"rows: {rows}\n")
    cols = [flat[start::5] for start in range(0, 5)]
    # print(f"cols: {cols}\n")
    lines = rows + cols
    # print(f"lines: {lines}\n")
    boards.append(Board(index, lines))
    index += 1

  return draws, boards

def main():
  draws, boards = slurp(filename)
  [board.dump() for board in boards]

  winner = find_winner(draws, boards)

  print(f"The winning board:")
  winner.dump()
  print(f"The winning board is {winner}, with a score of {score}")
  assert winner.score == 4512, "NOPE! Winning score should be 4512"
  # life_support_report(boards)

main()

