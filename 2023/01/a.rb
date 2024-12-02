

ans = 0

STDIN.each_line {  |line|
  puts line

  a = nil
  b = nil

  digits = line.each_char { |c|
              # puts c
              next unless c.match(/\d/)
              a ||= c.to_i
              b = c.to_i

              puts "GOT IT: #{a},#{b}"
           }

  x = a*10 + b
  puts "Line value: #{x}"
  ans = ans + x
}


puts "Answer: #{ans}"