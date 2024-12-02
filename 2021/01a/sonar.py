#! /usr/local/bin/python3
filename = "depths.txt"
file = open(filename, "r")

descents = 0
prev = -1

for depth in file:
  depth = int(depth)
  print(depth)

  if depth > prev and prev > 0:
    print("descending.")
    descents = descents + 1
  prev = depth

print(f"Descended {descents} times.")
