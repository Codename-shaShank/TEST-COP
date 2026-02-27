# Copilot Instructions

## Project Overview

This is a **URL shortener** web application built with Ruby on Rails 8.1. It allows users to shorten URLs, track click analytics, and manage their links. URLs are encoded using Base62 to produce short identifiers.

## Technology Stack

- **Language**: Ruby 3.2
- **Framework**: Rails 8.1 (note: `config.load_defaults` is intentionally kept at `7.0` in `config/application.rb` to preserve existing behaviour; do not bump it without auditing the Rails upgrade guide)
- **Database**: SQLite 3 (via `sqlite3` gem ≥ 2.1)
- **Web server**: Puma ≥ 6.0
- **Frontend**: Tailwind CSS, Hotwire (Turbo + Stimulus), ImportMaps
- **Authentication**: Devise (~> 4.9)
- **Analytics**: Chartkick (~> 5.0) + Groupdate (~> 6.4)
- **Caching / Action Cable**: Redis (~> 4.0)
- **Testing**: Rails Minitest (default), Capybara, Selenium WebDriver
- **CI**: GitHub Actions (`.github/workflows/ci.yml`)

## Key Models

- `Link` – a shortened URL; uses `Base62` encoding for its `to_param` / `find` override
- `User` – Devise-managed; owns many `Link` records
- `View` – tracks each click/visit for a `Link`
- `Metadata` – background-fetched page metadata for a link (via `MetadataJob`)

## Build & Test Commands

```bash
# Install dependencies
bundle install

# Set up database (create + migrate + seed)
bin/rails db:setup

# Prepare test database
bin/rails test:prepare

# Run all tests
bin/rails test

# Run a specific test file
bin/rails test test/models/link_test.rb

# Start the development server
bin/dev
```

## Conventions & Patterns

- **Controllers** use `before_action` for authentication (`authenticate_user!`) and resource loading (`set_link`). Follow the same pattern for new resources.
- **Turbo Streams**: The `create` action in `LinksController` responds to both HTML and `turbo_stream` formats. Follow this pattern when adding real-time UI updates.
- **Base62 encoding**: Short codes are Base62-encoded database IDs. Never expose raw integer IDs in routes; always go through `to_param` / `Base62`.
- **Scopes**: Use named scopes (e.g., `scope :recent_first`) for common query patterns.
- **Background jobs**: Use Active Job (`*Job` classes under `app/jobs/`) for async work such as metadata fetching.
- **Strong parameters**: Always use `params.require(...).permit(...)` in controllers.

## Dependency Notes

- **sqlite3**: Pinned to `>= 2.1` for Rails 8 compatibility. Do not downgrade.
- **redis**: Pinned to `~> 4.0`. The `redis` 5.x API has breaking changes; keep on 4.x unless explicitly upgrading and adapting the code.
- **devise**: Pinned to `~> 4.9`. Devise 5.x has breaking changes; keep on 4.x unless explicitly upgrading.
- **jbuilder**: Requires `>= 2.13` for Rails 8 compatibility (`ActiveSupport::ProxyObject` was removed).
- **puma**: Requires `>= 6.0` for Rack 3 / Rails 8 compatibility.

## Dependabot & Auto-Fix Workflows

This repository uses Dependabot (`.github/dependabot.yml`) for weekly bundler updates, with automated fix workflows in `.github/workflows/`:

- `ci.yml` – runs `bin/rails test:prepare && bin/rails test` on every PR and push to `main`.
- `dependabot-auto-fix.yml` – attempts to automatically fix CI failures on Dependabot PRs using GitHub Models AI.
- `auto-fix-main.yml` – broader auto-fix automation.

When working on Dependabot PRs:
1. Do **not** downgrade gems; adapt the code to the new version.
2. Check the gem's CHANGELOG for breaking changes before editing code.
3. Run `bin/rails test:prepare && bin/rails test` to confirm CI would pass.
