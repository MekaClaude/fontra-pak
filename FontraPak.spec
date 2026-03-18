# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for Fontra Pak.

This spec file builds a standalone executable for the Fontra Pak application,
a browser-based font editor bundled with PyInstaller.

Platform support:
- Windows: Produces Fontra Pak.exe with version info
- macOS: Produces Fontra Pak.app bundle with proper codesigning support
- Linux: Produces fontrapak executable
"""

import glob
import os
import sys

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Compute absolute paths based on spec file location
spec_dir = SPECPATH
src_dir = os.path.join(spec_dir, "..", "src")

# Collect all fontra submodules dynamically
fontra_hiddenimports = collect_submodules("fontra")

# Collect external fontra plugins if available
external_plugins = []
for plugin_name in ["fontra_compile", "fontra_glyphs", "fontra_rcjk"]:
    try:
        external_plugins.extend(collect_submodules(plugin_name))
    except Exception:
        pass  # Plugin not installed, skip

# Explicitly list all backend modules so they are never tree-shaken
explicit_backends = [
    "fontra.backends.designspace",
    "fontra.backends.opentype",
    "fontra.backends.fontra",
    "fontra.backends.workflow",
    "fontra.backends.copy",
    "fontra.backends.populate",
    "fontra.filesystem.projectmanager",
    "fontra.workflow.workflow",
    "fontra.workflow.command",
]

hiddenimports = fontra_hiddenimports + external_plugins + explicit_backends

# -----------------------------------------------------------------------
# Collect dist-info for fontra so importlib.metadata.entry_points() works
# at runtime inside the frozen bundle. Without this, the backend registry
# is empty and every file type raises UnknownFileType.
# -----------------------------------------------------------------------
fontra_distinfo_datas = []
try:
    from importlib.metadata import packages_distributions, Distribution
    dist = Distribution.from_name("fontra")
    di_path = str(dist._path)  # path to the dist-info directory
    fontra_distinfo_datas.append((di_path, os.path.basename(di_path)))
except Exception as e:
    print(f"WARNING: Could not find fontra dist-info: {e}")
    # Fallback: glob for it
    import glob
    for sp in sys.path:
        pattern = os.path.join(sp, "fontra-*.dist-info")
        for di_path in glob.glob(pattern):
            fontra_distinfo_datas.append((di_path, os.path.basename(di_path)))
            break

block_cipher = None

a = Analysis(
    ["FontraPakMain.py"],
    pathex=[src_dir],
    binaries=[],
    datas=[
        ("../src/fontra", "fontra"),
        ("../.skills-data-prompt/fontra-dev-logo/fontra-icon.ico", "icon"),
    ] + fontra_distinfo_datas,
    hiddenimports=hiddenimports + ["fontra_compile"],
    hookspath=["."],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Test frameworks
        "pytest",
        "pyunittest",
        "nose",
        "unittest",
        # Development tools
        "sphinx",
        "docutils",
        "jinja2",
        "markupsafe",
        # Heavy scientific packages not needed for font editing
        "matplotlib",
        "numpy",
        "scipy",
        "pandas",
        # ML/AI packages
        "tensorflow",
        "torch",
        "sklearn",
        # Other GUI frameworks
        "tkinter",
        "wx",
        "gtk",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# UPX exclude list - Qt libraries can be problematic with UPX
upx_exclude = [
    "PyQt6",
    "PyQt6.QtCore",
    "PyQt6.QtGui",
    "PyQt6.QtWidgets",
    "Qt6",
    "libpng16",
    "libjpeg",
]

if sys.platform == "darwin":
    # macOS: Build universal2 binary for Intel and Apple Silicon
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name="Fontra Pak",
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=upx_exclude,
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch="universal2",
        codesign_identity=None,
        entitlements_file=None,
        icon="icon/FontraIcon.icns",
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=upx_exclude,
        name="Fontra Pak",
    )
    app = BUNDLE(
        coll,
        name="Fontra Pak.app",
        icon="icon/FontraIcon.icns",
        bundle_identifier="xyz.fontra.fontra-pak",
        info_plist={
            "CFBundleDocumentTypes": [
                {
                    "CFBundleTypeExtensions": [
                        "ttf",
                        "otf",
                        "woff",
                        "woff2",
                        "ttx",
                        "designspace",
                        "ufo",
                        "glyphs",
                        "glyphspackage",
                        "fontra",
                        "rcjk",
                    ],
                    "CFBundleTypeRole": "Editor",
                },
            ],
        },
    )
elif sys.platform == "win32":
    # Windows: Build with version info
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name="Fontra Pak",
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=upx_exclude,
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon="../.skills-data-prompt/fontra-dev-logo/fontra-icon.ico",
        version="version-info.txt",
    )
else:
    # Linux and other platforms
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name="fontrapak",
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=upx_exclude,
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon="icon/FontraIcon.ico",
    )
