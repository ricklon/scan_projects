#!/usr/bin/env python3

import os
import time
import json
from datetime import datetime
import subprocess
from pathlib import Path
import argparse
from typing import Dict, List, Optional
from collections import Counter

def get_last_modified(path: str) -> float:
    """Get the last modification time of any file in the directory."""
    latest = 0
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(file_path)
                latest = max(latest, mtime)
            except OSError:
                continue
    return latest

def format_time_ago(timestamp: float) -> str:
    """Format the time difference between now and the timestamp."""
    if timestamp == 0:
        return "Never modified"
    
    diff = time.time() - timestamp
    if diff < 60:
        return "Just now"
    elif diff < 3600:
        minutes = int(diff / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif diff < 86400:
        hours = int(diff / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    else:
        days = int(diff / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"

def is_git_repo(path: str) -> bool:
    """Check if directory is a git repository."""
    try:
        result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'],
                              cwd=path,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def get_python_version(path: str) -> Optional[str]:
    """Try to detect Python version from pyproject.toml."""
    pyproject_path = os.path.join(path, "pyproject.toml")
    if os.path.exists(pyproject_path):
        try:
            with open(pyproject_path) as f:
                for line in f:
                    if "requires-python" in line:
                        return line.split("=")[-1].strip().strip('"')
        except:
            pass
    return None

def check_project_environment(path: str) -> Dict[str, bool]:
    """Check if directory has a managed development environment."""
    # Python-related files
    pyproject_path = os.path.join(path, "pyproject.toml")
    uv_lock_path = os.path.join(path, "uv.lock")
    poetry_lock_path = os.path.join(path, "poetry.lock")
    venv_path = os.path.join(path, ".venv")
    
    # Node.js/JavaScript-related files
    package_json_path = os.path.join(path, "package.json")
    node_modules_path = os.path.join(path, "node_modules")
    package_lock_path = os.path.join(path, "package-lock.json")
    yarn_lock_path = os.path.join(path, "yarn.lock")
    pnpm_lock_path = os.path.join(path, "pnpm-lock.yaml")
    
    is_poetry = False
    node_package_info = {}
    
    # Check for Poetry in pyproject.toml
    if os.path.exists(pyproject_path):
        try:
            with open(pyproject_path) as f:
                content = f.read()
                is_poetry = "tool.poetry" in content
        except:
            pass
    
    # Get Node.js package info
    if os.path.exists(package_json_path):
        try:
            with open(package_json_path) as f:
                package_data = json.load(f)
                node_package_info = {
                    'name': package_data.get('name', ''),
                    'version': package_data.get('version', ''),
                    'type': package_data.get('type', 'commonjs'),  # 'module' for ESM
                    'has_typescript': 'typescript' in package_data.get('dependencies', {}) or 
                                    'typescript' in package_data.get('devDependencies', {})
                }
        except:
            pass

    return {
        # Python environment info
        'has_pyproject': os.path.exists(pyproject_path),
        'has_uv_lock': os.path.exists(uv_lock_path),
        'has_poetry_lock': os.path.exists(poetry_lock_path),
        'has_venv': os.path.exists(venv_path),
        'is_poetry': is_poetry,
        
        # Node.js environment info
        'has_package_json': os.path.exists(package_json_path),
        'has_node_modules': os.path.exists(node_modules_path),
        'has_package_lock': os.path.exists(package_lock_path),
        'has_yarn_lock': os.path.exists(yarn_lock_path),
        'has_pnpm_lock': os.path.exists(pnpm_lock_path),
        'node_info': node_package_info
    }

def determine_project_type(env_info: Dict) -> List[str]:
    """Determine the primary type(s) of the project."""
    types = []
    
    # Check for Python project
    if env_info['has_pyproject'] or env_info['has_venv']:
        if env_info['has_uv_lock']:
            types.append('UV Python')
        elif env_info['is_poetry']:
            types.append('Poetry Python')
        else:
            types.append('Python')
    
    # Check for Node.js project
    if env_info['has_package_json']:
        node_type = 'TypeScript' if env_info['node_info'].get('has_typescript') else 'JavaScript'
        package_manager = 'npm'
        if env_info['has_yarn_lock']:
            package_manager = 'yarn'
        elif env_info['has_pnpm_lock']:
            package_manager = 'pnpm'
        
        types.append(f"{node_type} ({package_manager})")
    
    return types if types else ['Unknown']

def scan_projects(directory: str) -> List[Dict]:
    """Scan the directory for projects and their information."""
    projects = []
    
    try:
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isdir(full_path):
                last_modified = get_last_modified(full_path)
                is_git = is_git_repo(full_path)
                env_info = check_project_environment(full_path)
                python_version = get_python_version(full_path)
                
                projects.append({
                    'name': item,
                    'path': full_path,
                    'last_modified': last_modified,
                    'last_modified_fmt': format_time_ago(last_modified),
                    'is_git': is_git,
                    'python_version': python_version,
                    'environment_info': env_info
                })
        
        # Sort projects by last modification time (most recent first)
        return sorted(projects, key=lambda x: x['last_modified'], reverse=True)
    
    except PermissionError:
        print(f"Error: Permission denied accessing {directory}")
        return []

def get_project_statistics(projects: List[Dict]) -> Dict:
    """Calculate statistics about the projects."""
    stats = {
        'total': len(projects),
        'git_repos': sum(1 for p in projects if p['is_git']),
        'python_versions': Counter(p['python_version'] for p in projects if p['python_version']),
        'uv_managed': sum(1 for p in projects if p['environment_info']['has_uv_lock']),
        'poetry_managed': sum(1 for p in projects if p['environment_info']['is_poetry']),
        'node_projects': sum(1 for p in projects if p['environment_info']['has_package_json']),
        'typescript_projects': sum(1 for p in projects if p['environment_info']['node_info'].get('has_typescript')),
        'package_managers': {
            'npm': sum(1 for p in projects if p['environment_info']['has_package_lock']),
            'yarn': sum(1 for p in projects if p['environment_info']['has_yarn_lock']),
            'pnpm': sum(1 for p in projects if p['environment_info']['has_pnpm_lock'])
        }
    }
    return stats

def print_project_statistics(stats: Dict):
    """Print statistics about the projects."""
    print("\nProject Statistics:")
    print("-" * 70)
    print(f"Total projects: {stats['total']}")
    print(f"Git repositories: {stats['git_repos']}")
    
    print("\nPython Projects:")
    print(f"  UV-managed: {stats['uv_managed']}")
    print(f"  Poetry-managed: {stats['poetry_managed']}")
    
    print("\nNode.js Projects:")
    print(f"  Total Node.js projects: {stats['node_projects']}")
    print(f"  TypeScript projects: {stats['typescript_projects']}")
    print("  Package Managers:")
    print(f"    npm: {stats['package_managers']['npm']}")
    print(f"    yarn: {stats['package_managers']['yarn']}")
    print(f"    pnpm: {stats['package_managers']['pnpm']}")
    
    if stats['python_versions']:
        print("\nPython versions used:")
        for version, count in stats['python_versions'].items():
            if version:
                print(f"  Python {version}: {count} projects")

def main() -> None:
    parser = argparse.ArgumentParser(description='Scan project directory for recent activity')
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                       help='Directory to scan (default: current directory)')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit the number of projects shown')
    parser.add_argument('--uv-only', action='store_true',
                       help='Show only UV-managed projects')
    parser.add_argument('--poetry-only', action='store_true',
                       help='Show only Poetry-managed projects')
    parser.add_argument('--node-only', action='store_true',
                       help='Show only Node.js projects')
    parser.add_argument('--typescript-only', action='store_true',
                       help='Show only TypeScript projects')
    parser.add_argument('--git-only', action='store_true',
                       help='Show only Git repositories')
    parser.add_argument('--sort', choices=['date', 'name', 'python', 'type'],
                       default='date',
                       help='Sort projects by date, name, Python version, or project type')
    
    args = parser.parse_args()
    directory = os.path.expanduser(args.directory)
    
    if not os.path.exists(directory):
        print(f"Error: Directory {directory} does not exist")
        return
    
    print(f"\nScanning directory: {directory}\n")
    projects = scan_projects(directory)
    
    # Apply filters
    if args.uv_only:
        projects = [p for p in projects if p['environment_info']['has_uv_lock']]
    if args.poetry_only:
        projects = [p for p in projects if p['environment_info']['is_poetry']]
    if args.node_only:
        projects = [p for p in projects if p['environment_info']['has_package_json']]
    if args.typescript_only:
        projects = [p for p in projects if p['environment_info']['node_info'].get('has_typescript')]
    if args.git_only:
        projects = [p for p in projects if p['is_git']]
    
    # Apply sorting
    if args.sort == 'name':
        projects.sort(key=lambda x: x['name'].lower())
    elif args.sort == 'python':
        projects.sort(key=lambda x: (x['python_version'] or '', x['name'].lower()))
    elif args.sort == 'type':
        projects.sort(key=lambda x: str(determine_project_type(x['environment_info'])))
    
    if args.limit:
        projects = projects[:args.limit]
    
    if not projects:
        print("No projects found.")
        return
    
    # Print results
    print("Recent Projects:")
    print("-" * 70)
    for project in projects:
        git_status = "[Git]" if project['is_git'] else "[No Git]"
        project_types = determine_project_type(project['environment_info'])
        type_str = f"[{', '.join(project_types)}]"
        
        env_status = []
        node_info = project['environment_info']['node_info']
        
        # Add Python-related status
        if project['environment_info']['has_pyproject']:
            env_status.append("pyproject.toml")
        if project['environment_info']['has_uv_lock']:
            env_status.append("uv.lock")
        if project['environment_info']['has_venv']:
            env_status.append(".venv")
            
        # Add Node.js-related status
        if node_info:
            if node_info.get('type') == 'module':
                env_status.append("ESM")
            if node_info.get('has_typescript'):
                env_status.append("TypeScript")
        
        env_str = f"[{', '.join(env_status)}]" if env_status else "[No Package Manager]"
        python_ver = f"[Python {project['python_version']}]" if project['python_version'] else ""
        
        print(f"{project['name']} {git_status} {type_str}")
        print(f"Environment: {env_str} {python_ver}")
        print(f"Last modified: {project['last_modified_fmt']}")
        print(f"Path: {project['path']}")
        print("-" * 70)
    
    # Print statistics
    stats = get_project_statistics(projects)
    print_project_statistics(stats)

if __name__ == "__main__":
    main()