#!/usr/bin/env ruby

sum = 0


def parse_grid(input)
  puts "======================================"

  grid = input.readlines.map(&:chomp).map { |line| line.split('') }
  puts "grid:"
  pp grid
end

def find_start(grid)
  grid.each_with_index do |row, r|
    c = row.find_index('^')
    return[r,c] if c
  end
end


grid = parse_grid(STDIN)
r,c = find_start(grid)
puts "Guard starting at #{r},#{c}"



def parse_line(line)
  puts "parse_line(#{line})..."
  return if line.nil?
  # hits = line.scan(/mul\(\d{1,3},\d{1,3}\)/)

  # # puts "HITS: #{hits}"

  # hits.map do |f|
  #   puts "f: #{f}"
  #   (a, b) = f.scan(/\d{1,3}/)
  #   puts "pair: #{a} -- #{b}"
  #   [a.to_i, b.to_i]
  # end

  # .map(&:to_i)
end

STDIN.each_line do |raw_line|
  puts
  puts raw_line
  cells = parse_line(raw_line)

  # if safe_line?(cells)
  #   safe_count += 1
  #   puts "++++++++++++++++++++++ SAFE LINE"
  # else
  #   puts "Log line: #{@log}"
  #   puts "--------------------------------------------------- unsafe line"
  # end
end

puts
puts "SUM: #{sum}"

# Too low:
# Too High:
# Correct: