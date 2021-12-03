#! /usr/local/bin/python3
filename = "directions.txt"
file = open(filename, "r")

depth = 0
length = 0
aim = 0

for step in file:
  print(step.rstrip())
  [direction, delta] = step.split(' ')
  delta = int(delta)

  if direction == 'forward':
    length = length + delta
    depth = depth + delta * aim
  elif direction == 'down':
    aim = aim + delta
  elif direction == 'up':
    aim = aim - delta

  area = depth * length
  print(f"  depth: {depth} length: {length} aim: {aim} product area: {area} ")

print(f"Final depth: {depth} length: {length} aim: {aim} product area: {area} ")
