require 'net/http'
require 'uri'
require 'json'

def fetch_github_release_notes(gem_name, old_version, new_version)
  # Try common GitHub repo patterns
  potential_repos = [
    "#{gem_name}/#{gem_name}",
    "rails/#{gem_name}",
    "#{gem_name.gsub('-', '_')}/#{gem_name.gsub('-', '_')}"
  ]
  
  potential_repos.each do |repo|
    begin
      uri = URI("https://api.github.com/repos/#{repo}/releases")
      req = Net::HTTP::Get.new(uri)
      req['Accept'] = 'application/vnd.github.v3+json'
      req['Authorization'] = "token #{ENV['GH_TOKEN']}" if ENV['GH_TOKEN']
      
      res = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true, read_timeout: 10) { |http|
        http.request(req)
      }
      
      if res.is_a?(Net::HTTPSuccess)
        releases = JSON.parse(res.body)
        relevant_releases = releases.select { |r| 
          tag = r['tag_name'].gsub(/^v/, '')
          tag >= old_version && tag <= new_version
        }
        
        if relevant_releases.any?
          return {
            source: "GitHub releases (#{repo})",
            notes: relevant_releases.map { |r| 
              "### #{r['name'] || r['tag_name']}\n#{r['body']}" 
            }.join("\n\n")
          }
        end
      end
    rescue => e
      # Try next repo
    end
  end
  nil
end

def fetch_rubygems_changelog(gem_name)
  begin
    uri = URI("https://rubygems.org/api/v1/gems/#{gem_name}.json")
    res = Net::HTTP.get_response(uri)
    if res.is_a?(Net::HTTPSuccess)
      data = JSON.parse(res.body)
      changelog_uri = data['changelog_uri'] || data['source_code_uri']
      return { source: "RubyGems", url: changelog_uri } if changelog_uri
    end
  rescue => e
    # Ignore
  end
  nil
end

upgrades_file = 'upgrades.txt'
unless File.exist?(upgrades_file)
  puts "No upgrades file found"
  exit 0
end

all_notes = []
File.readlines(upgrades_file).each do |line|
  gem_name, old_ver, new_ver = line.strip.split('|')
  next unless gem_name
  
  puts "Fetching notes for #{gem_name} (#{old_ver} → #{new_ver})..."
  
  notes = fetch_github_release_notes(gem_name, old_ver, new_ver)
  unless notes
    notes = fetch_rubygems_changelog(gem_name)
  end
  
  if notes
    all_notes << "## #{gem_name} (#{old_ver} → #{new_ver})\n"
    if notes[:notes]
      all_notes << notes[:notes]
    elsif notes[:url]
      all_notes << "Changelog: #{notes[:url]}"
    end
    all_notes << "\n---\n"
  else
    all_notes << "## #{gem_name} (#{old_ver} → #{new_ver})\n"
    all_notes << "No changelog found. Check: https://rubygems.org/gems/#{gem_name}\n---\n"
  end
end

File.write('changelogs.txt', all_notes.join("\n")) if all_notes.any?
