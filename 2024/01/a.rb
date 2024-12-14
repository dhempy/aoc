#!/usr/bin/env ruby

a = []
b = []

STDIN.each_line do |line|
  puts " line: #{line}"
  line.split(/\s+/).each_slice(2) do |x, y|
    puts "got #{x} and #{y}"
    a << x.to_i
    b << y.to_i
  end
end



puts "left  words: #{a.join(', ')}"
puts "right words: #{b.join(', ')}"

a.sort!
b.sort!
puts " Sorting arrays..."

puts "First words: #{a.join(', ')}"
puts "Last words: #{b.join(', ')}"

total = 0

while a.any? do
  dist = (a.pop - b.pop).abs
  puts "Distance: #{dist}"
  total += dist
end

puts " TOTAL: #{total}"