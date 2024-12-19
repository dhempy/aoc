#!/usr/bin/env ruby

sum = 0

# def parse_grid(input)
#   puts "======================================"

#   grid = input.readlines.map(&:chomp).map { |line| line.split('') }
#   puts "grid:"
#   pp grid
# end

# grid = parse_grid(STDIN)




def parse_line(line)
  # puts "parse_line(#{line})..."
  return if line.chomp.nil?

  total, vals = line.split(':')
  total = total.to_i
  vals = vals.split(' ').map(&:to_i)
  # puts "total: #{total}"
  # puts "vals: #{vals}"

  return total, vals
end


def eqn_valid?(total, vals)
  # puts "eqn_valid?(#{total}, #{vals})"
  return (total == vals.first) if vals.one?

  # return false if total < (vals - [1]).sum  # then it could never be small enough
  return true if eqn_valid?(total, [(vals[0] + vals[1]), vals[2..]].flatten)
  return true if eqn_valid?(total, [(vals[0] * vals[1]), vals[2..]].flatten)
  return false
end


# CLS = "\e[H\e[2J"
# CLS = "\n"
CLS = "TOWERS:\n"

def dump(towers)
  puts CLS
  towers.each do |c, a|
    puts  "#{c}: #{a.inspect}"
  end.to_a

end


def out_of_bounds(coord, max)
  x, y = coord
  puts "    x:#{x}"
  puts "    y:#{y}"
  puts "    max:#{max}"
  (
    x.negative? || x >= max ||
    y.negative? || y >= max
  ) .tap { |oob| puts 'OUT OF BOUNDS' if oob }
end


towers = {}
echos = {}
max = nil

STDIN.each_with_index do |line, x|
  line.chomp!
  max ||= line.size
  puts "#{x}: #{line}  (size: #{max})"

  line.chars.each_with_index do |c, y|
    next if c == '.'
    # puts "#{x}, #{y}: #{c}"

    towers[c] ||= []
    towers[c] << [x,y]
  end

  # total, vals = parse_line(raw_line)

  # if eqn_valid?(total, vals)
  #   puts "VALID"
  #   sum += total
  # else
  #   puts "invalid"
  # end

  # if safe_line?(cells)
  #   safe_count += 1
  #   puts "++++++++++++++++++++++ SAFE LINE"
  # else
  #   puts "Log line: #{@log}"
  #   puts "--------------------------------------------------- unsafe line"
  # end
end
dump(towers)


towers.each do |c, a|
  puts "-- #{c} --"
  a.combination(2).each do |j, k|
    puts "  j:#{j} k:#{k}"
    dx = j[0] - k[0]
    dy = j[1] - k[1]

    puts "  delta: #{dx},#{dy}"

    e1 = [j[0]+dx, j[1]+dy]
    e2 = [k[0]-dx, k[1]-dy]

    puts "  echo1: #{e1}"
    puts "  echo2: #{e2}"

    echos[e1] = true unless out_of_bounds(e1, max)
    echos[e2] = true unless out_of_bounds(e2, max)

    # puts "  #{pair}"
    # puts "  join: #{pair.join}"
    # puts "  first: #{pair.first}"
  end
end

puts "echos:"
pp echos

sum = echos.count

puts
puts "SUM: #{sum}"

# Too low:
# Too High:
# Correct: 4555081946288