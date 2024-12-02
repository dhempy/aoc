class Hand
  attr_accessor :raw, :cards, :wager, :card_vals, :shape, :rank, :score

  CARD_VAL = {
    'A' => 14,
    'K' => 13,
    'Q' => 12,
    # 'J' => 11,
    'T' => 10,
    '9' => 9,
    '8' => 8,
    '7' => 7,
    '6' => 6,
    '5' => 5,
    '4' => 4,
    '3' => 3,
    '2' => 2,
    'J' => 1,
  }

  HAND_VAL = {
    '5' => 7,
    '41' => 6,
    '32' => 5,
    '311' => 4,
    '221' => 3,
    '2111' => 2,
    '11111' => 1,
  }

  def initialize(line)
    self.raw = line

    # QQQJA 483
    (cards, wager) = line.match(/(.....) (\d+)/).captures
    self.wager = wager.to_i
    self.cards = cards.chars
    self.card_vals = self.cards.map { |c| CARD_VAL[c] }
    self.enshape
  end

  def enshape
    # puts "\nenshape(card_vals)"
    histo = {}
    jokers = 0
    card_vals.each do |c|
      # puts "  c is #{c.inspect} #{c.class}"
      if c == 1 # Joker
        jokers += 1
      else
        histo[c] = histo[c].nil? ? 1 : histo[c] + 1
      end
    end

    freqs = histo.values.sort.reverse
    # puts "  shape: #{freqs} (before (#{jokers.class}) #{jokers} jokers)"
    freqs[0] = jokers + (freqs[0] || 0)
    # puts "  shape: #{freqs}"
    self.shape = freqs.join
    # puts "  shape: #{shape} (joined)"

    # puts "  hand: #{card_vals}"
  end

  def value
    # "#{HAND_VAL[shape]}#{card_vals}"
    [HAND_VAL[shape], card_vals].flatten
  end

  def enrank(r)
    rank = r
    self.score = rank * wager

    puts "enrank(#{r}) => #{cards} value: #{value} shape: #{shape } wager: #{wager} score: #{score} "
  end

  def solve
    wager
  end
end


class Board
  attr_accessor :hands

  def parse
    puts "\nPARSE =========================== "
    STDIN.map do |line|
      puts "input: #{line}"
      Hand.new(line.chomp)
    end # .tap { |a| pp a }
  end

  def initialize
    puts "\nINIT =========================== "
    self.hands = parse
  end

  def play
    puts "\nPLAY =========================== "

    # pp hands
    hands.sort! { |a,b| a.value <=> b.value }
    hands.each_with_index { |hand, n| hand.enrank(n+1) }
    self
  end

  def score
    # hands.sum(&:score)
    hands.map(&:score).sum
  end
end


board = Board.new

ans = board.play.score

puts "Answer: #{ans}"

# Part A - 249204891 -- correct
# Part B - 249666369 -- correct