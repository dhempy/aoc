#!/usr/bin/env ruby

safe_count = 0
unsafe_count = 0

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
  puts "safe_line?(#{cells.inspect})..."

  row_len = cells.length
  return true if row_len <= 1

  dir = cells[1] - cells[0]

  (0..(row_len - 2)).each do |i|
    if !safe_pair?(cells[i], cells[i + 1], dir)
      puts "OOPS! "
      return false unless trimmable
      if i.zero?
        # First pair was bad
        sub_line = cells[1..]
        puts "Try it without #{cells[0]}... (first element) "
        return true if safe_line?(sub_line, dir, false)
      end

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
  next if cells.none?
  @row = []
  @log = []

  if safe_line?(cells)
    safe_count += 1
    puts "++++++++++++++++++++++ SAFE LINE"
  else
    unsafe_count += 1

    puts "Log line: #{@log}"
    puts "--------------------------------------------------- unsafe line"
  end
end

puts
puts "  safe lines: #{safe_count}"
puts "unsafe lines: #{unsafe_count}"

# 519 is too low.
# 535 is too low.
# 536