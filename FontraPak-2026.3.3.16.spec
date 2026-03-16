# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Fontra Pak version 2026.3.3.16

block_cipher = None

a = Analysis(
    ['FontraPakMain.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../src/fontra', 'fontra'),
        ('../src-js', 'src-js'),
        ('icon/FontraIcon.ico', 'icon'),
    ],
    hiddenimports=[
        'aiohttp',
        'cattrs',
        'fontTools',
        'fontTools.misc',
        'fontTools.pens',
        'fontTools.pens.basePen',
        'fontTools.pens.pointPen',
        'fontTools.ttLib',
        'fontTools.ufoLib',
        'watchfiles',
        'yaml',
        'ufomerge',
        'pathops',
        'PIL',
        'ufo2ft',
        'psutil',
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Fontra Pak 2026.3.3.16',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon/FontraIcon.ico',
)
