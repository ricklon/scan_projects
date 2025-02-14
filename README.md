# scan-projects

A command-line tool to scan and analyze your project directories, with special support for UV-managed Python projects.

## Features

- 📂 Scans directories to find and analyze projects
- 🐍 Detects Python environments and UV configuration
- 🔍 Shows project last modified times
- 📊 Identifies Git repositories
- 🛠️ Detects UV-specific files (pyproject.toml, uv.lock, .venv)
- 🎯 Displays Python version requirements

## Installation

Install using UV:

```bash
uv pip install scan-projects
```

Or install from source:

```bash
git clone https://github.com/ricklon/scan-projects
cd scan-projects
uv pip install -e .
```

## Usage

Basic usage:

```bash
# Scan current directory
scan-projects

# Scan specific directory
scan-projects ~/projects

# Limit number of projects shown
scan-projects --limit 5
```

Example output:
```
Recent Projects:
----------------------------------------------------------------------
web-app [Git] [pyproject.toml, uv.lock, .venv] [Python >=3.12.3]
Last modified: 2 hours ago
Path: /home/user/projects/web-app
----------------------------------------------------------------------
legacy-project [Git] [No UV]
Last modified: 5 days ago
Path: /home/user/projects/legacy-project
----------------------------------------------------------------------
```

## Project Detection

The tool detects various aspects of your projects:

- UV Environment:
  - Presence of pyproject.toml
  - Presence of uv.lock
  - Presence of .venv directory
- Git status
- Python version requirements (from pyproject.toml)
- Last modification time

## Development

Setting up for development:

```bash
# Clone the repository
git clone https://github.com/ricklon/scan-projects
cd scan-projects

# Create and activate UV environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode
uv pip install -e .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created by Ricklon (rick.rickanderson@gmail.com)