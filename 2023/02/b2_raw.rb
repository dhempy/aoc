
DIGITS = {
  'one' => '1',
  'two' => '2',
  'three' => '3',
  'four' => '4',
  'five' => '5',
  'six' => '6',
  'seven' => '7',
  'eight' => '8',
  'nine' => '9',
}

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

TOKENS = %w[
  one 1
  two 2
  three 3
  four 4
  five 5
  six 6
  seven 7
  eight 8
  nine 9
]

ans = 0

STDIN.each_line {  |line|
  line.gsub!(/\n/,'')
  puts line
  rawline = line.dup
  revline = line.reverse

  first = line.match(/one|two|three|four|five|six|seven|eight|nine|1|2|3|4|5|6|7|8|9/).to_s
  puts "first: #{first}"

  last = revline.match(/9|8|7|6|5|4|3|2|1|enin|thgie|neves|xis|evif|ruof|eerht|owt|eno/).to_s.reverse
  puts "last: #{last}"

  a = VALS[first]
  b = VALS[last]

  puts " a:#{a} b:#{b}"
  x = a*10 + b
  puts " val #{x}\n"
  # if a == b then
  #   puts "DUPE!"
  #   puts " val #{x}"
  #   puts "   >> from #{rawline}"
  #   puts "   >>   to #{line}"
  # end

  # puts "Line value: #{x} from #{line} (raw: #{rawline})"
  ans = ans + x
}


puts "Answer: #{ans}"

# 53900 is TO HIGH

