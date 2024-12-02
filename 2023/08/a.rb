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


class Board
  attr_accessor :nodes, :turns, :turns_len

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

    puts "turns:"
    pp turns
    puts "nodes:"
    pp nodes
  end

  def shortest_path(src, dest)
    puts "\nSHORTEST_PATH(#{src}, #{dest}) =========================== "

    nodes[src].shortest_path(self, dest)
  end

  def solve
    shortest_path('AAA', 'ZZZ')
  end
end


board = Board.new

ans = board.solve

puts "Answer: #{ans}"


# Part A:
# Answer: 13019 - That's the right answer!


