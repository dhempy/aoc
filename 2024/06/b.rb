#!/usr/bin/env ruby

sum = 0
@loop_count = 0


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
CLS = "\033[0;0H"

# CLS = "________________________________________________________________\n"
CLS = "\n"

# def deep_dup(obj)
#   obj.map { |it| it.deep_dup }
# end

def dump_grid(grid, r = nil, c = nil)
  return if Random.rand < 0.001

  puts CLS + grid.map { |row|
    row.map { |cell|
      if cell.respond_to?(:join)
        # cell.any? ? cell.join(',')  : ' '
        cell.any? ? cell.sum()  : '.'
      else
        cell || ' '
      end
    }.join
  }.join("\n") + "\n"
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
      row[c] = [] unless cell == '#'
    end
  end
  dump_grid(grid)
end

def exited?(r, c, max)
  (
    r.negative? || r >= max ||
    c.negative? || c >= max
  ).tap { |result|
    puts "exited(#{r},#{c}, #{max}) => #{result}}" #if oob
  }
end

def turn(dir)
  # puts " TURN!!!"
  (dir + 1) % 4
end

def opposite(dir)
  DIRS[(dir + 2) % 4]
    .tap { |val| puts "opposite(#{dir}) => #{val}"}
end

def blocked?(grid, r, c)
  (
    grid[r][c] == '#'
  ).tap { |blocked|
    # puts "  BLOCKED" if blocked
  }
end

def looped?(grid, r, c, dir)
  if grid[r][c].include?(dir)
    # puts 'LOOPED'
    return true
  end
end

def debug(depth, r, c, msg)
  return if Random.rand < 0.001
  puts "        [#{r},#{c}]#{' ' * (depth % 20)} step #{depth} #{msg}"
end

def patrol(grid, max, r, c, dir, steps=0, hacks=0)
  # sleep(0.01)
  # puts "   patrol(grid, max, #{r}, #{c}, #{dir}(#{DIRS[dir]}), #{steps})..."
  debug(steps, r, c, "stepping in dir #{dir}")

  dump_grid(grid, r, c) if steps >= 6000

  if exited?(r, c, max)
    debug(steps, r, c, "EXITED THE MAP  <-----------------------------<<")
    return true
  end

  if blocked?(grid, r, c)
    debug(steps, r, c, "backing down from a a barrier.")
    return false
  end

  if looped?(grid, r, c, dir)
    @loop_count += 1
    debug(steps, r, c, "FOUND LOOP #{@loop_count} with direction #{dir} in #{grid[r][c]} <-----------------------------<< ")
    return true
  end

  # step forward one:
  grid[r][c].push(dir)

  # And seek OOB
  puts "success = patrol(grid, max, r+DIRS[#{dir}].first, c+DIRS[#{dir}].last, #{dir}, 1+steps, hacks)"
  success = patrol(grid, max, r+DIRS[dir].first, c+DIRS[dir].last, dir, 1+steps, hacks)
  # That patrol could probably be coerced down into the turn loop.... shrug.


  if !success
    debug(steps, r, c, "backed down blocked by a barrier")
    new_dir = dir
    tries = 3

    while (tries.positive? && !success) do
      tries -= 1
      debug(steps, r, c, "turning...")
      new_dir = turn(new_dir)
      success = patrol(grid, max, r+DIRS[new_dir].first, c+DIRS[new_dir].last, new_dir, 1+steps, hacks)
      debug(steps, r, c, "turned")
    end


    debug(steps, r, c, "After #{tries} tries, success is #{success}.")
  end

  # Now take that step back:
  grid[r][c].pop()

  if success
    debug(steps, r, c, "succeeded")
    dump_grid(grid, r, c) if steps >= 6000

    if !grid[r][c].empty?
      debug(steps, r, c, "Don't build here...we've been here before: #{grid[r][c]}")
      return true
    end

    if hacks.positive?
      debug(steps, r, c, "Sorry, can't add a second barrier.")
      return true
    end

    debug(steps, r, c, "Create barrier ##{hacks} at #{r},#{c}")
    grid[r][c] = '#'

    retreat = opposite(dir)
    prev_r, prev_c = r+retreat.first, c+retreat.last
    puts "prev_r: #{prev_r}"
    puts "prev_c: #{prev_c}"
    debug(steps, r, c, "In dir #{dir}, the cell before #{r},#{c} was #{prev_r},#{prev_c} => #{grid[prev_r][prev_c]} ")
    dump_grid(grid, r, c) if steps >= 6000

    success = patrol(grid, max, prev_r, prev_c, turn(dir), 1+steps, hacks + 1)


    # debug(steps, r, c, "patrol from one step back and turned in the next direction, and stepped forward one. (all to avoid stepping on the prev cell) ")
    # new_dir = turn(dir)
    # success = patrol(grid, max, prev_r+DIRS[new_dir].first, prev_c+DIRS[new_dir].last, new_dir, 1+steps, hacks + 1)

    debug(steps, r, c, "Remove temp barrier at #{r},#{c}")
    grid[r][c] = []  # It was already empty before the new barrier.

    return true
  else
    debug(steps, r, c, "patrol failed. Why? probably backed into a corner or created a 1x1 box around the guard ")

  end

  # debug(steps, r, c, "backing down from a failed path...probably backed into a corner")
  # raise "backing down from a failed path...probably backed into a corner"
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
puts "grid size: #{max} (rows)"
puts "grid size: #{grid.first.size} (first row)"

dir = 0
puts "Guard starting at #{r},#{c} moving #{DIRS[dir]} and exited?: #{exited?(r, c, max)}"

patrol(grid, max, r, c, dir)

# sum = count_grid(grid)

puts
puts "@loop_count: #{@loop_count}"

# Too low:
# Too High:
# Correct: # @loop_count: 1424


