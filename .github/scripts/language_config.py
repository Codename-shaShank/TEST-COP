"""
Configuration for multi-language dependency upgrade detection and fixing.
Maps languages to their specific settings, test commands, and breaking change patterns.
"""

LANGUAGE_CONFIG = {
    'ruby': {
        'name': 'Ruby/Rails',
        'extensions': ['.rb'],
        'lockfile': 'Gemfile.lock',
        'manifest': 'Gemfile',
        'dependency_manager': 'bundler',
        'setup_action': 'ruby/setup-ruby',
        'install_command': [
            'bundle config set --local deployment false',
            'bundle config set --local path vendor/bundle',
            'bundle install --jobs 4'
        ],
        'test_commands': [
            'bin/rails test:prepare || bin/rake test:prepare',
            'bin/rails test'
        ],
        'test_framework': 'rails-test',
        'major_version_indicators': {  # How to detect major version upgrades
            'rails': 7,
            'sinatra': 2,
            'sinatra': 3,
        },
        'breaking_changes': {
            'rails': {
                '8': '''
- Remove hash rocket syntax from method calls: `render :json => data` → `render json: data`
- Check Rack 3.0 compatibility (cookies, query parsing)
- Active Record `find(nil)` behavior changed (raises error instead of returning nil)
- `has_secure_password` no longer accepts password argument
                '''
            }
        },
        'upgrade_resources': [
            'https://guides.rubyonrails.org/',
            'https://github.com/rails/rails/releases',
        ]
    },
    
    'javascript': {
        'name': 'JavaScript/Node.js',
        'extensions': ['.js', '.jsx', '.mjs'],
        'lockfile': 'package-lock.json',  # Could be yarn.lock or pnpm-lock.yaml
        'manifest': 'package.json',
        'dependency_manager': 'npm',  # Could be yarn or pnpm
        'setup_action': 'actions/setup-node',
        'install_command': [
            'npm install',  # Or yarn/pnpm depending on lock file
        ],
        'test_commands': [
            'npm test',
            'npm run test:unit',
        ],
        'test_framework': 'jest|mocha|vitest',
        'major_version_indicators': {
            'express': 5,
            'webpack': 5,
            'next': 13,
            'react': 18,
        },
        'breaking_changes': {
            'express': {
                '5': '''
- Remove express.static middleware auto-import: `const bodyParser = require('body-parser')`
- Change to: `app.use(express.json())`
                '''
            },
            'webpack': {
                '5': '''
- Entry points must be explicit objects, not implicit
- Asset modules replace file-loader, url-loader, raw-loader
                '''
            }
        },
        'upgrade_resources': [
            'https://nodejs.org/en/docs/',
            'https://www.npmjs.com/',
            'https://webpack.js.org/migrate/',
        ]
    },
    
    'typescript': {
        'name': 'TypeScript',
        'extensions': ['.ts', '.tsx'],
        'lockfile': 'package-lock.json',
        'manifest': 'package.json',
        'dependency_manager': 'npm',
        'setup_action': 'actions/setup-node',
        'install_command': [
            'npm install',
        ],
        'test_commands': [
            'npm test',
            'tsc --noEmit',  # Type check
        ],
        'test_framework': 'jest|vitest',
        'major_version_indicators': {
            'typescript': 5,
        },
        'breaking_changes': {},
        'upgrade_resources': [
            'https://www.typescriptlang.org/docs/',
            'https://www.typescriptlang.org/docs/handbook/release-notes/',
        ]
    },
    
    'python': {
        'name': 'Python',
        'extensions': ['.py'],
        'lockfile': 'requirements.txt',  # Could be poetry.lock or Pipfile.lock
        'manifest': 'requirements.txt',
        'dependency_manager': 'pip',  # Could be poetry or pipenv
        'setup_action': 'actions/setup-python',
        'python_version': '3.11',
        'install_command': [
            'python -m pip install --upgrade pip',
            'pip install -r requirements.txt',  # Or poetry/pipenv
        ],
        'test_commands': [
            'python -m pytest',
            'python -m pytest tests/',
            'python -m unittest discover',
        ],
        'test_framework': 'pytest|unittest',
        'major_version_indicators': {
            'django': 4,
            'flask': 2,
            'python': 4,  # Python major version
        },
        'breaking_changes': {
            'django': {
                '4': '''
- Remove django.conf.urls.url(): use django.urls.path() or re_path() instead
- QuerySet.extra() removed: use annotate() or raw SQL
- default_auto_field default changed to BigAutoField
                '''
            },
            'flask': {
                '2': '''
- Python 3.7+ required
- Changed imports: Flask.json → Flask.json
- app.json() → app.json interface changed
                '''
            }
        },
        'upgrade_resources': [
            'https://docs.djangoproject.com/en/stable/releases/',
            'https://flask.palletsprojects.com/en/latest/changes/',
            'https://docs.python.org/3/whatsnew/',
        ]
    },
    
    'java': {
        'name': 'Java',
        'extensions': ['.java'],
        'lockfile': 'pom.xml',  # Could be build.gradle
        'manifest': 'pom.xml',
        'dependency_manager': 'maven',  # Could be gradle
        'setup_action': 'actions/setup-java',
        'java_version': '17',
        'install_command': [
            'mvn clean install',  # Or ./gradlew build
        ],
        'test_commands': [
            'mvn test',
            './gradlew test',
        ],
        'test_framework': 'junit|testng',
        'major_version_indicators': {
            'java': 11,
            'spring-boot': 3,
        },
        'breaking_changes': {
            'spring-boot': {
                '3': '''
- Java 17+ required
- javax.* imports → jakarta.* imports
- Remove spring-boot-starter-validation dependency (included in web starter)
                '''
            }
        },
        'upgrade_resources': [
            'https://www.oracle.com/java/technologies/',
            'https://spring.io/projects/spring-framework',
            'https://mvnrepository.com/',
        ]
    },
    
    'php': {
        'name': 'PHP',
        'extensions': ['.php'],
        'lockfile': 'composer.lock',
        'manifest': 'composer.json',
        'dependency_manager': 'composer',
        'setup_action': 'shivammathur/setup-php',
        'php_version': '8.2',
        'install_command': [
            'composer install',
        ],
        'test_commands': [
            'php artisan test',  # Laravel
            './vendor/bin/phpunit',  # PHPUnit
        ],
        'test_framework': 'phpunit|pest',
        'major_version_indicators': {
            'php': 8,
            'laravel': 10,
        },
        'breaking_changes': {
            'laravel': {
                '9': '''
- Symfony component version bump to 6.0+
- Route model binding: implicit vs explicit casting
- Pagination defaults changed
                '''
            }
        },
        'upgrade_resources': [
            'https://www.php.net/releases/',
            'https://laravel.com/docs/releases',
            'https://packagist.org/',
        ]
    },
    
    'dotnet': {
        'name': '.NET/C#',
        'extensions': ['.cs'],
        'lockfile': '*.csproj',
        'manifest': '*.csproj',
        'dependency_manager': 'nuget',
        'setup_action': 'actions/setup-dotnet',
        'dotnet_version': '8.0',
        'install_command': [
            'dotnet restore',
        ],
        'test_commands': [
            'dotnet test',
        ],
        'test_framework': 'xunit|nunit|mstest',
        'major_version_indicators': {
            'dotnet': 8,
        },
        'breaking_changes': {},
        'upgrade_resources': [
            'https://docs.microsoft.com/en-us/dotnet/',
            'https://www.nuget.org/',
            'https://github.com/dotnet/runtime/releases',
        ]
    }
}

# Common development dependencies that often cause issues
PROBLEMATIC_DEPENDENCIES = {
    'ruby': ['devise', 'pundit', 'cancan', 'carrierwave', 'paperclip'],
    'javascript': ['express', 'lodash', 'moment', 'webpack', 'babel'],
    'python': ['django', 'flask', 'sqlalchemy', 'numpy', 'pandas'],
    'java': ['spring-boot', 'hibernate', 'log4j', 'junit'],
    'php': ['laravel', 'symfony', 'doctrine', 'phpunit'],
    'dotnet': ['entity-framework', 'aspnetcore', 'mvc'],
}

# Common error patterns to look for
ERROR_PATTERNS = {
    'ruby': {
        'missing_method': r"undefined method `(\w+)' for",
        'wrong_number_args': r"wrong number of arguments \(given (\d+), expected (\d+)\)",
        'const_error': r"uninitialized constant (\S+)",
        'load_error': r"cannot load such file",
    },
    'javascript': {
        'undefined': r"(\w+) is not defined",
        'import_error': r"Cannot find module '([^']+)'",
        'syntax_error': r"SyntaxError: (.*)",
        'type_error': r"TypeError: (.*)",
    },
    'python': {
        'import_error': r"ModuleNotFoundError: No module named '(\w+)'",
        'attribute_error': r"AttributeError: (.*)",
        'type_error': r"TypeError: (.*)",
        'deprecation': r"DeprecationWarning: (.*)",
    },
    'java': {
        'class_not_found': r"error: cannot find symbol",
        'import_error': r"error: package (.*) does not exist",
        'method_error': r"error: cannot find symbol.*method",
    }
}

def get_language_config(language):
    """Get configuration for a specific language"""
    return LANGUAGE_CONFIG.get(language, {})

def get_test_command(language, config=None):
    """Get the appropriate test command for a language"""
    if config is None:
        config = get_language_config(language)
    
    return config.get('test_commands', [''])[0] or ''

def get_install_command(language, config=None):
    """Get the appropriate install command for a language"""
    if config is None:
        config = get_language_config(language)
    
    return config.get('install_command', [''])[0] or ''

def get_breaking_changes(language, package, major_version):
    """Get breaking changes description for a specific package upgrade"""
    config = get_language_config(language)
    breaking = config.get('breaking_changes', {})
    
    if package in breaking:
        return breaking[package].get(str(major_version), 'No known breaking changes')
    
    return None

