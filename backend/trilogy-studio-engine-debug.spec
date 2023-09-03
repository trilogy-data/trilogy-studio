# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import trilogy_public_models
import sys
from pathlib import Path

def get_trilogy_data_files():
    root = sys.modules.get(f'trilogy_public_models')
    root = Path(root.__file__)

    inclusion_files = []
    for key, value in trilogy_public_models.models.items():
    
        path = key.replace('.' , '/')

        check = root.parent / path

        files = check.iterdir()
        for f in files:
            if f.suffix in  ('.preql', '.py'):
                subroot = Path('trilogy_public_models') / path
                inclusion_files.append(( str(f), str(subroot)))
    return inclusion_files


datas = get_trilogy_data_files()
binaries = []
hiddenimports = []
tmp_ret = collect_all('uvicorn')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('duckdb')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('duckdb-engine')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['extra-hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=True,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='trilogy-studio-engine-debug',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='trilogy-studio-engine-debug',
)
