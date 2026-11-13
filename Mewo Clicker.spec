# -*- mode: python ; coding: utf-8 -*-
import sys


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('Assets', 'Assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

if sys.platform == 'darwin':
    # .app bundles must be onedir; onefile windowed is an error in PyInstaller 7.
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='Mewo Clicker',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
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
        a.datas,
        strip=False,
        upx=False,
        upx_exclude=[],
        name='Mewo Clicker',
    )
    app = BUNDLE(
        coll,
        name='Mewo Clicker.app',
        icon=None,
        version='1.0.1',
        bundle_identifier='mewo.arnav.mewoclicker',
        info_plist={
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.13',
            'LSApplicationCategoryType': 'public.app-category.games',
        },
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name='Mewo Clicker',
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
