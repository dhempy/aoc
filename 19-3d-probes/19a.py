
import sys

class Vector:
  def __init__(self, a, b):
    self.a = a
    self.b = b
    self.product = (((a.x - b.x) ** 2) + 1) * (((a.y - b.y) ** 2) + 1) * (((a.z - b.z) ** 2) + 1)
    self.dump()

  def dump(self):
    print(f'      vector [{self.a.name} => {self.b.name}] product: {self.product}')

class Beacon:
  def __init__(self, scanner, coord):
    print(f'Beacon({scanner.name}, {coord})')
    self.x = int(coord[0])
    self.y = int(coord[1])
    self.z = int(coord[2])
    self.name = f'({self.x},{self.y},{self.z})'
    self.scanner = scanner
    self.vectors = set()
    self.dump()

  def dump(self):
    print(f'    beacon {self.name} scanner: {self.scanner.name} vectors: {len(self.vectors)}')

class Scanner:
  def __init__(self, name, beacon_lines):
    self.name = name
    self.beacons = set()
    self.vectors = set()

    for line in beacon_lines.splitlines():
      # print(f'    Beacon line: {line}')
      coords = line.split(',')
      if len(coords) == 3:
        self.beacons.add(Beacon(self, coords))

    self.dump()

  def dump(self):
    print(f'  Scanner name: [{self.name}] beacons: [{len(self.beacons)}] vectors: [{len(self.vectors)}]')

class Board:
  def __init__(self, filename):
    self.filename = filename
    self.scanners = []
    self.slurp()


  def slurp(self):
    print(f'Reading file [{self.filename}]')
    file = open(self.filename)
    for scanner_text in file.read().split('--- scanner '):
      # print(f'scanner_text: [{scanner_text}] (len -> {len(scanner_text)})')
      if not scanner_text:
        continue
      name, beacon_lines = scanner_text.split(' ---\n')
      print(f'Scanner name: [{name}] beacon_lines: [{beacon_lines}]')

      self.scanners.append(Scanner(name, beacon_lines))


  def study(self):
    for scanner in self.scanners:
      for b1 in scanner.beacons:
        for b2 in scanner.beacons:
          scanner.vectors.add(Vector(b1, b2))   # vectors is a set

  def overlay(self):
    for s1 in self.scanners:
      for s2 in self.scanners:
        if s1 == s2:
          next
        common_vectors = s1.vectors.intersection(s2.vectors)
        if len(common_vectors) < 12:
          next
        print('OVERLAID SCANNERS!')

def main():
  filename = sys.argv[1]
  board = Board(filename)
  board.study()

main()
