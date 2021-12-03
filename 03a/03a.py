#! /usr/local/bin/python3
filename = "power.txt"
# filename = "tiny_power.txt"
file = open(filename, "r")

ones = []
lines = 0
line_num = 0
bit_count = -1

for power in file:
  print(power.rstrip())
  lines += 1

  if bit_count < 0:
    bit_count = len(power)-1
    print(f"Initialize array to {bit_count} items.")
    ones = [0] * bit_count
    print(ones)

  for index, bit in enumerate(power):
    print(f"{index}: {bit}")
    if bit == '1':
      print("increment")
      ones[index] += 1

    print(ones)

gamma_rate = 0
epsilon_rate = 0
threshold = int(lines / 2)

for one_count in ones:
  gamma_rate *= 2
  epsilon_rate *= 2
  if one_count >= threshold:
    gamma_rate += 1
  else:
    epsilon_rate += 1

print(f"gamma_rate: {gamma_rate}")
print(f"epsilon_rate: {epsilon_rate}")

total_power = gamma_rate * epsilon_rate
print(f"total_power: {total_power}")
