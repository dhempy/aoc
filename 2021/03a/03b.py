#! /usr/local/bin/python3
# filename = "tiny_power.txt"
filename = "power.txt"

def count_ones(list, bit_count):
  # Count of how many (1) bits are in each column (binary position)
  # of the input lines.
  ones = [0] * bit_count

  for binary in list:
    # print(f"\nReading: {binary}")
    for index, bit in enumerate(binary):
      # print(f"{index}: {bit}")
      if bit == '1':
        # print("Another one!")
        ones[index] += 1

    # print(ones)

  return ones



def energy_report(all_readings):
  line_count = len(all_readings)
  bit_count = len(all_readings[0])

  ones = count_ones(all_readings, bit_count)

  gamma_rate = 0
  epsilon_rate = 0
  threshold = int(line_count / 2)
  o2_matcher = [] # Collects most-common values.
  co2_matcher = [] # Collects least-common values.

  for one_count in ones:
    gamma_rate *= 2
    epsilon_rate *= 2
    if one_count >= threshold:
      print(f"is {one_count} >= {threshold}? Yes.")
      gamma_rate += 1
    else:
      print(f"is {one_count} >= {threshold}? No.")
      epsilon_rate += 1

  print(f"gamma_rate: {gamma_rate}")
  print(f"epsilon_rate: {epsilon_rate}")

  total_power = gamma_rate * epsilon_rate
  print(f"total_power: {total_power}")


def life_support_report(all_readings):
  bit_count = len(all_readings[0])

  oxygen_list = list(all_readings)
  for column in range(bit_count):
    oxygen_list = comb(oxygen_list, column, 'most_common')
    if len(oxygen_list) <= 1:
      break

  o2_generator_rating = int(oxygen_list[0], 2)
  print(f"O2 generator value: {o2_generator_rating}")


  co2_list = list(all_readings)
  for column in range(bit_count):
    co2_list = comb(co2_list, column, 'least_common')
    if len(co2_list) <= 1:
      break

  co2_scrubber_rating = int(co2_list[0], 2)
  print(f"CO2 scrubber value: {co2_scrubber_rating}")

  life_support_rating = o2_generator_rating * co2_scrubber_rating
  print(f"Life support rating: {life_support_rating}")


######### Now, O2/CO2 readings:

# Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. Discard numbers which do not match the bit criteria.

# If you only have one number left, stop; this is the rating value for which you are searching.

# Otherwise, repeat the process, considering the next bit to the right.


# To find oxygen generator rating,
# determine the most common value (0 or 1) in the current bit position,
# keep only numbers with that bit in that position.
# If 0 and 1 are equally common, keep values with a 1 in the
# position being considered.

def matcher(ones, column, line_count, match_type):
  half = line_count / 2 # Okay if this is a half-step float value.
  # print(f"matcher({ones}, {column}, {line_count}, {match_type})... half={half}")
  if ones[column] >= half:
    # print(f"is {ones[column]} >= {half}? Yes.")
    return '1' if match_type == 'most_common' else '0'
  else:
    # print(f"is {ones[column]} >= {half}? No.")
    return '0' if match_type == 'most_common' else '1'

def comb(input_list, column, match_type):
  line_count = len(input_list)
  bit_count = len(input_list[0])
  ones = count_ones(input_list, bit_count)
  match_val = matcher(ones, column, line_count, match_type)

  # print(f"comb({input_list}, {column}, match_val:{match_val})")
  new_list = [val for val in input_list if val[column] == match_val]
  print(f"combed list:{new_list} ")
  return new_list


def slurp_file(filename):
  with open(filename) as file:
      all_readings = [line.rstrip() for line in file]
  all_readings = [r for r in all_readings if r] # Remove empties.

  line_count = len(all_readings)
  bit_count = len(all_readings[0])
  print(f"{line_count} readings found.")
  print(f"Readings have {bit_count} bits.")

  # for reading in all_readings:
  #   print(reading)
  # print()
  return all_readings

def main():
  all_readings = slurp_file(filename)
  energy_report(all_readings)
  life_support_report(all_readings)

main()

