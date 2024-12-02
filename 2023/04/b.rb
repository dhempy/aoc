
def parse_line(line)
  puts "  Line: #{line}"
  (id, wins, mine) = line.match(/Card +(\d+): (.*)\|(.*)/).captures
  id = id.to_i
  wins = wins.split.map{ |x| x.to_i }
  mine = mine.split.map{ |x| x.to_i }
  # puts "    wins: #{wins}"
  # puts "    mine: #{mine}"
  hits = mine.count { |m| wins.include?(m)}
  puts "    hits: #{hits}"
  card = {
    id: id,
    hits: hits,
    copies: 1,
  }
  puts card
  card
end

def parse
  STDIN.map {  |line|
    parse_line(line)
  }
end

def compound_scores
  @cards.each_with_index { |card, n|
    puts "#{n}: #{card}"
    hits = card[:hits] || 0
    if hits.positive?
      @cards[(n+1)..(n + hits)].each { |c1|
        puts " increment #{c1[:id]} by #{card[:copies]}..."
        c1[:copies] += card[:copies]
      }
    end
  }
end

def tally_scores
  @cards.sum { |c| c[:copies]}
end

@cards = [{copies: 0}] # array of one hash, to force 1-based array.
@cards = (@cards << parse).flatten
puts "\ncards:\n#{@cards}\n\n"

compound_scores
puts "\ncards:\n#{@cards}\n\n"

ans = tally_scores


puts "Answer: #{ans.inspect}"
