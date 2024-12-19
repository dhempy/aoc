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
  puts "eqn_valid?(#{total}, #{vals})"
  return (total == vals.first) if vals.one?

  return false if total < (vals - [1]).sum  # then it could never be small enough
  return true if eqn_valid?(total, [(vals[0] + vals[1]), vals[2..]].flatten)
  return true if eqn_valid?(total, [(vals[0] * vals[1]), vals[2..]].flatten)
  return true if eqn_valid?(total, [("#{vals[0]}#{vals[1]}".to_i), vals[2..]].flatten)
  return false
end


STDIN.each_line do |raw_line|
  puts
  puts raw_line
  total, vals = parse_line(raw_line)

  if eqn_valid?(total, vals)
    puts "VALID"
    sum += total
  else
    puts "invalid"
  end

  # if safe_line?(cells)
  #   safe_count += 1
  #   puts "++++++++++++++++++++++ SAFE LINE"
  # else
  #   puts "Log line: #{@log}"
  #   puts "--------------------------------------------------- unsafe line"
  # end
end

puts
puts "SUM: #{sum}"


# SUM: 227921760109726
# ruby b.rb < in  44.23s user 16.95s system 93% cpu 1:05.52 total

# With sum optimizer, excluding 1's
# SUM: 227921760109726
# ruby b.rb < in  31.51s user 11.88s system 91% cpu 47.298 total

# With sum optimizer, allowing 1's
# SUM: 227187890784548  <<<<<<<<<< WRONG!!!!
# ruby b.rb < in  31.23s user 11.89s system 94% cpu 45.457 total