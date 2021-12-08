#! /usr/local/bin/python3
# filename = "input-test.txt"
filename = "input-solo.txt"
# filename = "input.txt"

from collections import Counter

debug = False
debug = True

def log(m):
  if debug: print(m)

def digits_with_length(clues, length):
  matches = [clue for clue in clues if len(clue) == length]
  log(f"digits_with_length({clues}, {length}) => {matches} ")
  return matches

def difference(a, b):
  diff = set(a) - set(b)
  # log(f"{a} - {b} => {diff}")
  return diff.pop()

def segments_not_in(s):
  not_in = set('abcdefg') - set(s)
  log(f"segments_not_in({s}) => {not_in}")
  return not_in

def digits_without(digits, c):
  log(f"digits_without({digits}, {c})...")
  matches = [digit for digit in digits if c not in digit]
  log(f"digits_without({digits}, {c})  => {matches}")
  return matches

def digits_with(digits, c):
  log(f"digits_with({digits}, {c}) ")
  matches = [digit for digit in digits if c in digit]
  log(f"digits_with({digits}, {c})  => {matches}")
  return matches

def has_both(clues, segments, a, b):
  log(f"has_both({clues}, {segments}, {a}, {b}) ")
  log(f" a: {segments[a]}")
  log(f" b: {segments[b]}")
  matches = set(digits_with(clues, segments[a])).intersection(set(digits_with(clues, segments[b])))
  log(f"has_both({clues}, {segments}, {segments[a]}, {segments[b]}) => {matches} <<<<<<<<<< ")
  return matches

def has_not(clues, segments, a):
  log(f"has_not({clues}, {segments}, {a}) ")
  log(f" a: {segments[a]}")
  matches = set(clues) - set(digits_with(clues, segments[a]))
  log(f"has_not({clues}, {segments}, {segments[a]}) => {matches} <<<<<<<<<< ")
  return matches


def solve(clues):
  seg_count = Counter()
  for clue in clues:
    seg_count += Counter(clue)
  log(f"seg_count: {seg_count}")

  segment_by_count = {}
  for char, count in seg_count.items():
    log(f"item: {char}, {count}")
    if count in segment_by_count.keys():  # there's prob a Python idiom for this:
      segment_by_count[count].append(char)
    else:
      segment_by_count[count] = [char]

  # segment_by_count = { num: char for char, num in seg_count.items() }
  log(f"segment_by_count: {segment_by_count}")

  segments = {}
  digits = {}

  # easy ones by length:
  digits[1] = digits_with_length(clues, 2)[0]
  digits[7] = digits_with_length(clues, 3)[0]
  digits[4] = digits_with_length(clues, 4)[0]
  digits[8] = digits_with_length(clues, 7)[0]

  # easy segments by count:
  segments[1] = segment_by_count[6][0]
  segments[4] = segment_by_count[4][0]
  segments[5] = segment_by_count[9][0]

  # now the tricky ones:
  segments[0] = difference(digits[7], digits[1])
  segments[2] = (set(segment_by_count[8]) - set([segments[0]])).pop()
  segments[6] = (set(segment_by_count[7]) - segments_not_in(digits[4])).pop()
  segments[3] = (set(segment_by_count[7]) - set(segments[6])).pop()

  # digits[2] = digits_without(clues, segments[5])[0]
  # print(f"digits[2]: {digits[2]}")

  # digits[3] = set(digits_with_length(clues, 5)).intersection(has_both(clues, segments, 2, 5)).pop()
  # print(f"digits[3]: {digits[3]}")

  # digits[5] = (set(digits_with_length(clues, 5)) - set([digits[2], digits[3]])).pop()
  # print(f"digits[5]: {digits[5]}")

  # digits[6] = set(digits_with_length(clues, 6)).intersection(has_both(clues, segments, 3, 4)).pop()
  # print(f"digits[6]: {digits[6]}")
  # digits[9] = set(digits_with_length(clues, 6)).intersection(has_both(clues, segments, 2, 3)).pop()
  # print(f"digits[9]: {digits[9]}")

  # digits[0] = set(digits_with_length(clues, 6)).intersection(has_both(clues, segments, 3)).pop()
  # print(f"digits[0]: {digits[0]}")
  #   shows:  has_both(['abcdefg', 'bcdef', 'acdfg', 'abcdf', 'abd', 'abcdef', 'bcdefg', 'abef', 'abcdeg', 'ab'], {1: 'e', 4: 'g', 5: 'b', 0: 'd', 2: 'a', 6: 'f', 3: 'c'}, a, g) => {'acdfg', 'abcdeg', 'abcdefg'} <<<<<<<<<<
  #           digits[0]: abcdeg

  digits[0] = set(digits_with_length(clues, 6)).intersection(has_not(clues, segments, 3)).pop()
  print(f"digits[0]: {digits[0]}")


  log(f"digits[3]: {digits[3]}")

  log(f"segments: {segments}")
  # log(f"segments resolved: {sorted(segments)}")

  wires = { wire: segment for segment, wire in segments.items() }
  log(f"wires: {wires}")

  log(f"digits: {digits}")
  key = { s: n for n, s in digits.items() }
  log(f"key: {key}")
  return key

def evalute(key, display):
  return 9999

def parse(line):
  log(f"decode: {line}")
  raw_clues, raw_display = line.split('|')
  log(f"raw_clues: {raw_clues}")
  log(f"raw_display: {raw_display}")
  clues = [''.join(sorted(c)) for c in raw_clues.split()]
  log(f"clues: {clues}")
  display = [''.join(sorted(d)) for d in raw_display.split()]
  log(f"display: {display}")
  return clues, display

def decode(line):
  clues, display = parse(line)
  key = solve(clues)
  return evalute(key, display)

def main():
  total = 0

  for line in open(filename):
    total += decode(line)

  print(f"\nTotal: {total}")
  # assert total == 61229, "NOPE! the total should be 61229"

main()

