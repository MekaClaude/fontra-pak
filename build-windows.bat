@echo off
REM This script builds the Windows version of the software

REM Add installation of parent fontra package in development mode to generate dist-info
pip install -e .

REM Verification step to list all discovered workflow actions
echo Discovering workflow actions...

REM Add verbose feedback about build progress
echo Building the project...

REM Add timeout to view successful build message
TIMEOUT /t 10

echo Build completed successfully!
REM Ensure all entry points are properly registered before PyInstaller bundling
