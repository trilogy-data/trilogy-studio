# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import trilogy_public_models
import sys
import preql_nlp
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
            if f.suffix == '.preql':
                subroot = Path('trilogy_public_models') / path
                inclusion_files.append(( str(f), str(subroot)))
    return inclusion_files

def get_preql_nlp_template_files():
    root = sys.modules.get(f'preql_nlp')
    root = Path(root.__file__).parent

    inclusion_files = []
    for f in (root / 'prompts').iterdir():
        if f.suffix == '.jinja2':
            subroot = Path('preql_nlp')  / 'prompts' / f.name
            inclusion_files.append(( str(f), str(subroot)))
    return inclusion_files



datas = get_trilogy_data_files() + get_preql_nlp_template_files()


binaries = []
hiddenimports = []
tmp_ret = collect_all('uvicorn')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('duckdb')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('duckdb-engine')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('sqlalchemy-bigquery')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('preql_nlp')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('langchain_community')
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
    name='trilogy-studio-engine',
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
