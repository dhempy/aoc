#! /usr/local/bin/python3
# filename = "input-test.txt"
# filename = "input-solo.txt"
# filename = "input.0123.txt"
# filename = "input.4567.txt"
# filename = "input.8989.txt"
filename = "input.txt"

from collections import Counter

debug = False
# debug = True

def log(m):
  if debug: print(m)

def digits_with_length(clues, length):
  # for clue in clues:
  #   print(f"clue: {clue} len: {len(clue)}")

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
  segments[6] = set(segment_by_count[7]).intersection(segments_not_in(digits[4])).pop()
  segments[3] = (set(segment_by_count[7]) - set(segments[6])).pop()

  digits[2] = digits_without(clues, segments[5])[0]
  digits[3] = set(digits_with_length(clues, 5)).intersection(has_both(clues, segments, 2, 5)).pop()
  digits[5] = (set(digits_with_length(clues, 5)) - set([digits[2], digits[3]])).pop()
  digits[6] = set(digits_with_length(clues, 6)).intersection(has_both(clues, segments, 3, 4)).pop()
  digits[9] = set(digits_with_length(clues, 6)).intersection(has_both(clues, segments, 2, 3)).pop()
  digits[0] = (set(digits_with_length(clues, 6)) - set([digits[6], digits[9]])).pop()

  log(f"segments: {sorted(segments)}")

  wires = { wire: segment for segment, wire in segments.items() }
  log(f"wires: {sorted(wires)}")

  log(f"digits: {sorted(digits)}")
  key = { s: n for n, s in digits.items() }
  log(f"key: {sorted(key)}")

  # these work only when wires are not crossed: (e.g. input.0123.txt)
  log(f"expect segment 0 to eq a == {segments[0]} => {'a' == segments[0]}")
  log(f"expect segment 1 to eq b == {segments[1]} => {'b' == segments[1]}")
  log(f"expect segment 2 to eq c == {segments[2]} => {'c' == segments[2]}")
  log(f"expect segment 3 to eq d == {segments[3]} => {'d' == segments[3]}")
  log(f"expect segment 4 to eq e == {segments[4]} => {'e' == segments[4]}")
  log(f"expect segment 5 to eq f == {segments[5]} => {'f' == segments[5]}")
  log(f"expect segment 6 to eq g == {segments[6]} => {'g' == segments[6]}")

  # these work only when wires are not crossed: (e.g. input.0123.txt)
  log(f"expect digit 0 to eq abcefg == {digits[0]} => {'abcefg' == digits[0]}")
  log(f"expect digit 1 to eq cf == {digits[1]} => {'cf' == digits[1]}")
  log(f"expect digit 2 to eq acdeg == {digits[2]} => {'acdeg' == digits[2]}")
  log(f"expect digit 3 to eq acdfg == {digits[3]} => {'acdfg' == digits[3]}")
  log(f"expect digit 4 to eq bcdf == {digits[4]} => {'bcdf' == digits[4]}")
  log(f"expect digit 5 to eq abdfg == {digits[5]} => {'abdfg' == digits[5]}")
  log(f"expect digit 6 to eq abdefg == {digits[6]} => {'abdefg' == digits[6]}")
  log(f"expect digit 7 to eq acf == {digits[7]} => {'acf' == digits[7]}")
  log(f"expect digit 8 to eq abcdefg == {digits[8]} => {'abcdefg' == digits[8]}")
  log(f"expect digit 9 to eq abcdfg == {digits[9]} => {'abcdfg' == digits[9]}")

  return key

def evalute(key, display):
  output = ''
  for s in display:
    # digit = str(key[s])
    output = f"{output}{key[s]}"
    # total = digit + total * 10
  log(f"evalute({key}, {display}) => {output} ")
  print(output)
  return output

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
    total += int(decode(line))

  print(f"\nTotal: {total}")
  # assert total == 61229, "NOPE! the total should be 61229"

main()

