#!/usr/bin/env ruby

def split(line)
  puts "split(#{line})..."
  return if line.nil?
  hits = line.scan(/mul\(\d{1,3},\d{1,3}\)/)

  # puts "HITS: #{hits}"

  hits.map do |f|
    puts "f: #{f}"
    (a, b) = f.scan(/\d{1,3}/)
    puts "pair: #{a} -- #{b}"
    [a.to_i, b.to_i]
  end
end


sum = 0
raw_lines = STDIN.readlines.map(&:chomp)

puts "======================================"
puts raw_lines
puts "class: #{raw_lines.class}"

grid = raw_lines.map { |line| line.split('') }
puts "grid:"
pp grid

grid_down = grid.transpose
puts "grid_down:"
pp grid_down

padding = [*0..(grid.length - 1)].map { |i| [nil] * i }

padded_down = padding.reverse.zip(grid).zip(padding).map(&:flatten)
grid_diag_down = padded_down.transpose.map(&:compact)
puts "grid_diag_down:"
pp grid_diag_down

padded_up = padding.zip(grid).zip(padding.reverse).map(&:flatten)
grid_diag_up = padded_up.transpose.map(&:compact)
puts "grid_diag_up:"
pp grid_diag_up

omni = grid + grid_down + grid_diag_down + grid_diag_up
puts "omni:"
# pp omni

omni_str = omni.map(&:join)
puts "omni_str:"
# pp omni_str

str = omni_str.join(' ')
# puts "str: #{str}"

str_and_back = str + ' '+ str.reverse
# puts "str_and_back: #{str_and_back}"

hits = str_and_back.scan(/XMAS/)
# puts "hits: #{hits}"

sum = hits.count
puts
puts "SUM: #{sum}"

# 2530 correct