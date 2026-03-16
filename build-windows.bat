@echo off
REM Build Fontra Pak for Windows
REM This script builds the Windows executable using PyInstaller

echo ============================================
echo Fontra Pak Windows Build Script
echo ============================================
echo.

REM Check Python version
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please ensure Python 3.10+ is installed.
    exit /b 1
)

echo.
echo Installing/verifying dependencies...
pip install -r requirements.txt
pip install -r requirements-dev.txt

echo.
echo Building Fontra client bundle...
cd ..
call npm install
call npm run bundle
cd fontra-pak

echo.
echo Building Windows executable with PyInstaller...
pyinstaller FontraPak.spec --clean

if exist "dist\Fontra Pak.exe" (
    echo.
    echo ============================================
    echo Build successful!
    echo ============================================
    echo Executable: dist\Fontra Pak.exe
    echo.
    echo To create an installer, you can use Inno Setup or NSIS.
) else (
    echo.
    echo ============================================
    echo Build failed! Check the error messages above.
    echo ============================================
    exit /b 1
)
