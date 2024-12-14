#!/usr/bin/env ruby

safe_count = 0

@row = []

def same_sign?(a, b)
  a * b > 0
end

@log = []

def safe_pair?(a, b, dir)
  diff = b - a
  puts "  #{diff} <- #{a} #{b}"

  return false if diff.zero?
  # puts 'a'
  return false if diff > +3
  # puts 'b'
  return false if diff < -3
  # puts 'c'
  return false unless same_sign?(diff, dir)
  # puts "  #{diff} <- #{a} #{b} SAFE PAIR"

  @log << diff

  return true
end

def safe_line?(cells, dir = false, trimmable = true)
  puts cells.inspect

  dir ||= cells[1] - cells[0]
  row_len = cells.length

  warned = false

  (0..(row_len - 2)).each do |i|
    if !safe_pair?(cells[i], cells[i + 1], dir)
      puts "OOPS! "
      return false unless trimmable
      sub_line = [cells[i]] + cells[i+2..]
      puts "Try it without #{cells[i + 1]}... "
      return safe_line?(sub_line, dir, false)
    end
  end

  return true
end

STDIN.each_line do |line|
  puts
  puts line
  cells = line.split(' ').map(&:to_i)
  @row = []
  @log = []

  if safe_line?(cells)
    safe_count += 1
    puts "++++++++++++++++++++++ SAFE LINE"
  else
    puts "Log line: #{@log}"
    puts "--------------------------------------------------- unsafe line"
  end
end

puts
puts "safe lines: #{safe_count}"

# 519 is too low.
# 535 is too low.