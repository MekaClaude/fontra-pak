# Fontra Pak Windows Build

## Latest Release

**Version:** 2026.3.3.0  
**Build Date:** 2026-03-16  
**Output:** `dist/Fontra-Pak-v2026.3.3.0/Fontra Pak.exe` (53.5 MB)

---

## Build Summary

Fontra Pak is a standalone Windows application for viewing and editing font files. It bundles:
- Fontra server (Python)
- Fontra client (JavaScript/HTML)
- PyQt6 for native Windows UI
- All required dependencies

### Versioned Builds

Starting with v2026.3.3.0, builds are organized in versioned folders:

```
dist/
├── Fontra Pak.exe              # Latest build (overwritten on each build)
└── Fontra-Pak-v2026.3.3.0/     # Versioned folder (preserved)
    └── Fontra Pak.exe
```

This allows:
- Multiple versions to coexist
- Easy rollback to previous versions
- Clear version tracking for releases

## What Was Done

### 1. Icon Update
- Created new Fontra icon from SVG source file
- Converted SVG to Windows ICO format with multiple sizes (16x16 to 512x512)
- Icon features the new stylized "F" logo in pink (RGB: 255, 0, 92)

**Files Modified:**
- `icon/fontra-icon-source.svg` - Source SVG file
- `icon/FontraIcon.ico` - Windows icon file (generated)

### 2. Build Process
The Windows executable was built using PyInstaller with the following steps:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. **Build Fontra client bundle:**
   ```bash
   cd ..
   npm install
   npm run bundle
   ```

3. **Build Windows executable:**
   ```bash
   pyinstaller FontraPak.spec --clean
   ```

### 3. Icon Conversion Script
Created `scripts/convert-icons-simple.py` for converting the SVG icon to ICO format.

**Usage:**
```bash
python scripts/convert-icons-simple.py
```

This creates `icon/FontraIcon.ico` with all required sizes for Windows.

## Build Script

A batch file `build-windows.bat` has been created to automate the entire build process:

```batch
build-windows.bat
```

This script:
1. Verifies Python installation
2. Installs dependencies
3. Builds the Fontra client bundle
4. Runs PyInstaller to create the Windows executable

## Output

**Executable:** `dist/Fontra Pak.exe`
- Size: 53.5 MB
- Includes all Python dependencies
- Bundled Fontra client (JavaScript/HTML)
- PyQt6 for native Windows UI
- New Fontra icon embedded

## Testing the Build

After building, you can test the executable by:

1. Double-clicking `dist/Fontra Pak.exe`
2. Dropping a font file (.designspace, .ufo, .ttf, .otf, .fontra) onto the application
3. The font should open in your default browser

## Creating an Installer (Optional)

To create a proper Windows installer, you can use:

### Inno Setup
1. Download Inno Setup from https://jrsoftware.org/isdl.php
2. Create a `.iss` script:
   ```iss
   [Setup]
   AppName=Fontra Pak
   AppVersion=1.0.0
   DefaultDirName={autopf}\Fontra Pak
   OutputDir=installer-output
   [Files]
   Source: "dist\Fontra Pak.exe"; DestDir: "{app}"
   [Icons]
   Name: "{group}\Fontra Pak"; Filename: "{app}\Fontra Pak.exe"
   ```
3. Compile with Inno Setup Compiler

### NSIS
Alternatively, use NSIS for more advanced installer features.

## Notes

- The build includes the new Fontra icon which will appear in:
  - Windows taskbar
  - Alt+Tab switcher
  - File Explorer (when associated with font files)
  - Application window title bar

- The icon ICO file contains multiple sizes for optimal display at different DPI settings

## Troubleshooting

### Build fails with "Module not found"
Ensure all dependencies are installed:
```bash
pip install -r requirements-dev.txt
```

### Icon not showing
Verify the icon file exists and is valid:
```bash
python scripts/convert-icons-simple.py
```

### Executable too large
This is normal - PyInstaller bundles Python and all dependencies. The size can be reduced slightly with UPX compression (already enabled in the spec file).

## Next Steps

1. **Code Signing** (recommended for distribution):
   - Obtain a code signing certificate
   - Sign the executable: `signtool sign /f certificate.pfx /t http://timestamp.digicert.com "dist\Fontra Pak.exe"`

2. **Create Installer** (see above)

3. **Test on clean Windows installation** to ensure all dependencies are bundled correctly

4. **Release to GitHub**:
   - Create a new release on GitHub
   - Upload the executable or installer
   - Include release notes

---

**Build completed successfully! ✅**
