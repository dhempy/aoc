

def compute_gears
  @gears.map do |key,val|
    puts "Gear #{key}: #{val}"
    next if val.count<2
    val.inject(&:*)
       .tap {|x| puts "Connected! #{x}" }
  end.compact.sum
end

def mark_gears(r, c1, c2, part_num)

  @board[r][c1..c2].each_with_index do |cell, c|
    next unless cell == '*'
    id = "#{r},#{c1+c}"
    puts "            >>> Found a gear at #{id} near #{part_num}"
    if @gears[id].nil?
      @gears[id] = [part_num]
    else
      @gears[id] << part_num
    end
  end
end


def check_part(r, c1, c2)
  puts "        check_part(#{c1}, #{c2})"
  part_num = @board[r][c1..c2].join.to_i

  borders = (@board[r-1][c1-1 .. c2+1] +
            [@board[r][c1-1], @board[r][c2+1]] +
            @board[r+1][c1-1 .. c2+1]
  ).join

  puts "          borders: #{borders}"

  none_found = borders.match?(/\A[\d\.]*\z/)

  mark_gears(r-1, c1-1, c2+1, part_num)
  mark_gears(r  , c1-1, c1-1, part_num)
  mark_gears(r  , c2+1, c2+1, part_num)
  mark_gears(r+1, c1-1, c2+1, part_num)

  puts " none Found? #{none_found}"
  if none_found
    puts "          FOUND A MISSING PART: #{part_num}"
    @missing_parts << part_num
  else
    @found_parts << part_num
  end
end


ans = 0

@board = []
@missing_parts = []
@found_parts = []
@gears = {}

STDIN.each_line {  |line|
  @board << line.chars
}

puts "Board size: #{@board.length}"

# 1. Each number
#    For each gear found, add number to gear.numbers
# 2. Afterward, travers gears.

@board.each_with_index do |row, r|
  puts "  row[#{r}]: #{row.join}"
  state = nil
  num_start = nil
  num_end = nil

  row.each_with_index do |cell, c|
    # puts "    row[#{r},#{c}]: #{cell}"

    terrain = case cell
              when /\d/ then :num
              when '.'  then nil
              else :part
              end

    case state
    when nil
      if terrain ==  :num
        state = :number
        num_start = c
      end
    when :number
      next if terrain == :num

      num_end = c-1
      puts "      Part number: #{r},#{num_start}...#{num_end}: #{row[num_start..num_end].join}"
      check_part(r, num_start, num_end)
      state = nil
    end
  end
end


puts "missing parts: #{@missing_parts}"
puts "found   parts: #{@found_parts}"
puts "gears: #{@gears}"

ans = compute_gears

puts "Answer: #{ans}"
