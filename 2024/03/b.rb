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

def split_do(line)
  # puts "split_do(#{line})..."
  lines = line.split(/do\(\)/)

  pairs = []
  lines.each do |line|
    puts "\nline: #{line}"
    (yes, no) = line.split(/don't()/)
    puts "     yes do this: #{yes}"
    puts "no don't do this: #{no}"
    pairs += split(yes)
    # puts "   adding in #{more}"
    # pairs << more
  end

  pairs
end

sum = 0
line = STDIN.read

puts "======================================"
puts line

pairs = split_do(line)
puts "pairs: #{pairs}"

sum += pairs.map { |p|
        p.inject(:*).tap{ |prod| puts "prod(#{p}) => #{prod}" }
      }.sum

puts
puts "SUM: #{sum}"

# 74361272