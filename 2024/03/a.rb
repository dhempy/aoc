#!/usr/bin/env ruby



def split(line)
  # puts "split(#{line})..."
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
STDIN.each_line do |line|
  puts "======================================"
  puts line

  pairs = split(line)
  puts "pairs: #{pairs}"

  sum += pairs.map { |p|
          p.inject(:*).tap{ |prod| puts "prod(#{p}) => #{prod}" }
        }.sum
end

puts
puts "SUM: #{sum}"

# 30129655 too low
# 175615763
