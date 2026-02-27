require 'set'

def parse_versions(lockfile)
  versions = {}
  File.readlines(lockfile).each do |line|
    if line =~ /^\s{4}(\S+)\s+\(([^)]+)\)/
      gem_name = $1
      version = $2.split(',').first.strip
      versions[gem_name] = version
    end
  end
  versions
end

old_versions = parse_versions('old_gemfile.lock')
new_versions = parse_versions('Gemfile.lock')

upgrades = []
new_versions.each do |gem, new_ver|
  old_ver = old_versions[gem]
  if old_ver && old_ver != new_ver
    upgrades << { gem: gem, old: old_ver, new: new_ver }
  end
end

puts "## Dependency Upgrades Detected:"
if upgrades.empty?
  puts "No version changes detected"
else
  upgrades.each do |u|
    puts "- #{u[:gem]}: #{u[:old]} → #{u[:new]}"
  end
end

# Save to file for later use
File.open('upgrades.txt', 'w') do |f|
  upgrades.each do |u|
    f.puts "#{u[:gem]}|#{u[:old]}|#{u[:new]}"
  end
end
