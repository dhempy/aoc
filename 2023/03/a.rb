
def check_part(r, c1, c2)
  puts "        check_part(#{c1}, #{c2})"
  part_num = @board[r][c1..c2].join.to_i

  # borders = @board[r][c1-1 .. c2+1] +  @board[r][c1-1 .. c2+1]
  borders = (@board[r-1][c1-1 .. c2+1] +
            [@board[r][c1-1], @board[r][c2+1]] +
            @board[r+1][c1-1 .. c2+1]
  ).join

  puts "          borders: #{borders}"

  none_found = borders.match?(/\A[\d\.]*\z/)
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


STDIN.each_line {  |line|
  @board << line.chars
}

puts "Board size: #{@board.length}"
# puts "Board 1: #{@board[1].length}"
# puts "@Board 2: #{@board[2].length}"
# puts '--------------'
# puts @board[1].join
# puts @board[1][3..8]
# puts '--------------'
# puts @board[2].join
# puts @board[2][3..8]

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
ans = @found_parts.sum
# }
# {
#   puts line
#   (game_num, reveals) = line.match(/Game (\d+): (.*)/).captures

#   puts "Game: #{game_num}"
#   puts "Reveals: #{reveals}"

#   good = reveals.split('; ').all? do |reveal|
#     puts " reveal #{reveal}"

#     reveal.split(', ').all? do |num_color|
#       (num, color) = num_color.split(' ')
#       puts "   #{num} of #{color}"
#       MOST[color] >= num.to_i
#     end.tap {|bool| puts "  reveal good: #{bool}"}
#   end.tap {|bool| puts " all reveals good: #{bool}"}


#   puts "Game good? #{good}"

#   ans += game_num.to_i if good
# }


puts "Answer: #{ans}"