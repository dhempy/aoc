#! /usr/local/bin/python3
filename = "input-test.txt"
# filename = "input.txt"

def cheat(picks, boards):
  return 13, 12345678

class Board:
  def __init__(self, name, lines):
    self.name = name
    self.lines = lines

  def dump(self):
    print(f"Board {self.name}: {len(self.lines)} lines")
    for line in self.lines:
      print(f"  {line}")


def slurp(filename):
  file = open(filename)
  picks = file.readline().split(',')
  file.readline()
  print(f"picks: {picks}")

  boards = []
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
    print(f"lines: {lines}\n")
    boards.append(Board("John", lines))

  print(f"boards: {boards}")

  return picks, boards

def main():
  picks, boards = slurp(filename)
  for board in boards:
    board.dump()
    # print(f"Board {board.name}: {len(board.lines)} lines: {board.lines} ")
  # print(boards)

  winner, score = cheat(picks, boards)

  print(f"The winning board is {winner}, with a score of {score}")
  assert winning_score == 4512, "NOPE! Winning score should be 4512"
  # life_support_report(boards)

main()

