# scan-projects

A command-line tool to scan and analyze your project directories, with special support for UV-managed Python projects and Node.js environments.

## Features

- 📂 Scans directories to find and analyze projects
- 🐍 Detects Python environments (UV and Poetry)
- 🌐 Identifies Node.js projects (including TypeScript)
- 🔍 Shows project last modified times
- 📊 Identifies Git repositories
- 🛠️ Detects project configuration files:
  - Python: pyproject.toml, uv.lock, poetry.lock, .venv
  - Node.js: package.json, package-lock.json, yarn.lock, pnpm-lock.yaml
- 🎯 Displays Python version requirements
- 📈 Provides project statistics and summaries

## Installation

Recommended installation using pipx (ideal for CLI tools):

```bash
# Install pipx if you haven't already
sudo apt install pipx
pipx ensurepath

# Install scan-projects
pipx install scan-projects
```

Or install from source:

```bash
git clone https://github.com/ricklon/scan-projects
cd scan-projects
pipx install .
```

## Usage

Basic usage:

```bash
# Scan current directory
scan-projects

# Scan specific directory
scan-projects ~/projects

# Scan parent directory
scan-projects ..
```

Advanced options:

```bash
# Filter options
scan-projects --uv-only        # Show only UV-managed projects
scan-projects --poetry-only    # Show only Poetry-managed projects
scan-projects --node-only      # Show only Node.js projects
scan-projects --typescript-only # Show only TypeScript projects
scan-projects --git-only       # Show only Git repositories

# Limit results
scan-projects --limit 5        # Show only 5 most recent projects

# Sorting options
scan-projects --sort date      # Sort by last modified (default)
scan-projects --sort name      # Sort alphabetically
scan-projects --sort python    # Sort by Python version
scan-projects --sort type      # Sort by project type
```

Example output:
```
Scanning directory: /home/user/projects

Recent Projects:
----------------------------------------------------------------------
web-app [Git] [UV Python]
Environment: [pyproject.toml, uv.lock, .venv] [Python >=3.12.3]
Last modified: 2 hours ago
Path: /home/user/projects/web-app
----------------------------------------------------------------------
node-api [Git] [TypeScript (npm)]
Environment: [package.json, TypeScript]
Last modified: 5 days ago
Path: /home/user/projects/node-api
----------------------------------------------------------------------

Project Statistics:
----------------------------------------------------------------------
Total projects: 2
Git repositories: 2

Python Projects:
  UV-managed: 1
  Poetry-managed: 0

Node.js Projects:
  Total Node.js projects: 1
  TypeScript projects: 1
  Package Managers:
    npm: 1
    yarn: 0
    pnpm: 0

Python versions used:
  Python >=3.12.3: 1 projects
```

## Project Detection

The tool detects various project types and configurations:

### Python Projects
- UV environment detection
  - pyproject.toml configuration
  - uv.lock file
  - .venv directory
- Poetry environment detection
  - poetry.lock file
  - Poetry configuration in pyproject.toml
- Python version requirements

### Node.js Projects
- Project type detection (JavaScript/TypeScript)
- Package manager detection (npm/yarn/pnpm)
- Module type (CommonJS/ESM)
- TypeScript configuration

### General Features
- Git repository detection
- Last modification tracking
- Project statistics and summaries

## Development

Setting up for development:

```bash
# Clone the repository
git clone https://github.com/ricklon/scan-projects
cd scan-projects

# Create and activate UV environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
uv pip install -e .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created by Ricklon (rick.rickanderson@gmail.com)