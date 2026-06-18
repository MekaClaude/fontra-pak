#!/usr/bin/env python3
"""
Build Fontra Pak with timestamped version
Creates version based on current date/time: YYYY.MM.DD.HH
Outputs to dist/Fontra-Pak-v{version}/Fontra Pak.exe
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

def run_command(cmd, cwd=None, description=""):
    """Run a command and check for errors"""
    print(f"{description}...")
    use_shell = isinstance(cmd, str)
    result = subprocess.run(cmd, shell=use_shell, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        cmd_str = cmd if isinstance(cmd, str) else ' '.join(cmd)
        print(f"Command failed: {cmd_str}")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        sys.exit(1)
    return result

def check_python():
    """Check Python version"""
    print("Checking Python version...")
    result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: Python not found")
        sys.exit(1)
    print(result.stdout.strip())

def get_timestamp_version():
    """Get version string in format YYYY.MM.DD.HH"""
    now = datetime.now()
    return f"{now.year}.{now.month:02d}.{now.day:02d}.{now.hour:02d}"

def update_version_info(version):
    """Update version-info.txt with the new version"""
    version_info_path = Path("version-info.txt")

    # Numeric version tuple
    year, month, day, hour = version.split('.')
    numeric_version = f"({year}, {int(month)}, {int(day)}, {int(hour)})"
    version_str = f"{year}.{int(month)}.{int(day)}.{int(hour)}"

    import re

    content = version_info_path.read_text(encoding='utf-8')

    # Update numeric versions dynamically
    content = re.sub(
        r'filevers=\(\d+,\s*\d+,\s*\d+,\s*\d+\),',
        f'filevers={numeric_version},',
        content
    )
    content = re.sub(
        r'prodvers=\(\d+,\s*\d+,\s*\d+,\s*\d+\),',
        f'prodvers={numeric_version},',
        content
    )

    # Update string versions dynamically
    content = re.sub(
        r"StringStruct\(u'FileVersion',\s*u'[\d.]+'\),",
        f"StringStruct(u'FileVersion', u'{version_str}'),",
        content
    )
    content = re.sub(
        r"StringStruct\(u'ProductVersion',\s*u'[\d.]+'\)\]\)",
        f"StringStruct(u'ProductVersion', u'{version_str}')])",
        content
    )

    version_info_path.write_text(content, encoding='utf-8')
    print(f"Updated version-info.txt to version {version}")

def update_fontra_version(version):
    """Update src/fontra/_version.py"""
    version_py_path = Path("../src/fontra/_version.py")

    import re

    content = version_py_path.read_text(encoding='utf-8')

    year, month, day, hour = version.split('.')
    version_str = f"{year}.{int(month):02d}.{int(day):02d}.{int(hour):02d}"
    version_tuple = f"({int(year)}, {int(month)}, {int(day)}, {int(hour)})"

    content = re.sub(
        r"__version__ = version = '[\d.]+'",
        f"__version__ = version = '{version_str}'",
        content
    )
    content = re.sub(
        r"__version_tuple__ = version_tuple = \([\d, ]+\)",
        f"__version_tuple__ = version_tuple = {version_tuple}",
        content
    )

    version_py_path.write_text(content, encoding='utf-8')
    print(f"Updated src/fontra/_version.py to version {version}")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    result = subprocess.run([
        sys.executable, "-m", "PyInstaller", "FontraPak.spec", "--clean"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("Build failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        sys.exit(1)

    print("Build successful!")

def create_versioned_folder(version):
    """Create versioned output folder and copy executable"""
    dist_dir = Path("dist")
    exe_name = "Fontra Pak.exe"

    # Ensure dist exists
    dist_dir.mkdir(exist_ok=True)

    # Versioned folder
    versioned_dir = dist_dir / f"Fontra-Pak-v{version}"
    versioned_dir.mkdir(exist_ok=True)

    # Copy executable to versioned folder
    exe_path = dist_dir / exe_name
    if exe_path.exists():
        shutil.copy2(exe_path, versioned_dir / exe_name)
        print(f"Created {versioned_dir / exe_name}")
    else:
        print(f"Warning: {exe_path} not found!")

def main():
    print("Fontra Pak Timestamped Build")
    print("=" * 40)

    # Check Python
    check_python()

    # Get timestamp version
    version = get_timestamp_version()
    print(f"Building version: {version}")

    # Update version files
    update_version_info(version)
    update_fontra_version(version)

    # Install dependencies
    run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        description="Installing dependencies"
    )
    run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"],
        description="Installing dev dependencies"
    )
    run_command(
        [sys.executable, "-m", "pip", "install", "-e", ".."],
        description="Installing local fontra package"
    )

    # Build client bundle
    run_command(
        "npm install",
        cwd="..",
        description="Installing npm dependencies"
    )
    run_command(
        "npm run bundle",
        cwd="..",
        description="Building Fontra client bundle"
    )

    # Build executable
    build_executable()

    # Create versioned folder
    create_versioned_folder(version)

    print("\nBuild completed successfully!")
    print(f"Output: dist/Fontra-Pak-v{version}/Fontra Pak.exe")

if __name__ == "__main__":
    main()