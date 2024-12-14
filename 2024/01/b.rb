#!/usr/bin/env ruby

a = []
b = {}

STDIN.each_line do |line|
  puts " line: #{line}"
  line.split(/\s+/).each_slice(2) do |x, y|
    puts "got #{x} and #{y}"
    a << x.to_i
    b[y.to_i] = 1 + (b[y.to_i] || 0)
  end
end

puts "left  array: #{a.join(', ')}"
puts "right array: #{b}"

total = 0

a.each do |x|

  dist = x * (b[x] || 0)
  puts "Distance: #{x} * #{b[x]} => #{dist}"

  total += dist
end

puts " TOTAL: #{total}"