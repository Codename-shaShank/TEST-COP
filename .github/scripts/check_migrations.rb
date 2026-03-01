#!/usr/bin/env ruby
# Script to detect and fix duplicate migration issues
# This prevents ActiveRecord::DuplicateMigrationNameError

require 'pathname'

migration_dir = 'db/migrate'
migrations = {}
duplicates = []

unless Dir.exist?(migration_dir)
  puts "✅ No migrations directory found"
  exit 0
end

# Parse migrations and find duplicates
Dir.glob("#{migration_dir}/*.rb").sort.each do |file|
  basename = File.basename(file)
  # Extract class name from migration file
  content = File.read(file)
  if content =~ /class\s+(\w+)\s*<\s*ActiveRecord::Migration/
    class_name = $1
    if migrations[class_name]
      # Found a duplicate
      duplicates << {
        class_name: class_name,
        existing: migrations[class_name],
        new: file
      }
    else
      migrations[class_name] = file
    end
  end
end

if duplicates.empty?
  puts "✅ No duplicate migrations found"
  exit 0
end

puts "⚠️  Found #{duplicates.length} duplicate migration(s):"
duplicates.each_with_index do |dup, idx|
  puts "  #{idx + 1}. Class: #{dup[:class_name]}"
  puts "     Existing: #{dup[:existing]}"
  puts "     Duplicate: #{dup[:new]}"
end

# Fix strategy: Keep the NEWER migration (higher timestamp) and remove older ones
puts "\n🔧 Attempting to fix duplicates (keeping newer versions)..."

fixed = []
duplicates.each do |dup|
  existing_time = File.mtime(dup[:existing])
  new_time = File.mtime(dup[:new])

  if existing_time < new_time
    # existing is older, remove it
    file_to_remove = dup[:existing]
    to_keep = dup[:new]
  else
    # new is older, remove it
    file_to_remove = dup[:new]
    to_keep = dup[:existing]
  end

  puts "  Removing (older):  #{file_to_remove}"
  puts "  Keeping (newer):   #{to_keep}"

  File.delete(file_to_remove)
  fixed << file_to_remove
end

if fixed.any?
  puts "\n✅ Fixed #{fixed.length} duplicate migration(s)"
  puts "\nFiles deleted:"
  fixed.each { |f| puts "  - #{f}" }
  exit 1  # Exit code 1 signals that changes were made
else
  puts "✅ No duplicates needed fixing"
  exit 0
end
