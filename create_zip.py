#!/usr/bin/env python3
import zipfile
import os
import shutil

def create_project_zip():
    """Create a zip file of the VLSI Hero project for GitHub upload."""
    
    # Files and directories to include
    files_to_include = [
        'app.py',
        'main.py', 
        'models.py',
        'README.md',
        'LICENSE',
        'CONTRIBUTING.md',
        'DEPLOYMENT.md',
        'CHANGELOG.md',
        'setup.py',
        'Procfile',
        'runtime.txt',
        'Dockerfile',
        'docker-compose.yml',
        'package.json',
        'package-lock.json',
        'pyproject.toml',
        'tailwind.config.js',
        'index.html'
    ]
    
    directories_to_include = [
        'pages',
        'js',
        'css',
        'assets'
    ]
    
    # Create .gitignore content
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Flask
instance/
.webassets-cache

# Environment variables
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Database
*.db
*.sqlite3

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.yarn-integrity

# CSS Build
css/output/
*.css.map

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp

# Replit specific
.replit
replit.nix
.upm/
uv.lock
.cache/
.pythonlibs/
.local/
"""
    
    # Create zip file
    with zipfile.ZipFile('vlsi-hero-project.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add individual files
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file, file)
                print(f"Added: {file}")
        
        # Add directories
        for directory in directories_to_include:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        archive_name = file_path
                        zipf.write(file_path, archive_name)
                        print(f"Added: {archive_name}")
        
        # Add .gitignore
        zipf.writestr('.gitignore', gitignore_content)
        print("Added: .gitignore")
    
    print(f"\nZip file created: vlsi-hero-project.zip")
    print(f"Size: {os.path.getsize('vlsi-hero-project.zip')} bytes")

if __name__ == "__main__":
    create_project_zip()