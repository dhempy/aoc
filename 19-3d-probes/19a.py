
import sys

OVERLAP_THRESHOLD = 12
# OVERLAP_THRESHOLD = 6

class Vector:
  def __init__(self, a, b):
    self.a = a
    self.b = b
    # self.vector = a-b # nice try.

    # if self.magnitude() < 1000000
    #   # Need greater resolution/magnitude:
    #   self.magnitude() = (((a.x**2 - b.x**3) ** 2) + (a.x**2 + b.x**2)) * (((a.y**2 - b.y**3) ** 2) + (a.x**2 + b.x**2)) * (((a.z**2 - b.z**3) ** 2) + (a.x**2 + b.x**2))

    #   # This won't work, since x/y/z may not match from different sensors:
    #   # self.magnitude() = (((a.x**2 + b.x**2 + 113*a.x + 257*b.x)  ** 2) + 197) *
    #   #                (((a.y**2 + b.y**2 + 367*a.y + 383*b.y)  ** 2) + 431) *
    #   #                (((a.z**2 + b.z**2 + 211*a.z + 179*b.z)  ** 2) + 379)

    # self.dump()

  def magnitude(self):
    # gdx = global difference in X between points
    self.gdx = self.a.gx - self.b.gx
    self.gdy = self.a.gy - self.b.gy
    self.gdz = self.a.gz - self.b.gz

      # This calc must not treat  x,y, and z positionally. They must work in any order.
    return ((self.gdx ** 2) + 1) * \
           ((self.gdy ** 2) + 1) * \
           ((self.gdz ** 2) + 1)

  def orient(self, orientation):
    self.a.orient(orientation)
    self.b.orient(orientation)

  def aligned_with(v1, v2):
    print(f'    aligned_with? v1:{v1.to_s()} v2:{v2.to_s()}')
    return v1.gdx == v2.gdx and v1.gdy == v2.gdy and v1.gdz == v2.gdz

  def name(self):
    return f'[{self.a.name} => {self.b.name}]'

  def to_s(self):
    return f'vector{self.name()} magnitude: {self.magnitude()}'

  def dump(self):
    print(f'      {self.to_s()}')


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
    self.orient() # Set default orienation. Also sets gx, gy, gz and gname

  def orient(self, orientation = 0):
      # Set gx (global  X), gy and gz according to new orientation.
      # Please don't judge me...Not elegant, but effective and possibly error-free.

      self.orientation = orientation

      if orientation == 1 or orientation == 0:
        # orientation 1 is always the first sensor's orientation.
        # orientation 0 behaves identically, but flags as not oriented.
        self.gx =  self.x
        self.gy =  self.y
        self.gz =  self.z
      elif orientation == 2:
        self.gx =  self.y
        self.gy = -self.x
        self.gz =  self.z
      elif orientation == 3:
        self.gx = -self.x
        self.gy = -self.y
        self.gz =  self.z
      elif orientation == 4:
        self.gx = -self.y
        self.gy =  self.x
        self.gz =  self.z
      elif orientation == 5:
        self.gx = -self.x
        self.gy =  self.y
        self.gz = -self.z
      elif orientation == 6:
        self.gx =  self.y
        self.gy =  self.x
        self.gz = -self.z
      elif orientation == 7:
        self.gx =  self.x
        self.gy = -self.y
        self.gz = -self.z
      elif orientation == 8:
        self.gx = -self.y
        self.gy = -self.x
        self.gz = -self.z
      elif orientation == 9:
        self.gx =  self.z
        self.gy =  self.x
        self.gz =  self.y
      elif orientation == 10:
        self.gx = -self.x
        self.gy =  self.z
        self.gz =  self.y
      elif orientation == 11:
        self.gx = -self.z
        self.gy = -self.y
        self.gz =  self.y
      elif orientation == 12:
        self.gx =  self.x
        self.gy = -self.z
        self.gz =  self.y
      elif orientation == 13:
        self.gx =  self.z
        self.gy = -self.x
        self.gz = -self.y
      elif orientation == 14:
        self.gx = -self.x
        self.gy = -self.z
        self.gz = -self.y
      elif orientation == 15:
        self.gx = -self.z
        self.gy =  self.x
        self.gz = -self.y
      elif orientation == 16:
        self.gx =  self.x
        self.gy =  self.z
        self.gz = -self.y
      elif orientation == 17:
        self.gx =  self.y
        self.gy =  self.z
        self.gz =  self.x
      elif orientation == 18:
        self.gx =  self.z
        self.gy = -self.y
        self.gz =  self.x
      elif orientation == 19:
        self.gx = -self.y
        self.gy = -self.z
        self.gz =  self.x
      elif orientation == 20:
        self.gx = -self.z
        self.gy =  self.y
        self.gz =  self.x
      elif orientation == 21:
        self.gx =  self.z
        self.gy =  self.y
        self.gz = -self.x
      elif orientation == 22:
        self.gx =  self.y
        self.gy = -self.z
        self.gz = -self.x
      elif orientation == 23:
        self.gx = -self.z
        self.gy = -self.y
        self.gz = -self.x
      elif orientation == 24:
        self.gx = -self.y
        self.gy =  self.z
        self.gz = -self.x
      else:  # e.g. 0 = unoriented Default to orientation 1 --  always the first sensor's orientation. (and may be the same for others.)
        raise ValueError(f"Bad orientation: {orientation}")

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

  def orient(self, orientation = 0):
    # zero indicates unoriented, but aligns as orientation = 1
    self.orientation = orientation
    for beacon in self.beacons:
      beacon.orient(orientation) # Not efficient. Better to look up transform once, then apply to all beacons.  Oh, well.

  def add_vector(self, vector):
    print(f'  add_vector({vector.to_s()})')
    # self.vectors.add(vector)
    # assert vector.magnitude() not in self.vectors, f' >>>>>>>>>>>>>>> WARNING: Duplicate vectors in scanner[{self.name}]: {vector}'
    if vector.magnitude() in self.vectors:
      print(f' >>>>>>>>>>>>>>> WARNING? Duplicate vectors in scanner[{self.name}]: {vector.magnitude()}. <<<<<<<<<<<<<<<<<<<<< ')
      self.vectors[vector.magnitude()].append(vector)
    else:
      self.vectors[vector.magnitude()] = [vector]

  def vector_beacons(self, magnitudes):
    beacons = set()
    for mag in magnitudes:
      vector = self.vectors[mag][0] # this will break if a scanner ever has duplicate vectors.
      beacons.add(vector.a)
      beacons.add(vector.b)
    print(f'   {len(beacons)} matching beacons for scanner[{self.name}]: {list(beacons)} ')
    return beacons

  def vector_beacon_count(self, magnitudes):
    beacons = self.vector_beacons(magnitudes)
    if beacons:
      return len(beacons)
    else:
      return 0

  def overlay(s1, s2):
    assert s1.name < s2.name
    common_magnitudes = s1.magnitudes().intersection(s2.magnitudes())
    print(f'  compare overlay of {s1.name}({len(s1.vectors)} vectors) and {s2.name}({len(s2.vectors)} vectors) with {len(common_magnitudes)} common vectors and {s1.vector_beacon_count(common_magnitudes)}+{s2.vector_beacon_count(common_magnitudes)} common beacons... ')
    if s1.vector_beacon_count(common_magnitudes) < OVERLAP_THRESHOLD or s2.vector_beacon_count(common_magnitudes) < OVERLAP_THRESHOLD:
      return
    print(f'\n    OVERLAID SCANNERS: {s1.name} and {s2.name} ')
    s1.align(s2, common_magnitudes)

  def magnitudes(self):
    s = set()
    # self.dump()
    for magnitude in self.vectors.keys():
      s.add(magnitude)
    # print(f" magnitudes: {list(s)}")
    return s

  def align(s1, s2, common_magnitudes):
    print(f'scanner[{s1.name}] is oriented to [{s1.orientation}]. Find orientation to align scanner[{s2.name}] with it...')
    if not s1.orientation:
      print(f'Not attempting alignment because first scanner[{s1.name}] is NOT oriented.')
      return
    if not s1.orientation or s2.orientation:
      print(f'Not attempting alignment because second scanner[{s2.name}] is ALREADY oriented.')
      return

    aligned_vectors = []
    best_orientation = 0
    best_so_far = 0

    orientations = range(1,24+1) # Avoid 0 (not True) as unoriented
    for orientation in orientations:
      print(f'  Try orientation {orientation}')
      s2.orient(orientation)
      aligned_vectors = []

      for mag in common_magnitudes:
        v1 = s1.vectors[mag][0] # this will break if a scanner ever has duplicate vectors.
        v2 = s2.vectors[mag][0] # this will break if a scanner ever has duplicate vectors.

        if v1.aligned_with(v2):
          print(f'   YAY! {v1.to_s()} is aligned with\n        {v2.to_s()} ')
          aligned_vectors.append(mag)

      beacon_count = s1.vector_beacon_count(aligned_vectors)
      print(f'Now, ({len(aligned_vectors)}/{len(common_magnitudes)}) vectors are aligned and {beacon_count} beacons are aligned')

      if beacon_count < OVERLAP_THRESHOLD or beacon_count < best_so_far:
        continue

      print(f'     >>>>>>> HOLY SHIT! The stars have aligned for scanners {s1.name}(orientation {s1.orientation}) and {s2.name}(new orientation {orientation}) <<<<<<< ({beacon_count} >= thresh {OVERLAP_THRESHOLD})\n')
      s2.orient(orientation)
      best_so_far = beacon_count
      best_orientation = orientation

    if best_so_far == 0:
      print(f'  Did not find an orientation for sensor[{s1.name}] and sensor[{s2.name}]. \n')
    s2.orient(best_orientation) # zero if none found.
    print(f'     >>>>>>> FINALLY! Orienting scanner[{s2.name}] to final orientation {best_orientation} <<<<<<<\n')


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
            if vector.magnitude() in self.magnitudes:
              self.magnitudes[vector.magnitude()] += 1
            else:
              self.magnitudes[vector.magnitude()] = 1

    for magnitude, count in self.magnitudes.items():
      print(f'  {count} of vector {magnitude} { "#"*20*(count-1) }')

    # print(f'all vectors         : {self.magnitudes}')
    print(f'Count all vectors   : {sum(self.magnitudes.values())}')
    # print(f'unique vectors      : {self.magnitudes.keys()}')
    print(f'count unique vectors: {len(self.magnitudes.keys())}')

  def dump_vector_set(self, scanner):
    scanner.dump()
    for v in scanner.vectors:
      print(v.magnitude())

  def overlay_scanners(self):
    for s1 in self.scanners:
      for s2 in self.scanners:
        if s1.name < s2.name:
          s1.overlay(s2)

  def show_orientations(self):
    for s in self.scanners:
      print(f'  Scanner[{s.name}] orientation: {s.orientation} ')

def main():
  filename = sys.argv[1]
  board = Board(filename)
  board.study()
  print(f"Board has {len(board.vectors)} raw vectors.")
  board.overlay_scanners()
  board.show_orientations()

main()
