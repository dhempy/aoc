require 'pry'
require "readline"
Readline.input = IO.new(IO.sysopen("/dev/tty", "r+"))

S = [+1, 0]  # South (visually) is a HIGHER numbered row, based on input.
N = [-1, 0]  # North (visually) is a LOWER  numbered row, based on input.
E = [0, +1]
W = [0, -1]

PASSAGE = {
  '|' => { S => S, N => N },
  '-' => { E => E, W => W },
  'F' => { N => E, W => S },
  '7' => { N => W, E => S },
  'J' => { S => W, E => N },
  'L' => { S => E, W => N },
}

WALL  = '┼'
WATER = '~'
LAND  = '#'

NOT_DRY_LAND = [WALL, WATER]

class Node
  attr_accessor :c, :dist

  def initialize(c)
    @c = c
  end

  def next_move(dir)
    # puts "  #{c}.next_move(#{dir}):"
    # pp PASSAGE
    PASSAGE.dig(c, dir)
      # .tap {|x| puts "   returning #{x}"}
  end

  def to_g
    case c
    when 'S'; 'S'
    # when '|'; '│' # connected
    # when '-'; '─' # connected
    # when '|'; '|' # spaced
    # when '-'; '-' # spaced
    when 'F'; '┌'
    when '7'; '┐'
    when 'J'; '┘'
    when 'L'; '└'
    when '*'; '*'
    when '.'; '.'
    else;     c
    end
  end

  def inspect
    # c
    to_g
  end
end

class Board
  attr_accessor :grid, :curr_row, :curr_col, :start_row, :start_col, :dist

  def initialize
    @grid = []
  end

  def parse
    puts "\n PARSE =========================== "

    #    .....
    #    .S-7.
    #    .|.|.
    #    .L-J.
    #    .....

    self.grid = STDIN.map.with_index do |line, row|
                    line.chomp!
                    next if line.empty?
                    # puts "input: [#{line}]"
                    line.chars.map.with_index do |ch, col|
                      # puts "  char: #{ch}"
                      @start_row, @start_col = row, col if ch == 'S'
                      # node = Node.new(ch)
                      Node.new(ch)
                    end
                  end
    get_sizes
  end

  def get_sizes
    @max_rows = @grid.size
    @max_cols = @grid.first.size
  end

  def finished?
    # puts " grid[#{@curr_row}][#{@curr_col}].c == 'S' => #{grid[@curr_row][@curr_col].c == 'S'}  (dist = #{@dist}) "
    puts @dist if @dist % 100 == 0
    # @here.c == 'S'
    [@curr_row, @curr_col] == [@start_row, @start_col]

  end

  def go(dir)
    # puts "    Go(#{dir})"
    # puts "      from #{@curr_row},#{@curr_col} => #{@here}"
    @curr_row += dir[0]
    @curr_col += dir[1]
    @here = grid[@curr_row][@curr_col]
    @dist = @dist + 1
    # puts "        to #{@curr_row},#{@curr_col} => #{@here}"
  end

  # records the full distance of the loop in @dist,
  # and marks loop with WALL characters.
  def survey_pipe(mark_walls = false)
    puts "\n SURVEY LOOP =========================== "

    @curr_row, @curr_col = @start_row, @start_col
    puts "  starting at #{@curr_row},#{@curr_col}"
    @here = grid[@curr_row][@curr_col]
    @dist = 0
    delta = S # This is a valid starting direction for the given input. Adjust as needed.

    loop do
      # print "\033[0;0H";
      # puts inspect
      go(delta)
      delta = @here.next_move(delta)
      @here.c = WALL if mark_walls
      # puts "  next_move returned #{delta}"
      break if finished?
      break if delta.nil?
    end

    inspect
  end

  def solve_a
    puts "\n SOLVE A =========================== "

    inspect
    survey_pipe
    @part_a_solution = @dist / 2
  end

  # returns a new scaled-up board, with twice the resolution in both dimensions
  def explode
    big_board = Board.new

    @grid.each_with_index do |line, r|
      br = r * 2
      r1 = big_board.grid[br  ] = []
      r2 = big_board.grid[br+1] = []

      line.each_with_index do |node, c|
        ch = node.c
        c1 = c * 2
        c2 = c1 + 1
        # puts "#{r},#{c}: (#{br},#{c1} => ch.c: #{ch.c}"
        case ch
        when '-' # '─'
          r1[c1] = Node.new(ch ); r1[c2] = Node.new('-');
          r2[c1] = Node.new(' '); r2[c2] = Node.new(' ');
        when '|' # '│'
          r1[c1] = Node.new(ch ); r1[c2] = Node.new(' ');
          r2[c1] = Node.new('|'); r2[c2] = Node.new(' ');
        when 'F' # '┌'
          r1[c1] = Node.new(ch ); r1[c2] = Node.new('-');
          r2[c1] = Node.new('|'); r2[c2] = Node.new(' ');
        when '7'
          r1[c1] = Node.new(ch ); r1[c2] = Node.new(' ');
          r2[c1] = Node.new('|'); r2[c2] = Node.new(' ');
        when 'J'
          r1[c1] = Node.new(ch ); r1[c2] = Node.new(' ');
          r2[c1] = Node.new(' '); r2[c2] = Node.new(' ');
        when 'L' # '└'
          r1[c1] = Node.new(ch ); r1[c2] = Node.new('-');
          r2[c1] = Node.new(' '); r2[c2] = Node.new(' ');
        when 'J'
          r1[c1] = Node.new(ch ); r1[c2] = Node.new(' ');
          r2[c1] = Node.new(' '); r2[c2] = Node.new(' ');
        when '.'
          r1[c1] = Node.new(ch ); r1[c2] = Node.new('.');
          r2[c1] = Node.new('.'); r2[c2] = Node.new('.');
        when 'S'
          r1[c1] = Node.new(ch ); r1[c2] = Node.new('-');
          r2[c1] = Node.new('|'); r2[c2] = Node.new(' ');
          big_board.start_row, big_board.start_col = br, c1
        else
          puts "Huh? ch is #{ch}"
          r1[c1] = Node.new(ch ); r1[c2] = Node.new(' ');
          r2[c1] = Node.new(' '); r2[c2] = Node.new(' ');
        end
      end

      # puts "r1: #{r1.inspect}"
      # puts "r2: #{r2.inspect}"
    end

    big_board.get_sizes
    big_board
  end

  # halves the board in both dimensions, scaling down the content
  # Returns the number of LAND cells.
  def cell_count(color)
    puts "\n land_count ==================== "

    count = 0
    # small_board = Board.new

    @grid.each_slice(2) do |row, _row2|
      # puts "  Keep row: #{row}"
      row.each_slice(2) do |cell, _cell2|
        # puts "  Keep cell: #{cell.c}"
        count += 1 if cell.c == color
      end
    end

    count
  end

  # returns number of flooded exterior cells
  def flood(color, r=0, c=0, so_far=0)
    puts "flood(#{color}, #{r},#{c}, #{so_far})"
    return 0 if r<0 || c < 0 || r >= @max_rows || c >= @max_cols
    here = @grid[r][c]

    return 0 if here.c == WALL || here.c == color

    # optimize : we *could* stop as soon as we find the starting point, I think.

    here.c = color
    # sleep 0.5 / @max_rows
    # print "\033[0;0H"
    # puts inspect

    return so_far +
      flood(color, r+1, c) +
      flood(color, r-1, c) +
      flood(color, r, c+1) +
      flood(color, r, c-1) +
      1
  end

  def find_dry_neighbor(r, c)
    return[r-1, c] unless NOT_DRY_LAND.include? @grid[r-1][c].c
    return[r+1, c] unless NOT_DRY_LAND.include? @grid[r+1][c].c
    return[r, c-1] unless NOT_DRY_LAND.include? @grid[r][c-1].c
    return[r, c+1] unless NOT_DRY_LAND.include? @grid[r][c+1].c
    return[r-1, c+1] unless NOT_DRY_LAND.include? @grid[r-1][c+1].c
    return[r+1, c+1] unless NOT_DRY_LAND.include? @grid[r+1][c+1].c
    return[r-1, c-1] unless NOT_DRY_LAND.include? @grid[r-1][c-1].c
    return[r+1, c-1] unless NOT_DRY_LAND.include? @grid[r+1][c-1].c
  end

  def solve_b
    puts "\n SOLVE B =========================== "
    puts inspect
    survey_pipe() # just for debugs
    puts "surveyed:"
    puts inspect
    survey_pipe(true)

    puts "\e[H\e[2J"

    @waters = flood(WATER, 0, 0)
    puts " WALLED GARDEN:"
    puts inspect

    r, c = find_dry_neighbor(@start_row, @start_col)
    puts "DRY neighbor to #{start_row},#{start_col} is #{r},#{c}"
    @drys = flood(LAND, r, c)
    puts " dry land found: #{@drys}"
    puts " METAL ISLAND:"
    puts inspect


    # small_board = implode
    # puts " RESIZED ISLAND:"
    # puts small_board.inspect

    @part_b_solution = cell_count(LAND)
  end

  def inspect
    "Cursor: (#{@curr_row},#{@curr_col})\n" +
      grid.map do |row|
        row.map do |cell|
          cell.to_g
        end.join
      end.join("\n")
  end
end


board_a = Board.new

board_a.parse
pp board_a
puts "Board_a size: #{board_a.grid.length}"


# ans_a = board_a.solve_a
# pp board_a
# puts "Part A Answer: #{ans_a}"


board_b = board_a.explode
pp board_b
puts "Board_b size: #{board_b.grid.length}"

ans_b = board_b.solve_b
puts "Part B Answer: #{ans_b}"


# expected = "DUNNO"
# raise "WRONG! #{ans} should be #{expected}" unless ans == expected



# Part A: Answer: 6599 -  That's the right answer!
# Part B Answer: 477 - That's the right answer!