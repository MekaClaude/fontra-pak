# Fontra Pak v2026.3.3.0 - Release Notes

## Build Information

**Version:** 2026.3.3.0  
**Build Date:** 2026-03-16  
**Platform:** Windows 64-bit  
**Executable:** `dist/Fontra-Pak-v2026.3.3.0/Fontra Pak.exe`  
**Size:** 53.5 MB

---

## What's New

### 🎨 New Application Icon
- **Brand new Fontra dev logo** embedded in the application
- The icon appears in:
  - Windows taskbar
  - Alt+Tab application switcher
  - File Explorer (when associated with font files)
  - Application window title bar
- Icon features a stylized "F" in Fontra pink (RGB: 255, 0, 92)

### 📦 Versioned Build Output
- Executables are now organized in versioned folders
- Format: `dist/Fontra-Pak-v{version}/`
- Multiple versions can coexist without overwriting each other
- Example: `dist/Fontra-Pak-v2026.3.3.0/Fontra Pak.exe`

### 🔧 Technical Updates
- Updated to Python 3.13.12
- PyInstaller 6.19.0
- PyQt6 for native Windows UI
- All Fontra plugins included:
  - fontra-compile
  - fontra-glyphs (partial support)
  - fontra-rcjk

---

## Supported File Formats

### Read & Write
- `.designspace` - DesignSpace documents
- `.ufo` - Unified Font Object
- `.fontra` - Fontra project format
- `.rcjk` - RoboCJK server format
- `.glyphs` / `.glyphspackage` - Glyphs format (partial)

### Read Only
- `.ttf` - TrueType fonts
- `.otf` - OpenType fonts
- `.woff` / `.woff2` - Web fonts
- `.ttx` - TTX font format

### Export
- `.ttf` / `.otf` - Compiled fonts
- All read/write formats above

---

## Installation

### No Installation Required
Fontra Pak is a standalone executable. No installation needed!

1. Download `Fontra Pak.exe`
2. Double-click to launch
3. Drop font files onto the application window

### Optional: Create Desktop Shortcut
Right-click `Fontra Pak.exe` → Send to → Desktop (create shortcut)

---

## Usage

### Opening Fonts
1. **Drag & Drop:** Drop font files directly onto the Fontra Pak window
2. **File Open:** Drop a font file onto the application icon
3. **New Font:** Click "New Font..." to create a new empty font project

### Editor Mode
- Enter text in the "Sample text" field before opening a font
- The editor will launch with your text pre-loaded

### Supported Operations
- View and edit glyph outlines
- Modify spacing and sidebearings
- Edit font metadata
- Create and edit variation axes
- Export to TTF/OTF
- Real-time preview in browser

---

## System Requirements

- **OS:** Windows 10 or Windows 11 (64-bit)
- **RAM:** 4 GB minimum, 8 GB recommended
- **Disk Space:** ~100 MB for the application
- **Browser:** Any modern browser (Chrome, Firefox, Edge)

---

## Known Issues

1. **First Launch:** May take a few seconds to initialize on first run
2. **Large Fonts:** Very large font families may take longer to load
3. **Glyphs Import:** Some complex Glyphs files may not import perfectly

---

## Reporting Issues

Found a bug or have a feature request?

- **GitHub Issues:** https://github.com/fontra/fontra-pak/issues
- **Documentation:** https://docs.fontra.xyz

---

## Changelog

### v2026.3.3.0 (2026-03-16)
- ✨ New Fontra dev logo application icon
- 📁 Versioned build output folders
- 🔨 Updated build system with PyInstaller 6.19.0
- 🐛 Various bug fixes and stability improvements

---

## Credits

**Developed by:** Just van Rossum  
**Icon Design:** Fontra Design Team  
**License:** GNU General Public License v3 (GPLv3)  
**Website:** https://fontra.xyz

---

## Legal

© Google LLC, Just van Rossum

Fontra Pak is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

---

**Built with ❤️ for the type design community**
