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

count = 0


def xmas?(grid, r, c)
  # puts "xmas?(#{r}, #{c})..."
  window = [
    grid[r][c..c+2],
    grid[r+1][c..c+2],
    grid[r+2][c..c+2]
  ]
  pp window

  # corners = [
  #     window[0][0],
  #     window[0][2],
  #     window[2][0],
  #     window[2][2]
  # ].join
  # puts "corners: #{corners}"

  return false unless window[1][1] == 'A'
  return false unless (window[0][2] == 'M' && window[2][0] == 'S') || (window[0][2] == 'S' && window[2][0] == 'M')
  return false unless (window[0][0] == 'M' && window[2][2] == 'S') || (window[0][0] == 'S' && window[2][2] == 'M')
  return true

end

(0..grid.length-3).each do |r|
  (0..grid[r].length-3).each do |c|
    if (xmas?(grid, r, c))
      count += 1
      puts "#{count}: #{grid[r][c]}  ============= X-MAS!!! ============= "
    else
      puts "#{count}: #{grid[r][c]}"
    end
  end
end



puts
puts "SUM: #{count}"

# 2530 correct