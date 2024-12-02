def parse
  @seeds = STDIN.readline
                .match(/seeds: (.*)/)
                .captures
                .first
                .split
                .map(&:to_i)
  STDIN.readline

  @maps = STDIN.read.split("\n\n").map do |txt|
    puts "-------------\n#{txt}"
    (label, lines) = txt.match(/(.*) map:\n(.*)/m).captures
    puts "label: #{label}"
    (from_stuff, to_stuff) = label.split('-to-')
    # puts " lines: #{lines}"
    maps = lines.split("\n").map do |line|
      puts "  line: #{line}"
      (dest, start, len) = line.match(/(\d+) (\d+) (\d+)/).captures.map(&:to_i)
      # puts "     d:#{dest} s:#{start} l:#{len}"
      delta = dest - start
      stop = start + len
      { start: start, stop: stop, len: len, dest: dest, delta: delta}
    end

    [
      from_stuff, {
        label: label,
        from_stuff: from_stuff,
        to_stuff: to_stuff,
        maps: maps
      }
    ]
  end.to_h
end

def next_step(step, id)
  puts "  next_step(#{step}, #{id})"
  step[:maps].find do |maybe|
    puts "    test #{maybe}"
    true if id.between?(maybe[:start], maybe[:stop])
  end.tap { |x| puts "    Found next_step: #{x}"}
end

def navigate(from_stuff, to_stuff, id)
  puts " navigate(#{from_stuff}, #{to_stuff}, #{id})..."
  return id if from_stuff == to_stuff

  step = @maps[from_stuff]
  puts "  step: #{step}"
  goto = next_step(step, id)
  delta = (goto && goto[:delta]) || 0
  puts "  goto: #{goto}"
  navigate(step[:to_stuff], to_stuff, id + delta)
end

def process
  @seeds.each do |seed|
    @seed_locations[seed] = navigate('seed', 'location', seed)
  end
end

def first_location
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

process

puts "seed_locations:"
pp @seed_locations

ans = first_location



puts "Answer: #{ans}"