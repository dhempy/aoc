#! /usr/local/bin/python3
filename = "crabs.txt"
# filename = "tiny_crabs.txt"
# filename = "2_crabs.txt"

from collections import Counter
import sys

def one_crab_cost(src, dest):
  diff = abs(src - dest)
  return int((diff+1) * diff/2)

  # 1: 1 = 1                 = 2*1.5  = (diff+1) * diff/2
  # 2: 3 = 1 + 2             = 3*1    = (diff+1) * diff/2
  # 3: 6 = 1 + 2 + 3         = 4*1.5  = (diff+1) * diff/2
  # 4: 10= 1 + 2 + 3 + 4     = 5*2    = (diff+1) * diff/2
  # 5: 15= 1 + 2 + 3 + 4 + 5 = 6*2.5  = (diff+1) * diff/2

  # for x in range(9):
  #   print(f"steps:{x} costs:{one_crab_cost(0, x)}")

def crab_cost(crabs, dest):
  total_cost = 0
  for src, count in crabs.items():
    cost = one_crab_cost(src, dest)
    group_cost = cost * count
    # print(f"from {src} to {dest} costs {cost}, times {count} crabs is {group_cost}")
    total_cost += group_cost
  return total_cost

def energy_report(crabs):
  # find range
  here = min(crabs.keys())
  there = max(crabs.keys())+1
  best_cost = sys.maxsize

  for dest in range(here, there):
    cost = crab_cost(crabs, dest)
    if(cost < best_cost):
      print(f"New best cost: {cost} at location {dest} (was {best_cost})")
      best_cost = cost
      best_location = dest

  print(f"BEST LOCATION is {best_location}, with a cost of {best_cost}. ")

def slurp(filename):
  return Counter(map(int,open(filename).read().split(',')))

def main():
  crabs = slurp(filename)
  energy_report(crabs)

main()


# --- Part Two ---

# The crabs don't seem interested in your proposed solution. Perhaps you
# misunderstand crab engineering?

# As it turns out, crab submarine engines don't burn fuel at a constant rate.
# Instead, each change of 1 step in horizontal position costs 1 more unit of
# fuel than the last: the first step costs 1, the second step costs 2, the
# third step costs 3, and so on.

# As each crab moves, moving further becomes more expensive. This changes the
# best horizontal position to align them all on; in the example above, this
# becomes 5:

# Move from 16 to 5: 66 fuel
# Move from 1 to 5: 10 fuel
# Move from 2 to 5: 6 fuel
# Move from 0 to 5: 15 fuel
# Move from 4 to 5: 1 fuel
# Move from 2 to 5: 6 fuel
# Move from 7 to 5: 3 fuel
# Move from 1 to 5: 10 fuel
# Move from 2 to 5: 6 fuel
# Move from 14 to 5: 45 fuel
# This costs a total of 168 fuel.
#   This is the new cheapest possible outcome; the old alignment
#   position (2) now costs 206 fuel instead.

# Determine the horizontal position that the crabs can align to using the
# least fuel possible so they can make you an escape route! How much fuel
# must they spend to align to that position?

