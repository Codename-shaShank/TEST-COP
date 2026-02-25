## Dependency change summary

Base branch: ``

This PR updates the resolved gem set based on changes in `Gemfile` / `Gemfile.lock` (and related gemspec changes, if any).

### Direct dependencies (from Gemfile)

| Gem | Old | New | Change | Groups | Risk |
|-----|-----|-----|--------|--------|------|
| `bootsnap` | – | 1.18.3 | added | default | Medium |
| `capybara` | – | 3.40.0 | added | default | Medium |
| `chartkick` | – | 5.0.6 | added | default | Medium |
| `debug` | – | 1.9.1 | added | default | Medium |
| `devise` | – | 4.9.3 | added | default | Medium |
| `groupdate` | – | 6.4.0 | added | default | Medium |
| `importmap-rails` | – | 2.0.1 | added | default | Medium |
| `jbuilder` | – | 2.11.5 | added | default | Medium |
| `puma` | – | 5.6.8 | added | default | Medium |
| `rails` | – | 7.0.8.1 | added | default | Medium |
| `redis` | – | 4.8.1 | added | default | Medium |
| `selenium-webdriver` | – | 4.18.1 | added | default | Medium |
| `sprockets-rails` | – | 3.4.2 | added | default | Medium |
| `sqlite3` | – | 2.9.0 | added | default | Medium |
| `stimulus-rails` | – | 1.3.3 | added | default | Medium |
| `tailwindcss-rails` | – | 2.3.0 | added | default | Medium |
| `turbo-rails` | – | 2.0.5 | added | default | Medium |
| `web-console` | – | 4.2.1 | added | default | Medium |

### Transitive / stdlib gems (from Gemfile.lock only)

| Gem | Old | New | Change | Groups | Risk |
|-----|-----|-----|--------|--------|------|
| `actioncable` | – | 7.0.8.1 | added | runtime? | Medium |
| `actionmailbox` | – | 7.0.8.1 | added | runtime? | Medium |
| `actionmailer` | – | 7.0.8.1 | added | runtime? | Medium |
| `actionpack` | – | 7.0.8.1 | added | runtime? | Medium |
| `actiontext` | – | 7.0.8.1 | added | runtime? | Medium |
| `actionview` | – | 7.0.8.1 | added | runtime? | Medium |
| `activejob` | – | 7.0.8.1 | added | runtime? | Medium |
| `activemodel` | – | 7.0.8.1 | added | runtime? | Medium |
| `activerecord` | – | 7.0.8.1 | added | runtime? | Medium |
| `activestorage` | – | 7.0.8.1 | added | runtime? | Medium |
| `activesupport` | – | 7.0.8.1 | added | runtime? | Medium |
| `addressable` | – | 2.8.6 | added | runtime? | Medium |
| `base64` | – | 0.2.0 | added | runtime? | Medium |
| `bcrypt` | – | 3.1.20 | added | runtime? | Medium |
| `bindex` | – | 0.8.1 | added | runtime? | Medium |
| `builder` | – | 3.2.4 | added | runtime? | Medium |
| `concurrent-ruby` | – | 1.2.3 | added | runtime? | Medium |
| `crass` | – | 1.0.6 | added | runtime? | Medium |
| `date` | – | 3.3.4 | added | runtime? | Medium |
| `erubi` | – | 1.12.0 | added | runtime? | Medium |
| `globalid` | – | 1.2.1 | added | runtime? | Medium |
| `i18n` | – | 1.14.4 | added | runtime? | Medium |
| `io-console` | – | 0.7.2 | added | runtime? | Medium |
| `irb` | – | 1.12.0 | added | runtime? | Medium |
| `loofah` | – | 2.22.0 | added | runtime? | Medium |
| `mail` | – | 2.8.1 | added | runtime? | Medium |
| `marcel` | – | 1.0.4 | added | runtime? | Medium |
| `matrix` | – | 0.4.2 | added | runtime? | Medium |
| `method_source` | – | 1.0.0 | added | runtime? | Medium |
| `mini_mime` | – | 1.1.5 | added | runtime? | Medium |
| `minitest` | – | 5.22.3 | added | runtime? | Medium |
| `msgpack` | – | 1.7.2 | added | runtime? | Medium |
| `net-imap` | – | 0.4.10 | added | runtime? | Medium |
| `net-pop` | – | 0.1.2 | added | runtime? | Medium |
| `net-protocol` | – | 0.2.2 | added | runtime? | Medium |
| `net-smtp` | – | 0.4.0.1 | added | runtime? | Medium |
| `nio4r` | – | 2.7.0 | added | runtime? | Medium |
| `nokogiri` | – | 1.16.2 | added | runtime? | Medium |
| `orm_adapter` | – | 0.5.0 | added | runtime? | Medium |
| `psych` | – | 5.1.2 | added | runtime? | Medium |
| `public_suffix` | – | 5.0.4 | added | runtime? | Medium |
| `racc` | – | 1.7.3 | added | runtime? | Medium |
| `rack` | – | 2.2.8.1 | added | runtime? | Medium |
| `rack-test` | – | 2.1.0 | added | runtime? | Medium |
| `rails-dom-testing` | – | 2.2.0 | added | runtime? | Medium |
| `rails-html-sanitizer` | – | 1.6.0 | added | runtime? | Medium |
| `railties` | – | 7.0.8.1 | added | runtime? | Medium |
| `rake` | – | 13.1.0 | added | runtime? | Medium |
| `rdoc` | – | 6.6.2 | added | runtime? | Medium |
| `regexp_parser` | – | 2.9.0 | added | runtime? | Medium |
| `reline` | – | 0.4.3 | added | runtime? | Medium |
| `responders` | – | 3.1.1 | added | runtime? | Medium |
| `rexml` | – | 3.2.6 | added | runtime? | Medium |
| `rubyzip` | – | 2.3.2 | added | runtime? | Medium |
| `sprockets` | – | 4.2.1 | added | runtime? | Medium |
| `stringio` | – | 3.1.0 | added | runtime? | Medium |
| `thor` | – | 1.3.1 | added | runtime? | Medium |
| `timeout` | – | 0.4.1 | added | runtime? | Medium |
| `tzinfo` | – | 2.0.6 | added | runtime? | Medium |
| `warden` | – | 1.2.9 | added | runtime? | Medium |
| `websocket` | – | 1.2.10 | added | runtime? | Medium |
| `websocket-driver` | – | 0.7.6 | added | runtime? | Medium |
| `websocket-extensions` | – | 0.1.5 | added | runtime? | Medium |
| `xpath` | – | 3.2.0 | added | runtime? | Medium |
| `zeitwerk` | – | 2.6.13 | added | runtime? | Medium |

_Generated by gem_diff GitHub Action._
