# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['EventScraperJP.py'],
    pathex=[],
    binaries=[],
    datas=[('site', 'site')],
    hiddenimports=['requests', 're', 'bs4', 'openpyxl', 'pykakasi', 'pandas', 'time', 'os', 'concurrent.futures', 'random', 'sys', 'datetime', 'openpyxl.styles', 'openpyxl.worksheet.dimensions', 'openpyxl.utils', 'openpyxl.utils.dataframe', 'flask', 'flask.json'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='EventScraperJP',
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
)
