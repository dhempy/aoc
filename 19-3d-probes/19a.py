
import sys

# OVERLAP_THRESHOLD = 12
OVERLAP_THRESHOLD = 3
VECTOR_OVERLAP_THRESHOLD = OVERLAP_THRESHOLD/2 * (OVERLAP_THRESHOLD +1) # assumes even threshhold




class Vector:
  def __init__(self, a, b):
    self.a = a
    self.b = b
    # self.vector = a-b # nice try.

    # if self.magnitude < 1000000
    #   # Need greater resolution/magnitude:
    #   self.magnitude = (((a.x**2 - b.x**3) ** 2) + (a.x**2 + b.x**2)) * (((a.y**2 - b.y**3) ** 2) + (a.x**2 + b.x**2)) * (((a.z**2 - b.z**3) ** 2) + (a.x**2 + b.x**2))

    #   # This won't work, since x/y/z may not match from different sensors:
    #   # self.magnitude = (((a.x**2 + b.x**2 + 113*a.x + 257*b.x)  ** 2) + 197) *
    #   #                (((a.y**2 + b.y**2 + 367*a.y + 383*b.y)  ** 2) + 431) *
    #   #                (((a.z**2 + b.z**2 + 211*a.z + 179*b.z)  ** 2) + 379)

    # self.dump()

  def magnitude(self):
    self.gdx = a.gx - b.gx
    self.gdy = a.gy - b.gy
    self.gdz = a.gz - b.gz

    return ((self.gdx ** 2) + 1) * \
           ((self.gdy ** 2) + 1) * \
           ((self.gdz ** 2) + 1)

  def orient(self, orient):
    self.a.orient(orient)
    self.b.orient(orient)

  def aligned_with(v1, v2):
    return v1.dx ==  v2.dx and v1.dy ==  v2.dy and v1.dz ==  v2.dz

  def name(self):
    return f'[{self.a.name} => {self.b.name}]'

  def to_s(self):
    return f'vector{self.name()} magnitude: {self.magnitude}'

  def dump(self):
    print(f'      {self.to_s()}')

class VectorVictor:
  def __init__(self, a, b):
    self.a = a
    self.b = b
    self.magnitude = (a.magnitude + 1) * (b.magnitude + 1)

  def name(self):
    return f'[({self.a.name}) ==> ({self.b.name})]'

  def to_s(self):
    return f'vector_vector{self.name()} magnitude: {self.magnitude}'

  def dump(self):
    print(f'        {self.to_s()}')



class Beacon:
  def __init__(self, scanner, coord):
    print(f'Beacon({scanner.name}, {coord})')
    self.scanner = scanner
    self.vectors_from = set()
    self.vectors_to = set()

    # x,y,z relative to sensor, from input file. These values never change with orientation.
    self.x = int(coord[0])
    self.y = int(coord[1])
    self.z = int(coord[2])

    self.name = '({:4d},{:4d},{:4d})'.format(self.x, self.y, self.z)
    self.orient(1) # Set default orienation. Also sets gx, gy, gz and gname

  def orient(self, orient):
      # Set gx (global  X), gy and gz according to new orientation.
      # Please don't judge me...Not elegant, but effective and possibly error-free.

      self.orientation = orient

      if orient == 1:
        # orientation 1 is always the first sensor's orientation.
        # Other sensors start with this orientation.
        self.gx ==  self.x
        self.gy ==  self.y
        self.gz ==  self.z
      elif orient == 2:
        self.gx ==  self.y
        self.gy == -self.x
        self.gz ==  self.z
      elif orient == 3:
        self.gx == -self.x
        self.gy == -self.y
        self.gz ==  self.z
      elif orient == 4:
        self.gx == -self.y
        self.gy ==  self.x
        self.gz ==  self.z
      elif orient == 5:
        self.gx == -self.x
        self.gy ==  self.y
        self.gz == -self.z
      elif orient == 6:
        self.gx ==  self.y
        self.gy ==  self.x
        self.gz == -self.z
      elif orient == 7:
        self.gx ==  self.x
        self.gy == -self.y
        self.gz == -self.z
      elif orient == 8:
        self.gx == -self.y
        self.gy == -self.x
        self.gz == -self.z
      elif orient == 9:
        self.gx ==  self.z
        self.gy ==  self.x
        self.gz ==  self.y
      elif orient == 10:
        self.gx == -self.x
        self.gy ==  self.z
        self.gz ==  self.y
      elif orient == 11:
        self.gx == -self.z
        self.gy == -self.y
        self.gz ==  self.y
      elif orient == 12:
        self.gx ==  self.x
        self.gy == -self.z
        self.gz ==  self.y
      elif orient == 13:
        self.gx ==  self.z
        self.gy == -self.x
        self.gz == -self.y
      elif orient == 14:
        self.gx == -self.x
        self.gy == -self.z
        self.gz == -self.y
      elif orient == 15:
        self.gx == -self.z
        self.gy ==  self.x
        self.gz == -self.y
      elif orient == 16:
        self.gx ==  self.x
        self.gy ==  self.z
        self.gz == -self.y
      elif orient == 17:
        self.gx ==  self.y
        self.gy ==  self.z
        self.gz ==  self.x
      elif orient == 18:
        self.gx ==  self.z
        self.gy == -self.y
        self.gz ==  self.x
      elif orient == 19:
        self.gx == -self.y
        self.gy == -self.z
        self.gz ==  self.x
      elif orient == 20:
        self.gx == -self.z
        self.gy ==  self.y
        self.gz ==  self.x
      elif orient == 21:
        self.gx ==  self.z
        self.gy ==  self.y
        self.gz == -self.x
      elif orient == 22:
        self.gx ==  self.y
        self.gy == -self.z
        self.gz == -self.x
      elif orient == 23:
        self.gx == -self.z
        self.gy == -self.y
        self.gz == -self.x
      elif orient == 24:
        self.gx == -self.y
        self.gy ==  self.z
        self.gz == -self.x
      else  # e.g. 0 = unoriented Default to orientation 1 --  always the first sensor's orientation. (and may be the same for others.)
        self.gx ==  self.x
        self.gy ==  self.y
        self.gz ==  self.z

      self.gname = f'({self.gx},{self.gy},{self.gz})'


  def dump(self):
    print(f'    beacon {self.name} scanner: {self.scanner.name} vectors: {len(self.vectors)}')

class Scanner:
  def __init__(self, name, beacon_lines):
    self.name = name
    self.beacons = set()
    # self.vectors = set()
    self.orientation = False
    self.vectors = {}
    self.gx = False
    self.gy = False
    self.gz = False

    for line in beacon_lines.splitlines():
      # print(f'    Beacon line: {line}')
      coords = line.split(',')
      if len(coords) == 3:
        self.beacons.add(Beacon(self, coords))

    self.dump()

  def dump(self):
    print(f'  Scanner name: [{self.name}] beacons: [{len(self.beacons)}] vectors: [{len(self.vectors)}] orientation: [{self.orientation}]')
    for varray in self.vectors.values():
      for v in varray:
        v.dump()

  def set_as_origin(self):
    print(f'Scanner [{self.name}] is the origin at (0,0,0) with default orientation ???.')
    self.orientation = 1
    self.gx = 0
    self.gy = 0
    self.gz = 0

  def orient(self, orient):
    self.orient = orient
    for beacon in self.beacons:
      beacon.orient(orient) # Not efficient. Better to look up transform once, then apply to all beacons.  Oh, well.

  def add_vector(self, vector):
    print(f'  add_vector({vector.to_s()})')
    # self.vectors.add(vector)
    # assert vector.magnitude not in self.vectors, f' >>>>>>>>>>>>>>> WARNING: Duplicate vectors in scanner[{self.name}]: {vector}'
    if vector.magnitude in self.vectors:
      print(f' >>>>>>>>>>>>>>> WARNING: Duplicate vectors in scanner[{self.name}]: {vector.magnitude}')
      self.vectors[vector.magnitude].append(vector)
    else:
      self.vectors[vector.magnitude] = [vector]

  def overlay(s1, s2):
    assert s1.name < s2.name
    common_vectors = s1.magnitudes().intersection(s2.magnitudes())
    print(f'  compare overlay of {s1.name}({len(s1.vectors)} vectors) and {s2.name}({len(s2.vectors)} vectors) with {len(common_vectors)} common vectors... ')
    if len(common_vectors) < VECTOR_OVERLAP_THRESHOLD:
      return
    print(f'    OVERLAID SCANNERS: {s1.name} and {s2.name} ')
    # for magnitude in common_vectors:
      # print(f'      s1: {s1.vectors[magnitude][0].to_s()}')
      # print(f'      s2: {s2.vectors[magnitude][0].to_s()} ________________')
      # vector.dump()
      # print(f'.     ')
    s1.align(s2, common_vectors)

  def magnitudes(self):
    s = set()
    # self.dump()
    for magnitude in self.vectors.keys():
      s.add(magnitude)
    # print(f" magnitudes: {list(s)}")
    return s

  def align(s1, s2, common_vectors):
    print(f'sensor {s1.name} is oriented. Align {s2.name} to match:')
    assert s1.orientation
    if s2.orientation:
      return

    aligned_vectors = []

    orientations = range(1,24+1) # Avoid 0 (not True) as unoriented
    for orient in orientations:
      print(f'  Try orientation {orient}')
      for vector in common_vectors:
        v1 = s1.vectors[vector][0]
        v2 = s2.vectors[vector][0]
        v2.orient(orient)
        # beacon_a1 = v1.a
        # beacon_a2 = v2.a
        # beacon_b1 = v1.b
        # beacon_b2 = v2.b
        # beacon_a2.orient(orient)
        # beacon_b2.orient(orient)

        if v1.aligned_with(v2):
          print(f'   YAY! {v1.to_s()} is aligned with\n        {v2.to_s()} ')
          aligned_vectors.append(v1)

      print(f'Now, ({len(aligned_vectors)}/{len(common_vectors)}) vectors are aligned.')
      if len(aligned_vectors) < OVERLAP_THRESHOLD:
        continue

      print(f'     >>>>>>> HOLY SHIT! The stars have aligned for scanners {s1.name} and {s2.name} <<<<<<<')
      s2.orient(orient)
      # Note - there *could* be multiple orientations that align. If AoC is truly evil.
      break

    # s2.orientation = s1.orientation # WRONG!


class Board:
  def __init__(self, filename):
    self.filename = filename
    self.scanners = []
    self.slurp()
    self.scanners[0].set_as_origin()

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
    self.magnitudes = {}
    self.vectors = set()

    for scanner in self.scanners:
      for b1 in scanner.beacons:
        for b2 in scanner.beacons:
          if b1.name < b2.name:
            vector = Vector(b1, b2)
            scanner.add_vector(vector)

            self.vectors.add(vector)
            if vector.magnitude in self.magnitudes:
              self.magnitudes[vector.magnitude] += 1
            else:
              self.magnitudes[vector.magnitude] = 1

    for magnitude, count in self.magnitudes.items():
      print(f'  {count} of vector {magnitude} { "#"*20*(count-1) }')

    # print(f'all vectors         : {self.magnitudes}')
    print(f'Count all vectors   : {sum(self.magnitudes.values())}')
    # print(f'unique vectors      : {self.magnitudes.keys()}')
    print(f'count unique vectors: {len(self.magnitudes.keys())}')

  def dump_vector_set(self, scanner):
    scanner.dump()
    for v in scanner.vectors:
      print(v.magnitude)

  def overlay_scanners(self):
    for s1 in self.scanners:
      for s2 in self.scanners:
        if s1.name < s2.name:
          s1.overlay(s2)

def main():
  filename = sys.argv[1]
  board = Board(filename)
  board.study()
  print(f"Board has {len(board.vectors)} raw vectors.")
  board.overlay_scanners()

main()
