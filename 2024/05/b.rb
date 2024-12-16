# BROKEN
# #!/usr/bin/env ruby

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


def valid_line(cells, corrected = false)
  puts " valid_line(#{cells})..."

  this_index = 0
  cells.reduce([]) do |seen, value|
    # puts "   seen: #{seen.inspect} (#{seen.class}) "
    # puts "   @precedes[#{value}].intersection(#{seen})&.any? "
    # puts "   #{@precedes[value]}.intersection(#{seen})&.any? "
    # puts "     => #{@precedes[value]&.intersection(seen)&.any?}"
    collider = @precedes[value]&.intersection(seen)&.first
    if collider
      that_index = cells.find_index(collider)
      # puts "    #{value}: fail because @precedes[#{value}] is #{@precedes[value]} and collides with seen: #{seen.inspect} with: #{collider} at cells[#{that_index}]"
      # puts "    #{value}: btw,          @follows[#{value}] is #{@follows[value]} "
      # puts "   FAIL ----------------------"

      new_cells = cells.dup
      new_cells[this_index], new_cells[that_index] = new_cells[that_index], new_cells[this_index]


      return valid_line(new_cells, true)
      # ignore that there might not be a solution...advent prob won't do that.
      # return false
    end

    this_index += 1

    # puts "   PRE  seen: #{seen.inspect} (#{seen.class}) "
    seen << value
  end

  puts "   ALL GOOD +++++++++++++++++++++ #{cells}"

  if (corrected)
    mid = cells[(cells.length-1)/2]
    puts "  >>>>>>>>>>>>>>>> CORRECTED RESULT: middle cell[#{(cells.length-1)/2}] of #{cells}: #{mid}"
    @sum += mid.to_i
  end
  return cells
end

def parse_line(line)
  puts "parse_line(#{line})..."
  return if line.empty?

  cells = line.split(',')


  valid_line(cells)
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