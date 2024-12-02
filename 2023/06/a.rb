
class Race
  attr_accessor :time, :record

  def initialize(time, record)
    self.time = time
    self.record = record
  end

  # def inspect
  #   "race: time: #{time} record: #{record}"
  # end

  def winner_count
    (1..time).select do |t|
      dist = t * (time - t)
      puts "time #{t} goes #{dist}, compared to #{record} #{dist > record ? "WINNNER" : nil}" if time % 100000 == 0
      dist > record
    end.count
  end

  def solve
    winner_count
  end
end

def solve(races)
  races.map do |race|
    pp race
    race.solve
  end.inject(&:*)
end


# # Sample data:
# races = [
#   Race.new(7, 9),
#   Race.new(15, 40),
#   Race.new(30, 200),
# ]

# # Actual data:
# races = [
#   Race.new(54, 239),
#   Race.new(70, 1142),
#   Race.new(82, 1295),
#   Race.new(75, 1253),
# ]

# # Part B SAMPLEdata:
# races = [
#   Race.new(71530, 940200),
# ]

# # Part B Actual data:
# Time:   54708275
# Distance:   239114212951253
# Answer :45128024 -- That's the right answer
races = [
  Race.new(54708275, 239114212951253),
]

pp races

ans = solve(races)


puts "Answer: #{ans}"