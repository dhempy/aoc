VALS = {
  'one' => 1,
  'two' => 2,
  'three' => 3,
  'four' => 4,
  'five' => 5,
  'six' => 6,
  'seven' => 7,
  'eight' => 8,
  'nine' => 9,
  '1' => 1,
  '2' => 2,
  '3' => 3,
  '4' => 4,
  '5' => 5,
  '6' => 6,
  '7' => 7,
  '8' => 8,
  '9' => 9,
}

ans = STDIN.each_line.map {  |line|
  first = line.match(/one|two|three|four|five|six|seven|eight|nine|1|2|3|4|5|6|7|8|9/).to_s
  last = line.reverse.match(/9|8|7|6|5|4|3|2|1|enin|thgie|neves|xis|evif|ruof|eerht|owt|eno/).to_s.reverse
  puts VALS[first]*10 + VALS[last]
  VALS[first]*10 + VALS[last]
}.sum

puts "Answer: #{ans}"
