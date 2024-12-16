#!/usr/bin/env ruby

sum = 0


DIRS = [
  [-1, 0],
  [0, 1],
  [1, 0],
  [0, -1]
]

def parse_grid(input)
  puts "======================================"

  grid = input.readlines.map(&:chomp).map { |line| line.split('') }

  puts "grid:"
  # pp grid
  dump_grid(grid)
  grid
end

CLS = "\e[H\e[2J"
CLS = "________________________________________________________________\n"

def dump_grid(grid)
  puts CLS + grid.map(&:join).join("\n") + "\n"
end

def find_start(grid)
  grid.each_with_index do |row, r|
    c = row.find_index('^')
    return[r,c] if c
  end
end

def zero_grid(grid)
  grid.each do |row|
    row.each_with_index do |cell, c|
      # puts "cell: #{cell} at index #{c}"
      row[c] = [' '] unless cell == '#'
    end
  end
  dump_grid(grid)
end

def out_of_bounds(r, c, max)
  (
    r.negative? || r >= max ||
    c.negative? || c >= max
  ).tap { |oob| puts 'OUT OF BOUNDS' if oob }
end

def turn(dir)
  puts " TURN!!!"
  (dir + 1) % 4
end

def blocked(grid, r, c)
  (
    grid[r][c] == '#'
  ).tap { |blocked| puts 'BLOCKED' if blocked }

end

def patrol(grid, max, r, c, dir, seen)
  # sleep(0.01)
  # puts "   patrol(grid, max, #{r}, #{c}, #{dir}(#{DIRS[dir]}), #{seen})..."

  dump_grid(grid)

  return seen if out_of_bounds(r, c, max)
  return nil if blocked(grid, r, c)

  if grid[r][c].include?(dir)
    puts "        ^^^ FOUND A LOOP ^^^ "
    return
  end

  grid[r][c].push(dir)
  success = patrol(grid, max, r+DIRS[dir].first, c+DIRS[dir].last, dir, 1+seen)
  grid[r][c].pop()

  if grid[r][c].empty?
    grid[r][c] = '#'
    ... and do some recursive stuff...
    ... and do some recursive stuff...
    ... and do some recursive stuff...
    ... and do some recursive stuff...
    ... and do some recursive stuff...
    ... and do some recursive stuff...
    ... and do some recursive stuff...
    ... and do some recursive stuff...
    ... and do some recursive stuff...
    ... and do some recursive stuff...
  end

  return success if success

  dir = turn(dir)
  success = patrol(grid, max, r+DIRS[dir].first, c+DIRS[dir].last, dir, 1+seen)

  return success if success

  return 10000
end

def count_grid(grid)
  grid.map { |row|
    row.select { |cell| cell.to_i > 0 }.tap { |counts| puts "counts: #{counts} " }
  }.flatten.count
end

grid = parse_grid(STDIN)
r,c = find_start(grid)
zero_grid(grid)
max = grid.size # assume square

dir = 0
puts "Guard starting at #{r},#{c} moving #{DIRS[dir]} and out_of_bounds: #{out_of_bounds(r, c, max)}"

patrol(grid, max, r, c, dir, 0)

# sum = count_grid(grid)

puts
puts "SUM: #{sum}"

# Too low:
# Too High:
# Correct: