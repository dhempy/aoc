

ans = 0

# The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
# The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36,
# respectively. Adding up these five powers produces the sum 2286.


ans = STDIN.map {  |line|
  puts line
  (game_num, reveals) = line.match(/Game (\d+): (.*)/).captures

  puts "Game: #{game_num}"
  puts "Reveals: #{reveals}"

  need =  { 'red' => 0, 'green' => 0, 'blue' => 0 }


  good = reveals.split('; ').each do |reveal|
    puts " reveal #{reveal}"

    reveal.split(', ').each do |num_color|
      (num, color) = num_color.split(' ')
      num = num.to_i
      puts "   #{num} of #{color}"
      need[color] = num if need[color] < num
    end # .tap {|bool| puts "  reveal good: #{bool}"}
  end # .tap {|bool| puts " all reveals good: #{bool}"}


  puts "need: #{need}"
  power = need.values.inject(:*)
  puts "power: #{power}"
  # ans += game_num.to_i if good
  puts
  power
}.sum


puts "Answer: #{ans}"