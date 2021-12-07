#! /usr/local/bin/python3
# filename = "tiny_crabs.txt"
# filename = "2_crabs.txt"
filename = "crabs.txt"

from collections import Counter
import sys

def one_crab_cost(src, dest):
  return abs(src - dest)

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

  # Iterate range
  for dest in range(here,there):
    # print(f"Try it at {dest}...")
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
  # print(crabs)

  energy_report(crabs)
  # life_support_report(crabs)

main()


# --- Day 7: The Treachery of Whales --- A giant whale has decided your
#     submarine is its next meal, and it's much faster than you are. There's
#     nowhere to run!

# Suddenly, a swarm of crabs (each in its own tiny submarine - it's too deep for
# them otherwise) zooms in to rescue you! They seem to be preparing to blast a
# hole in the ocean floor; sensors indicate a massive underground cave system
# just beyond where they're aiming!

# The crab submarines all need to be aligned before they'll have enough power to
# blast a large enough hole for your submarine to get through. However, it
# doesn't look like they'll be aligned before the whale catches you! Maybe you
# can help?

# There's one major catch - crab submarines can only move horizontally.

# You quickly make a list of the horizontal position of each crab (your puzzle
# input). Crab submarines have limited fuel, so you need to find a way to make
# all of their horizontal positions match while requiring them to spend as
# little fuel as possible.

# For example, consider the following horizontal positions:

# 16,1,2,0,4,2,7,1,2,14 This means there's a crab with horizontal position 16, a
# crab with horizontal position 1, and so on.

# Each change of 1 step in horizontal position of a single crab costs 1 fuel.
# You could choose any horizontal position to align them all on, but the one
# that costs the least fuel is horizontal position 2:

# Move from 16 to 2: 14 fuel Move from 1 to 2: 1 fuel Move from 2 to 2: 0 fuel
# Move from 0 to 2: 2 fuel Move from 4 to 2: 2 fuel Move from 2 to 2: 0 fuel
# Move from 7 to 2: 5 fuel Move from 1 to 2: 1 fuel Move from 2 to 2: 0 fuel
# Move from 14 to 2: 12 fuel This costs a total of 37 fuel. This is the
# cheapest possible outcome; more expensive outcomes include aligning at
# position 1 (41 fuel), position 3 (39 fuel), or position 10 (71 fuel).

# Determine the horizontal position that the crabs can align to using the least
# fuel possible. How much fuel must they spend to align to that position?
