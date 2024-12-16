#!/usr/bin/env ruby

@sum = 0

@follows = {}
@precedes  = {}

def parse_grid(input)
  puts "parse_grid..."

  input.each_line do |raw_line|
    raw_line.chomp!
    puts raw_line
    break if raw_line.empty?
    (a, b) = raw_line.split('|')

    @follows[b] ||= []
    @follows[b] << a

    @precedes[a] ||= []
    @precedes[a] << b
  end

  puts "@precedes:"
  pp @precedes

  puts "@follows:"
  pp @follows

  puts "==========================\n\n"
end


def valid_line?(cells)

  cells.reduce([]) do |seen, value|
    # puts "   @precedes[#{value}]}.intersection(#{seen})&.any? "
    # puts "   #{@precedes[value]}.intersection(#{seen})&.any? "
    # puts "     => #{@precedes[value]&.intersection(seen)&.any?}"
    if @precedes[value]&.intersection(seen)&.any?
      puts "    #{value}: fail because #{@precedes[value]} collides with: #{seen.inspect}"
      # puts "   FAIL ----------------------"
      return false
    end
    seen << value
  end

  puts "   ALL GOOD +++++++++++++++++++++ cells.length: #{cells.length}"
  mid = cells[(cells.length-1)/2]
  puts "  middle cell[#{(cells.length-1)/2}]: #{mid}"
  @sum += mid.to_i
  return true
end

def parse_line(line)
  puts "parse_line(#{line})..."
  return if line.empty?

  cells = line.split(',')
  # cells = line.scan(/mul\(\d{1,3},\d{1,3}\)/)

  # puts "cells: #{cells}"

  valid_line?(cells)
  # cells.map do |f|
  #   puts "f: #{f}"
  #   (a, b) = f.scan(/\d{1,3}/)
  #   puts "pair: #{a} -- #{b}"
  #   [a.to_i, b.to_i]
  # end

  # .map(&:to_i)
end

parse_grid(STDIN)


STDIN.each_line do |raw_line|
  raw_line.chomp!
  parse_line(raw_line)

  # if safe_line?(cells)
  #   safe_count += 1
  #   puts "++++++++++++++++++++++ SAFE LINE"
  # else
  #   puts "Log line: #{@log}"
  #   puts "--------------------------------------------------- unsafe line"
  # end
end

puts
puts "SUM: #{@sum}"

# Too low:
# Too High:
# Correct: 7307