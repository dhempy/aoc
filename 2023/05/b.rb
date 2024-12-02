
def initial_map(ranges)
  # puts ranges
  lane = {
            label: 'START-to-seed',
            from_stuff: 'START',
            to_stuff: 'seed',
            terminal_id: {},
            maps: []
          }

  ranges.each_slice(2) do |start, len |
    stop = start + len - 1
    dest = start # No shift.
    add_map(lane, start, stop, dest)
  end

  set_min_max_mapped(lane)

  @lanes["START-HERE"] = lane
end

def parse_seeds
  # seeds: 79 14 55 13
  seeds = STDIN.readline
                .match(/seeds: (.*)/)
                .captures
                .first
                .split
                .map(&:to_i)
  initial_map(seeds)

  STDIN.readline
end

def parse_lanes
  STDIN.read.split("\n\n").each do |txt|
    # puts "-------------\n#{txt}"
    (label, lines) = txt.match(/(.*) map:\n(.*)/m).captures
    # puts "label: #{label}"
    (from_stuff, to_stuff) = label.split('-to-')
    # puts " lines: #{lines}"

    lane = {
            label: label,
            from_stuff: from_stuff,
            to_stuff: to_stuff,
            terminal_id: {}, # the ID of the thing (e.g. location) in the final state.
            maps: [],
          }

    lines.split("\n").map do |line|
      # puts "  line: #{line}"
      (dest, start, len) = line.match(/(\d+) (\d+) (\d+)/).captures.map(&:to_i)
      # puts "     d:#{dest} s:#{start} l:#{len}"
      # delta = dest - start
      stop = start + len - 1
      # {
      #   start: start, stop: stop, len: len, dest: dest, delta: delta,
      #   terminal_id: {},
      #   total_delta: nil,
      # }

      add_map(lane, start, stop, dest)
    end

    seed_missing_maps(lane)
    @lanes[from_stuff] = lane
  end
end

def parse
  parse_seeds
  parse_lanes
end

def sort_maps(lane)
  lane[:maps].sort_by! { |m| m[:start] }
end

def seed_missing_maps(lane)
  set_min_max_mapped(lane)
  range = (lane[:min_mapped]..lane[:max_mapped])
  add_missing_maps(lane, range)
end

# create a pass-through, zero-delta map:
# caller must sort maps sometime later.
def add_map(lane, start, stop, dest=start)
    # puts "add_map(#{lane[:label]}}, #{start}, #{stop}, #{dest})"

    len = stop - start + 1
    delta = dest - start

    new_map = {
                start: start, stop: stop, len: len, dest: dest, delta: delta,
                terminal_id: {},
                total_delta: nil,
              }

    # puts "     Addding map to lane #{lane[:label]}: #{new_map}"
    lane[:maps] << new_map
end

def set_min_max_mapped(lane)
  sort_maps(lane)
  lane[:min_mapped] = lane[:maps].first[:start]
  lane[:max_mapped] = lane[:maps].last[:stop]
end

def add_missing_maps(lane, range)
  # puts "add_missing_maps(lane, #{range})"
  # pp lane
  # return if range.nil? || range.empty?

  last_stop = range.min
  # puts "  Find first gap starting at #{last_stop}:"

  lane[:maps].each_with_object({}) do |m|
    # puts "  Is there a gap prior to #{m[:start]}?"
    # puts "    Gap between #{lane[:label]} #{last_stop} and #{m[:start]}" unless last_stop == m[:start]
    last_stop = m[:stop]+1
  end

  # puts "  is range is within mapped values?"
  # return if lane[:min_mapped] && range.min >= lane[:min_mapped] && range.max <= lane[:max_mapped]
  # puts "  range is within mapped values?"

  return if lane[:from_stuff] == 'START' # Never expand starting maps!

  # puts "add_missing_maps found work to do..."
  set_min_max_mapped(lane)

  if range.min < lane[:min_mapped]
    add_map(lane, range.min, lane[:min_mapped]-1)
  end

  if range.max > lane[:max_mapped]
    add_map(lane, lane[:max_mapped] + 1, range.max)
  end

  set_min_max_mapped(lane)

  prev = nil

  # puts "        lane: (before adding missing)"
  # pp lane

  # puts "  gap audit (with corrections)"
  lane[:maps].dup.each do |one|
    # puts "    checking for gap loop "
    if prev
      # puts "     test for gap between #{prev[:stop]+1} .. #{one[:start]} "
      if prev[:stop]+1 < one[:start]
        puts "  GENERATING missing map for gap: #{lane[:label]} #{prev[:stop]}..#{one[:start]}"
        add_map(lane, prev[:stop] + 1, one[:start] - 1)
      end
    end
    prev = one
  end

  set_min_max_mapped(lane)

  # puts "        lane: (after adding missing)"
  # pp lane

end

def mind_the_gap
  puts "  gap audit (mind the gap)"

  @lanes.each do |stuff, lane|
    next if stuff == "START-HERE"
    prev = nil

    lane[:maps].each do |one|
      if prev
        # puts "     test for gap between #{prev[:stop]+1} .. #{one[:start]} "
        if prev[:stop]+1 != one[:start]
          raise "     GAP DETECTED between #{stuff} #{prev[:stop]+1} .. #{one[:start]} "
        end
      end
      prev = one
    end
  end
end

# returns the lowest terminal_id from this point within range.
def navigate(from_stuff, final_stuff, range = nil)
  puts "navigate(#{from_stuff}, #{final_stuff}, #{range})"
  raise "LOCATION NOT FOUND" unless from_stuff

  if from_stuff == final_stuff
    # lane[:terminal_id] = range
    puts "  FOUND LOCATION! best is #{range.min}"
    return range.min
  end

  lane = @lanes[from_stuff]
  # puts "  lane: ++++++++++++++++++++++++"
  # pp lane

  puts "   ALREADY SOLVED: #{lane[:terminal_id][range]}" if lane[:terminal_id][range]
  return lane[:terminal_id][range] if lane[:terminal_id][range]

  # puts " >>> WORKING HARD <<< (#{from_stuff}, #{final_stuff}, #{range})"
  # sleep 1

  range ||= (lane[:min_mapped]..lane[:max_mapped])
  # puts "     range: #{range.inspect}"
  add_missing_maps(lane, range) if range

  candidates = lane[:maps].map do |step|
    # puts "   lane #{lane[:label]} step before: #{step}"

    # abort if no range overlaps:
    if step[:start] > range.max || step[:stop]  < range.min
      # puts "     skipping, no range overlap"
      next
    end

    # find best path within this map, over the requested range
    range_start = [step[:start], range.min].max + step[:delta]
    range_stop  = [step[:stop] , range.max].min + step[:delta]
    sub_range = (range_start..range_stop)
    # puts "   subrange: #{sub_range.inspect}"

    terminal_id = navigate(lane[:to_stuff], final_stuff, sub_range)
    lane[:terminal_id][range] ||= terminal_id

    # puts "   lane #{lane[:label]} step after: #{step}"
    terminal_id
  end.compact

  # puts " +++++++ Sort candidates #{candidates} to find best final..."
  # pp lane
  # pp lane[:maps]
  # puts "   #{lane[:maps].pluck(:terminal_id)}"
  best_terminal_id = candidates.min
  lane[:terminal_id][range] = best_terminal_id
  # puts "terminal_id should be set: ~~~~~~~~~~~~~~~~~~"
  # pp lane
  best_terminal_id

  # maybe I should return best_step instead of best_terminal_id? or best_map?
  # maybe need to rename @lanes to @lanes?
end


def process
  @best = navigate('START-HERE', 'location')
  puts "****** WINNER: #{@best}"
end

@lanes = {}

puts "\nparse: ==========================================="
parse


puts "\nprocess: ==========================================="
process
mind_the_gap


puts "\nlanes: (FINAL) ==========================================="
pp @lanes


puts "\nbest: ==========================================="
pp @best

ans = @best



puts "\nAnswer: #{ans} ==========================================="



# Example path: (not the best, probably)
# Seed 79,
# soil 81,
# fertilizer 81,
# water 81,
# light 74,
# temperature 78,
# humidity 78,
# location 82.

# 690038049 = That's not the right answer; your answer is too high.
# 2254686 = That's the right answer!