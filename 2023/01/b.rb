
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
ans = 0

STDIN.each_line {  |line|
  line.gsub!(/\n/,'')
  rawline = line.dup
  # puts line

  # If the second argument is a Hash, and the matched text is one of its keys,
  # the corresponding value is the replacement string.
  line.gsub!(/one|two|three|four|five|six|seven|eight|nine/,DIGITS)
  # DIGITS.each do |str, val|
  #   line.gsub!(str, val)
  # end
  # puts line

  puts "from #{rawline} \n  to #{line}" if line != rawline
  a = nil
  b = nil

  digits = line.each_char { |c|
              # puts c
              next unless c.match(/\d/)
              a ||= c.to_i
              b = c.to_i

              # puts "GOT IT: #{a},#{b}"
           }

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

