
@possible_counts = {}

# Returns the number of solutions to the input
# pattern and word_needs, remains the same throughout.
# str builds up to the same length as pattern
def solutions(pattern, word_needs, str = '', possible_counts = {})
  # puts "solutions('#{pattern}', #{word_needs}, '#{str}')"

  if str = ''
    total_need = word_needs.sum
    total_skip = pattern.length - total_need
    @possible_counts = {}
  end

  action = check_solution(pattern, word_needs, str, total_need, total_skip, possible_counts)
  # puts "    check_solution returned '#{action}'"

  case action
  when :GO_ON
    # puts "   GO_ON: #{str}"
    poss =  find_next_strings_greedy(pattern, str)
    # puts "  possibilities: #{poss}"
    return poss.sum do |longer_str|
      solutions(pattern, word_needs, longer_str, possible_counts)
        # .tap  {|n| puts "      found #{n} sub-solutions"}
    end
  when :COMPLETE
    # puts "       >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> COMPLETE: #{str}"
    return 1
  else
    # puts "    HALT: #{str} (#{action})"
    return 0
  end
end

# Looks for reasons to stop processing.
# Returns GO_ON if no reason found, and str can continue to be built up.
# Returns COMPLETE if this is a completely correct end solution.
# Returns any other code to indicate why this str is not viable.
# word_needs is the *entire* needs, not just remaining.
def check_solution(pattern, word_needs, str, total_need, total_skip, possible_counts)
  # puts "    check_solution('#{pattern}', word_needs, '#{str}')"
  return :TOO_LONG     if str.size > pattern.size

  # # this could go in check_needs:
  # char_count = str.count('#')
  # need_count = word_needs.sum
  # puts "char_count=#{char_count} need_count=#{need_count}"
  # return :TOO_WORDY    if char_count > need_count

  return :BAD_PATTERN  if !pattern_match?(pattern, str)

  return :FAILED_NEEDS if remainder_impossible?(pattern, word_needs, str, total_need, total_skip, possible_counts)

  need_stat = check_needs(word_needs, str, str.size == pattern.size)
  # puts "      need_stat=#{need_stat}"
  return :FAILED_NEEDS if need_stat == :FAILED_NEEDS
  return :COMPLETE     if need_stat == :COMPLETE && str.size == pattern.size
  return :GO_ON        if need_stat == :GO_ON


  return :GO_ON        if str.size < pattern.size

  # return :COMPLETE     if need_stat == :COMPLETE
  # return :COMPLETE     if str.size == pattern.size ## This may be too weak.

  # To do: Find many more ways to strike down INVALID attempts early on.

  raise "Should never get this far. What happened?"
end

# Only checks through str. string may become invalid when it grows longer.
def pattern_match?(pattern, str)
  str.chars.zip(pattern.chars).all? do |s, p|
    # puts "pattern_match(#{p}, #{s})"
    p == s || p=='?'
  end
end

def remainder_impossible?(pattern, word_needs, str, total_need, total_skip, possible_counts)
  puts "remainder_impossible?('pattern', word_needs, '#{str}')"


  so_far_word = str.count '#'
  so_far_skip = str.length - so_far_word


  cursor = str.length
  # puts "  cursor  is #{cursor}"

  if cursor == 0
    rest = pattern
  else
    rest = pattern[cursor..]
    # puts "    used  is '#{used}'"
  end

  could_add  = possible_count(rest, ['#','?'], possible_counts)
  could_skip = possible_count(rest, ['.','?'], possible_counts)
  # could_add  = rest.count('#') + rest.count('?')
  # could_skip = rest.count('.') + rest.count('?')

  puts "  need:#{total_need} have:#{so_far_word} could_add:#{could_add} could_skip:#{could_skip}"

  if total_need > so_far_word + could_add
    puts "     remainder is IMPOSSIBLE. Not enough words. STOP"
    return true
  end

  if total_skip > so_far_skip + could_skip
    puts "     remainder is IMPOSSIBLE. Not enough blanks. STOP"
    return true
  end

  puts "     remainder is possible. KEEP GOING"
  return false
    # .tap { |too_hard| puts too_hard ? ' ------ IMPOSSIBLE -------' :  ' >>>>>>>> KEEP GOING ------'}
end

def possible_count(substr, chars, possible_counts)
  puts "    possible_count(#{substr}, #{chars})"
  puts "      hash: #{possible_counts}"
  key = "#{substr}~#{chars}"
  if !@possible_counts[key]
    puts "      NOT CHACHED...COMPUTE:"
    @possible_counts[key] = chars.map{ |c| substr.count(c)}.sum
  end

  puts "      hash: #{possible_counts}"

  puts "      possible_count is #{@possible_counts[key]}"
  return @possible_counts[key]
end

# Only checks all of current str. string may become invalid when it grows longer.
# if exact_match, then the needs must be exact_match, exactly met.
def check_needs(word_needs, str, exact_match)
  # puts "check_needs?(#{word_needs}, '#{str}', #{exact_match})"
  # binding.pry

  word_lengths = str.split('.').map(&:length).select(&:positive?)

  if exact_match
    # puts "  COMPLETE? word_lengths=#{word_lengths} word_needs:#{word_needs}"

    return :COMPLETE if word_lengths == word_needs
    return :FAILED_NEEDS if word_lengths.length != word_needs.length

    expecations = [word_needs].zip(word_lengths)
    if expecations.any? { |have, expected|
                          # puts "  (have)#{have} != #{expected}(expected)"
                          have != expected
                        }
      return :FAILED_NEEDS
    else
      return :COMPLETE
    end
  end

  # puts "    // word_lengths=#{word_lengths} word_needs:#{word_needs}"
  # puts "  GO_ON? (!exact_match)"
  return :GO_ON if word_lengths.empty? && !exact_match

  latest_word_index = word_lengths.count - 1
  # puts "  latest_word_index: #{latest_word_index}"

  if latest_word_index > 0 # then there is a prior word
    # puts "  FAILED_NEEDS? (pattern mismatch in prior words, excluding current_word)"
    expecations = word_lengths[..(latest_word_index-1)].zip(word_needs)
    return :FAILED_NEEDS if
        expecations.any? { |have, expected|
          # puts "  (have)#{have} != #{expected}(expected)"
          have != expected
        }
  end

  # puts "  complete?"
  # return :COMPLETE if exact_match && word_lengths == word_needs

  # puts "  FAILED_NEEDS? (exact)"

  # return :FAILED_NEEDS if exact_match && word_lengths != word_needs

  # puts "  FAILED_NEEDS? (so far)"

  # puts " (word_lengths[latest_word_index] > word_needs[latest_word_index]) "
  # puts " (#{word_lengths[latest_word_index]} > #{word_needs[latest_word_index]}) "
  # return :FAILED_NEEDS if (word_lengths[latest_word_index] > word_needs[latest_word_index])

  # puts "  GO_ON? (first word)"
  return :GO_ON if latest_word_index == 0 # e.g. they're on their first word...nothing else to check.

  # puts " (word_lengths[..(latest_word_index-1)].zip(word_needs).any? { |a, b| a != b }) "
  # puts " (word_lengths[..(latest_word_index-1)].zip(word_needs).any? { |a, b| a != b }) "


  # puts '  GO ON...nothing else matched'
  return :GO_ON
end




# Returns an array of possible next steps.
# Steps are each an array: [longer_str].
#   longer_str is a new array, exactly one char longer than dst.
# Pays no regard to pattern at all.
# New strings may be too long, too short, or invalid against pattern.
# If dst ends in "#"", and need_counds starts with zero,
#   then a new word is started ("." addedd), and the zero in need_counds is removed.
def find_next_strings_greedy(pattern, current_string)
  # puts "find_next_strings_greedy('pattern', '#{current_string}')"

  cursor = current_string.length

  if pattern[cursor] == '?'
    return find_dynamic_possibilities(pattern, current_string)
  else
    return find_static_possibilities(pattern, current_string)
  end
end


def find_static_possibilities(pattern, current_string)
  # puts "find_static_possibilities('pattern', '#{current_string}')"

  # puts " pattern  is '#{pattern}'"

  cursor = current_string.length
  # puts "  cursor  is #{cursor}"

  if cursor == 0
    rest = pattern
  else
    # used = pattern[..cursor-1]
    rest = pattern[cursor..]

    # puts "    used  is '#{used}'"
  end

  # puts "    rest  is '#{rest}'"
  if (stop = rest.index('?'))
    # puts "    stop  is '#{stop}'"
    chunk = rest[..stop-1]
    # puts "    chunk is '#{chunk}'"

    return [current_string + chunk]
  else
    return [current_string + rest]

  end
end

def find_dynamic_possibilities(pattern, current_string)
  # puts "find_dynamic_possibilities('pattern', '#{current_string}')"

  [
    current_string + '#',
    current_string + '.'
  ]
end
















class Record
  def initialize(pattern, counts)
    # puts "Board.init(\"#{pattern}\", [#{counts}])"

    @pattern = pattern

    # This approach keeps needs as an array of ints.
    # This will be used to recursively create many permutations of those needs.
    @word_needs = counts.split(',').map { |n| n.to_i }

    # for part b:

    @pattern = [@pattern, @pattern, @pattern, @pattern, @pattern].join('?')
    @word_needs = @word_needs + @word_needs + @word_needs + @word_needs + @word_needs
    # puts inspect
  end

  def solve
    solutions(@pattern, @word_needs)
      .tap { |n| puts "  ++ Found #{n} solutions for #{@pattern}, #{@word_needs}"}
  end

  def expect_solution(expected)
    # puts inspect
    # puts "expect_solution(#{expected}): pattern=#{@pattern} word_needs=#{@word_needs} haves=#{haves}"
    got = solutions(@pattern, @word_needs)

    msg = "Got #{got}, expected #{expected} from \n#{inspect}"
    if got == expected
      # puts "PASSED: #{msg}\n\n"
    else
      raise "FAIL: #{msg}"
      # raise "FAIL: #{msg}"
    end
  end

  def inspect
    <<~INSP
     <Record: pattern =#{@pattern}
              word_needs=#{@word_needs}
              haves=#{@haves}>
    INSP
              # => #{haves}
  end
end






class Board
  attr_accessor :records

  def parse
    # puts "\nPARSE =========================== "
    # e.g. ?###???????? 3,2,1
    @records = STDIN.map do |line|
                      line.chomp!
                      next if line.empty?
                      # puts "input: [#{line}]"
                      pattern, counts = line.split(' ')
                      Record.new(pattern, counts)
                    end
  end

  def initialize
    # puts "\nINIT =========================== "
    parse

    pp self
  end

  def solutions
    # puts @records

    @records.sum do |rec|
      rec.solve
    end
  end
end

# board = Board.new
# ans_a = board.solutions_a
# puts "Answer: #{ans_a}"

board = Board.new
ans_b = board.solutions
puts "Answer: #{ans_b}"


# Part A:
# 7221 - Correct!
# Part B:
