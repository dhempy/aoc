class Node
  attr_accessor :raw, :name, :steps

  def initialize(line)
    self.raw = line

    # AAA = (BBB, CCC)
    # puts "  line: [#{line}]"
    (name, left, right) = line.match(/(\w+) = \((\w+), (\w+)\)/).captures
    self.name = name

    self.steps = {}
    self.steps['L'] = left  # BBB
    self.steps['R'] = right # CCC
  end

  def advance(turn)
    hence = steps[turn]
    puts "  #{self.name}.advance(#{turn}) => hence: #{hence}"
    hence

    # steps[turn]
  end

  def finished?
    name[-1] == 'Z'
  end

  def shortest_path(board, dest, so_far = 0)
    puts "  #{self.name}.shortest_path(board, #{dest}, #{so_far})"
    if (dest == self.name)
      puts "  FOUND #{dest} in #{so_far} steps!"
      return so_far
    end
    turn = board.turns[so_far % board.turns_len]
    hence = steps[turn]

    puts "  turn: #{turn}, hence: #{hence}"
    board.nodes[hence].shortest_path(board, dest, 1+so_far)

    # steps.values.min do |toward|
    #   Board.nodes[toward].shortest_path(dest, 1+so_far)
    # end
  end
end

class Ghost
  attr_accessor :board, :initial, :current, :period

  def initialize(board, initial)
    @board = board
    @initial = initial
    @current = initial
    enperiod
  end

  def advance()
    # puts "  #{initial}...#{current}.advance(): period: #{period}"
    turn = board.turns[period % board.turns_len]
    node = board.nodes[current]
    # puts "    Node to advance: #{node}, #{turn}"
    @current = node.advance(turn)
    @period += 1
  end


  def enperiod
    @period = 0
    advance until finished?
    puts " ghost[:initial].period => #{period}"

  end

  def finished?
    # raise if period > 10
    current[-1] == 'Z'
  end
end

class Board
  attr_accessor :nodes, :turns, :turns_len, :ghosts

  def parse
    puts "\nPARSE =========================== "

    # e.g. LLRRRLLLRLRLRL
    step_string = STDIN.readline.match(/([LR]+)/).captures.first
    self.turns = step_string.chars
    self.turns_len = turns.size
    puts "turns: #{turns} (num: #{turns_len})"

    self.nodes = {}
    STDIN.each do |line|
      line.chomp!
      next if line.empty?
      puts "input: [#{line}]"
      node = Node.new(line.chomp)
      self.nodes[node.name] = node
    end
  end

  def initialize
    puts "\nINIT =========================== "
    parse

    ghost_names = nodes.keys.select { |n| n[-1] == 'A' }

    self.ghosts = ghost_names.map { |name| Ghost.new(self, name) }

    puts "turns:"
    pp turns
    puts "nodes:"
    pp nodes
    # puts "ghosts:"
    # pp ghosts
  end

  def advance_fleet(turn)
    puts
    ghosts.each_with_index { |g, n| ghosts[n] = nodes[g].advance(turn) }
  end

  def advance_first(turn)
    puts
    ghosts.each_with_index { |g, n| ghosts[n] = nodes[g].advance(turn); return }
  end

  def fleet_finished?
    ghosts.all? { |g| g[-1] == 'Z' }
  end

  def ghost_fleet_navigate
    puts "\nghost_fleet_navigate() =========================== "

    steps = 0
    until fleet_finished?
      puts "steps: #{steps}"  if steps%100000 == 0
      # pp ghosts
      turn = turns[steps % turns_len]
      advance_fleet(turn)
      # advance_first(turn)
      steps += 1

      # raise if steps > 10
    end

    puts "FLEET FINISHED in #{steps} steps!"
    steps
  end

  def ghost_LCM
    periods = ghosts.map(&:period).uniq
    puts "PERIODS: #{periods}"
    # lcm = periods.inject(&:*)
    lcm = periods.reduce(&:lcm)
    puts "lcm: #{lcm}"
    lcm
  end

  def solve
    # ghost_fleet_navigate
    ghost_LCM
  end
end

# Next strategy:
# Next strategy:
# Next strategy:
# Next strategy:
# Next strategy:
# Next strategy:
# # Next strategy:
#   - Measure the repeat period of each ghost
#   - Find the least common multiple of those periods. Hopefully that's the solution.
#   - If not, add in the pre-repeat offset of each, and ???


board = Board.new

ans = board.solve

puts "Answer: #{ans}"


# Part A:
# Answer: 13019 - That's the right answer!

# Part B:
# Answer: 22054907450270570746800047 - That's not the right answer; your answer is too high. (This was product, not LCM)
# Answer: 13524038372771 - That's the right answer!  - LCM, calculated elswehere

# Failing when Iterating for 12 hours:
# steps: 20,879,900,000
# steps: 20,880,000,000
# ^Cb.rb:23:in `advance': Interrupt