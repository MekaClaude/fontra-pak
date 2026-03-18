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
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
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

    # Read current content
    content = version_info_path.read_text(encoding='utf-8')

    # Update numeric versions
    content = content.replace(
        "filevers=(2026, 3, 18, 17),",
        f"filevers={numeric_version},"
    )
    content = content.replace(
        "prodvers=(2026, 3, 18, 17),",
        f"prodvers={numeric_version},"
    )

    # Update string versions
    content = content.replace(
        "StringStruct(u'FileVersion', u'2026.3.18.17'),",
        f"StringStruct(u'FileVersion', u'{version}'),"
    )
    content = content.replace(
        "StringStruct(u'ProductVersion', u'2026.3.18.17')])",
        f"StringStruct(u'ProductVersion', u'{version}')])"
    )

    # Write back
    version_info_path.write_text(content, encoding='utf-8')
    print(f"Updated version-info.txt to version {version}")

def update_fontra_version(version):
    """Update src/fontra/_version.py"""
    version_py_path = Path("../src/fontra/_version.py")

    # Read current content
    content = version_py_path.read_text(encoding='utf-8')

    # Update version string
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith("__version__ = version = "):
            lines[i] = f"__version__ = version = '{version}'"
        elif line.startswith("__version_tuple__ = version_tuple = "):
            year, month, day, hour = version.split('.')
            lines[i] = f"__version_tuple__ = version_tuple = ({year}, {int(month)}, {int(day)}, {int(hour)})"

    # Write back
    version_py_path.write_text('\n'.join(lines), encoding='utf-8')
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
        f"{sys.executable} -m pip install -r requirements.txt",
        description="Installing dependencies"
    )
    run_command(
        f"{sys.executable} -m pip install -r requirements-dev.txt",
        description="Installing dev dependencies"
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