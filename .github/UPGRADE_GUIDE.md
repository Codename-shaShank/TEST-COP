# 🚀 Multi-Language Dependency Upgrade Guide

This guide helps the AI understand which dependencies have breaking changes and how to fix them.

## 📋 Supported Languages & Dependency Managers

| Language | Package Manager | Lock File | Detection |
|----------|-----------------|-----------|-----------|
| **Ruby** | Bundler | `Gemfile.lock` | `Gemfile` present |
| **Node.js** | npm | `package-lock.json` | `package.json` + no lock files |
| **Node.js** | Yarn | `yarn.lock` | `yarn.lock` present |
| **Node.js** | pnpm | `pnpm-lock.yaml` | `pnpm-lock.yaml` present |
| **Python** | pip | `requirements.txt` | `requirements.txt` present |
| **Python** | Poetry | `poetry.lock` | `poetry.lock` present |
| **Python** | Pipenv | `Pipfile.lock` | `Pipfile.lock` present |
| **Java** | Maven | `pom.xml` | `pom.xml` present |
| **Java** | Gradle | `build.gradle` | `build.gradle(.kts)` present |
| **PHP** | Composer | `composer.lock` | `composer.json` present |
| **.NET** | NuGet | `*.csproj` | `*.csproj` present |

---

## 🔴 MAJOR VERSION UPGRADES (High Risk)

### Ruby/Rails Upgrades

#### Rails 7.x → 8.0
**Breaking Changes:**
```ruby
# ❌ BEFORE (Rails 7)
render :json => data
has_secure_password :password

# ✅ AFTER (Rails 8)
render json: data  # Hash rocket syntax removed for keyword args
has_secure_password  # No longer accepts password argument
```

**Common Fixes:**
- Remove `require 'bundler/setup'` from bin/spring, bin/rails
- Move `Gem::Specification#loaded_specs` to `Gem.loaded_specs`
- Update before_filter to before_action in controllers
- Check Rack 3.0 compatibility (cookies, query string parsing)

**Test Command:**
```bash
bin/rails test
```

#### Rails 6.x → 7.0
**Breaking Changes:**
```ruby
# Sprockets -> Importmap/esbuild
# YAML.unsafe_load → YAML.load (with permitted classes)

# ❌ BEFORE
ApplicationRecord.find(id)  # Could raise or return nil inconsistently

# ✅ AFTER
ApplicationRecord.find(id)  # Always raises ActiveRecord::RecordNotFound
```

**Upgrade Path:**
```bash
rails app:update  # Run Rails upgrader generator
bundle update --major rails
````

---

### Node.js/JavaScript Upgrades

#### Express 4 → 5
**Breaking Changes:**
```javascript
// ❌ BEFORE
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());

// ✅ AFTER
app.use(express.json());
app.use(express.urlencoded());
```

#### Webpack 4 → 5
**Breaking Changes:**
```javascript
// ❌ BEFORE
entry: './src/index.js',  // Implicit default

// ✅ AFTER
entry: {
  main: './src/index.js'  // Explicit entry
}
```

#### Next.js 12 → 13
**Breaking Changes:**
```javascript
// ❌ BEFORE - pages/api/hello.js
export default (req, res) => {
  res.json({})
}

// ✅ AFTER - app/api/hello/route.js (App Router)
export async function GET(request) {
  return Response.json({})
}
```

**Test Command:**
```bash
npm test
```

---

### Python Upgrades

#### Django 3.x → 4.0
**Breaking Changes:**
```python
# ❌ BEFORE
from django.conf.urls import url
urlpatterns = [url(r'^article/(?P<year>[0-9]{4})/$', views.year_archive)]

# ✅ AFTER
from django.urls import path, re_path
urlpatterns = [
    path('article/<int:year>/', views.year_archive),
    # or: re_path(r'^article/(?P<year>[0-9]{4})/$', views.year_archive)
]
```

#### Python 2 → Python 3
**Breaking Changes:**
```python
# ❌ BEFORE (Python 2)
print "Hello"
xrange(10)
unicode("text")

# ✅ AFTER (Python 3)
print("Hello")
range(10)
"text"  # All strings are unicode by default
```

**Test Command:**
```bash
python -m pytest
# or: python -m unittest discover
```

---

### Java Upgrades

#### Java 8 → Java 11+
**Breaking Changes:**
```java
// ❌ BEFORE - Java 8
import javax.xml.bind.JAXBContext;

// ✅ AFTER - Java 11+
// Add dependency: com.sun.xml.bind:jaxb-impl
import javax.xml.bind.JAXBContext;
```

#### Spring Boot 2.x → 3.x
**Breaking Changes:**
```java
// ❌ BEFORE
@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)

// ✅ AFTER - configuration has changed significantly
spring.datasource.hikari.auto-commit=false
```

**Test Command:**
```bash
mvn test
# or: ./gradlew test
```

---

### PHP Upgrades

#### PHP 7 → PHP 8
**Breaking Changes:**
```php
// ❌ BEFORE
class User {}
function foo() {
    $x = 1;
    echo "Hello {$x} world";  // Variable interpolation
}

// ✅ AFTER
readonly class User {}  // New readonly keyword
function foo() {
    $x = 1;
    echo "Hello {$x} world";  // Still works but preferred: "Hello $x world"
}
```

#### Laravel 8 → 9
**Breaking Changes:**
```php
// ❌ BEFORE
use Illuminate\Support\Facades\Route;
Route::get('/users', 'UserController@index');

// ✅ AFTER
Route::get('/users', [UserController::class, 'index']);
```

**Test Command:**
```bash
php artisan test
# or: ./vendor/bin/phpunit
```

---

## 🟡 MINOR VERSION UPGRADES (Medium Risk)

### Patch Updates
- Usually safe; minimal breaking changes
- May include deprecation warnings
- Security fixes included

### Minor Updates
- May include new features
- Deprecation warnings increase
- Some API changes possible

**Common patterns:**
```ruby
# Gems may move methods around
User.where(active: true).count  # ❌ DEPRECATED
User.where(active: true).size   # ✅ NEW
```

---

## 🟢 SECURITY & PATCH UPDATES (Low Risk)

- No API changes
- Only bug fixes and security patches
- Safe to apply automatically

---

## 🛠️ AI-Generated Fix Format

### Expected Fix Output Format

```
### ANALYSIS:
[Explain the root cause and which dependencies caused it]

### FIX: path/to/file.rb
```ruby
# Show BEFORE and AFTER clearly
# ❌ BEFORE:
old_code_here

# ✅ AFTER:
new_code_here
```

### FIX: path/to/another/file.rb
```ruby
[More fixes if needed]
```

### COMMIT_MESSAGE:
fix: [framework/library]: [brief description of the fix]
```

---

## 📚 Language-Specific Resources

### Ruby/Rails
- **Official Upgrade Guides**: https://guides.rubyonrails.org/
- **Release Notes**: https://github.com/rails/rails/releases
- **Deprecation Checklist**: Look for `Rails.logger.warn` output

### Node.js/JavaScript
- **Migration Guides**: https://nodejs.org/en/docs/guides/
- **npm Registry**: https://www.npmjs.com/
- **Semver**: https://semver.org/

### Python
- **What's New**: https://docs.python.org/3/whatsnew/
- **PyPI**: https://pypi.org/
- **Deprecation Warnings**: Run with `python -W all`

### Java
- **Release Notes**: https://www.oracle.com/java/technologies/
- **Maven Central**: https://mvnrepository.com/
- **Gradle Docs**: https://docs.gradle.org/

### PHP
- **PHP Manual**: https://www.php.net/manual/
- **Packagist**: https://packagist.org/
- **Symfony/Laravel Docs**: Framework-specific

### .NET
- **Release Notes**: https://github.com/dotnet/runtime/releases
- **NuGet**: https://www.nuget.org/
- **Breaking Changes**: https://docs.microsoft.com/en-us/dotnet/

---

## 🔍 How the Workflow Works

1. **Detect Language** - Automatically identifies project type
2. **Detect Upgrades** - Compares lockfiles for version changes
3. **Fetch Guides** - Downloads release notes and breaking changes
4. **Run Tests** - Executes language-specific test commands
5. **AI Analysis** - Sends test failures + upgrade context to AI
6. **Auto-Fix** - Applies suggested code changes
7. **Verify** - Re-runs tests to validate fixes
8. **Up to 3 Iterations** - Refines fixes if tests still fail

---

## ⚠️ Limitations & Manual Review Cases

### When Manual Review is REQUIRED:

1. **Major Framework Upgrades** (Rails 6→7, Django 2→3)
   - Complex refactoring often needed
   - Configuration changes not caught by tests
   - Architecture changes (API routing, middleware)

2. **Multiple Major Dependencies** Upgrading Simultaneously
   - Conflicting changes between libs
   - Complex interactions not obvious from test failures

3. **Deprecated Features** You're Still Using
   - Code may work but warnings appear
   - Better patterns exist but require human judgment

4. **Breaking Changes in Dependencies**
   - Not caught by your test suite
   - Require understanding of API semantics
   - May need new code for removed features

### Success Rates by Change Type:

| Change Type | AI Success | Reason |
|-------------|-----------|--------|
| Syntax/API changes | 80-90% | Clear patterns, obvious errors |
| Method signature changes | 70-80% | Good error messages |
| Single-file logic | 40-60% | Requires context understanding |
| Multi-file refactoring | 10-30% | Too complex, needs human judgment |
| Architecture changes | <5% | Semantic understanding needed |

---

## 🎯 Best Practices

### Before Upgrading:
1. Run `bundle audit` / `npm audit` / `pip check` to find current issues
2. Review breaking changes list from the library
3. Create a separate branch for the upgrade
4. Tag current version before upgrading

### During Upgrade:
1. Upgrade one major dependency at a time if possible
2. Run tests after each dependency upgrade
3. Check deprecation warnings: `RUBYOPT=-W2 rails test`

### After Upgrade:
1. Review all AI-suggested changes
2. Manually test critical user flows
3. Run performance benchmarks if applicable
4. Update documentation

