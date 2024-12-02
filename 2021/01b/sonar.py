#! /usr/local/bin/python3
filename = "depths.txt"
file = open(filename, "r")

descents = 0
prev = -1

agr_descents = 0
agr_prev = -1
readings = [-1,-1,-1]
line_num = 0
sample_size = 3

for depth in file:
  depth = int(depth)
  print(depth)

  # Single readings:
  if depth > prev and prev > 0:
    print(f"  descending {prev} -> {depth}")
    descents = descents + 1
  else:
    print(f"   ASCENDING {prev} -> {depth}")
  prev = depth

  # Aggregate readings:
  index = line_num % sample_size
  readings[index] = depth
  reading = sum(readings)

  if line_num >= sample_size:
    reading = sum(readings)
    if reading > agr_prev:
      print(f"  descending {agr_prev} -> {reading}. (sum: {readings})")
      agr_descents += 1
    else:
      print(f"   ASCENDING {agr_prev} -> {reading}. (sum: {readings})")
    agr_prev = reading

  line_num = line_num + 1

print(f"Descended {descents} times.")
print(f"Descended {agr_descents} times. ({sample_size}-sum)")
