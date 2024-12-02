
def solve_line(line)
  puts "  Line: #{line}"
  (wins, mine) = line.match(/: (.*)\|(.*)/).captures
  wins = wins.split.map{ |x| x.to_i }
  mine = mine.split.map{ |x| x.to_i }
  puts "    wins: #{wins}"
  puts "    mine: #{mine}"
  hits = mine.count { |m| wins.include?(m)}
  puts "    hits: #{hits}"
  return 0 if hits.zero?
  score = 2 ** (hits-1)
  puts "    score: #{score}"
  score
end

ans = STDIN.map {  |line|
  solve_line(line)
}.compact.sum



puts "Answer: #{ans}"