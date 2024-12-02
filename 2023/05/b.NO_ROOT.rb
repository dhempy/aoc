
# def initial_map(ranges)
#   pp ranges
#   maps = ranges.each_slice(2).map do |start, len |

#     # puts "  range: #{range}"
#     # start = range[0]
#     # len = range[1]
#     stop = start + len - 1
#     delta = start

#     { start: start, stop: stop, len: len, dest: start, delta: delta, best_location: nil}
#   end

#   {
#     label: 'START-to-seed',
#     from_stuff: 'START',
#     to_stuff: 'seed',
#     best_location: nil,
#     maps: maps

#   }
# end



def parse
  @seeds = STDIN.readline
                .match(/seeds: (.*)/)
                .captures
                .first
                .split
                .map(&:to_i)
  STDIN.readline

  # puts "seeds: "

  # @maps["START-HERE"] = initial_map(@seeds)

  @maps = STDIN.read.split("\n\n").map do |txt|
    # puts "-------------\n#{txt}"
    (label, lines) = txt.match(/(.*) map:\n(.*)/m).captures
    # puts "label: #{label}"
    (from_stuff, to_stuff) = label.split('-to-')
    # puts " lines: #{lines}"
    maps = lines.split("\n").map do |line|
      # puts "  line: #{line}"
      (dest, start, len) = line.match(/(\d+) (\d+) (\d+)/).captures.map(&:to_i)
      # puts "     d:#{dest} s:#{start} l:#{len}"
      delta = dest - start
      stop = start + len
      { start: start, stop: stop, len: len, dest: dest, delta: delta, best_location: nil}
    end

    [
      from_stuff, {
        label: label,
        from_stuff: from_stuff,
        to_stuff: to_stuff,
        best_location: nil,
        maps: maps
      }
    ]
  end.to_h
end

def next_step(step, id)
  # puts "  next_step(#{step}, #{id})"
  step[:maps].find do |maybe|
    # puts "    test #{maybe}"
    true if id.between?(maybe[:start], maybe[:stop])
  end #.tap { |x| puts "    Found next_step: #{x}"}
end


# returns best location of all possible paths.
def navigate(from_stuff, to_stuff, id = 0)
  step = @maps[from_stuff]

  puts "\n navigate(#{from_stuff}, #{to_stuff}, #{id})..."
  raise "LOCATION NOT FOUND" unless from_stuff

  puts "  step: #{step}"

  if from_stuff == to_stuff
    # step[:best_location] = id
    puts "  FOUND LOCATION!"
    puts "  step: #{step}"
    return id
  end

  if step[:best_location]
    puts "     already solved: #{step[:best_location]}"
    return step[:best_location] if step[:best_location]
  end

  puts "...WORKING HARD..."
  sleep 1


  step[:maps].each do |goto|
    puts "    goto: #{goto}"
    delta = (goto && goto[:delta]) || 0
    goto[:best_location] = navigate(step[:to_stuff], to_stuff, id + delta)
  end

  best_path = step[:maps].min { |a, b| a[:best_location] <=> b[:best_location] }
  step[:best_location] = best_path[:best_location]
end

# def process
#   @best = navigate('START-HERE', 'location')
#   puts "****** WINNER: #{@best}"
# end

def process
#   maps = ranges

  @seeds.each_slice(2).map do |start, len|
    range = (start..(start+len-1))
    puts "\n============ TEST FROM #{range}"
    range.each do |seed|
      puts "  ========== test #{seed}"

      @seed_locations[seed] = navigate('seed', 'location', seed)
    end
  end
end

def best_location
  @seed_locations.sort_by{|key,val| val}.first
end

@seeds = {}
@maps = {}
@seed_locations = {}

parse
puts "seeds:"
pp @seeds

puts "maps:"
pp @maps

# puts "seed_ranges:"
# pp @seed_ranges.inspect


process

puts "maps: (FINAL)"
pp @maps

# exit


# puts "seed_locations:"
# pp @seed_locations
puts "best:"
pp @best

ans = best_location


puts "Answer: #{ans}"