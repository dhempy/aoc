
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

class Node
  def next_move(dir)
    PASSAGE.dig(c, dir)
  end
end

class Board
  def finished?
    [@curr_row, @curr_col] == [@start_row, @start_col]
  end

  def go(dir)
    @curr_row += dir[0]
    @curr_col += dir[1]
    @here = grid[@curr_row][@curr_col]
    @dist = @dist + 1
  end

  # records the full distance of the loop in @dist,
  # and marks loop with WALL characters.
  def survey_pipe(mark_walls = false)
    delta = S # This is a known valid starting direction for the given input. Adjust as needed.

    loop do
      go(delta)
      delta = @here.next_move(delta)
      @here.c = WALL if mark_walls
      break if finished?
      break if delta.nil?
    end
  end

  def solve_a
    survey_pipe
    @part_a_solution = @dist / 2
  end

  def solve_b
    survey_pipe(true)
    @waters = flood(WATER, 0, 0)
    r, c = find_dry_neighbor(@start_row, @start_col)
    @drys = flood(LAND, r, c)
    @part_b_solution = cell_count(LAND)
  end
end


board_a = Board.new
answer_a =  board_a.parse.solve_a
board_b = board_a.explode
answer_b = board_b.solve_b
