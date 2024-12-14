require 'simplecov'
SimpleCov.start

# Previous content of test helper now starts here
RSpec.configure do |config|
  config.example_status_persistence_file_path = 'tmp/examples.txt'
  config.filter_run_when_matching :focus
end
