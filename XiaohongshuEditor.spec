# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('E:\\wayForward\\projects\\RedBookCards\\resources', 'resources'), ('E:\\wayForward\\projects\\RedBookCards\\src', 'src')],
    hiddenimports=['PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets', 'PySide6.QtWebEngineCore', 'PySide6.QtWebEngineWidgets', 'markdown', 'markdown.extensions', 'markdown.extensions.fenced_code', 'markdown.extensions.tables', 'markdown.extensions.nl2br', 'markdown.extensions.attr_list', 'markdown.extensions.def_list', 'markdown.extensions.footnotes', 'markdown.extensions.toc', 'markdown.extensions.sane_lists', 'markdown.extensions.smarty', 'bs4'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy', 'test', 'tests'],
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
    name='XiaohongshuEditor',
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
    version='E:\\wayForward\\projects\\RedBookCards\\version_info.txt',
    icon=['E:\\wayForward\\projects\\RedBookCards\\resources\\icons\\app.ico'],
)
