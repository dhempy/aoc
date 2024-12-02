

ans = 0

# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

# The Elf would first like to know which games would have been possible if the bag
# contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

MOST = {
  'red' => 12,
  'green' => 13,
  'blue' => 14
}

STDIN.each_line {  |line|
  puts line
  (game_num, reveals) = line.match(/Game (\d+): (.*)/).captures

  puts "Game: #{game_num}"
  puts "Reveals: #{reveals}"

  good = reveals.split('; ').all? do |reveal|
    puts " reveal #{reveal}"

    reveal.split(', ').all? do |num_color|
      (num, color) = num_color.split(' ')
      puts "   #{num} of #{color}"
      MOST[color] >= num.to_i
    end.tap {|bool| puts "  reveal good: #{bool}"}
  end.tap {|bool| puts " all reveals good: #{bool}"}


  puts "Game good? #{good}"

  ans += game_num.to_i if good
}


puts "Answer: #{ans}"



