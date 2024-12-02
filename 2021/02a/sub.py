#! /usr/local/bin/python3
filename = "directions.txt"
file = open(filename, "r")

depth = 0
length = 0

for step in file:
  print(step.rstrip())
  [direction, distance] = step.split(' ')
  distance = int(distance)

  if direction == 'forward':
    length = length + distance
  elif direction == 'down':
    depth = depth + distance
  elif direction == 'up':
    depth = depth - distance

  print(f"  depth: {depth} length: {length} ")

area = depth * length
print(f"Final depth: {depth} length: {length} product area: {area} ")
