# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_submodules

# Détection automatique du chemin courant
base_path = os.path.abspath(".")

hiddenimports = collect_submodules('PyQt5')

block_cipher = None

a = Analysis(
    ['wrapper_main.py'],
    pathex=[base_path],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('services', 'services'),
        ('modules', 'modules'),
        ('ui', 'ui'),
        ('config.py', '.'),
        (os.path.abspath(os.path.join(base_path, '..', 'GESTION_BUDGET_UFR_SET')), 'GESTION_BUDGET_UFR_SET'),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GestionBudgetUFR',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # True si tu veux voir les logs dans un terminal
    icon='ufr.ico' if os.path.exists('ufr.ico') else None,
)

