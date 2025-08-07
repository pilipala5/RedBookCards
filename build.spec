# -*- mode: python ; coding: utf-8 -*-
# ============================================
# build.spec - PyInstaller 打包配置文件
# ============================================

import sys
from pathlib import Path

# 获取项目根目录
ROOT_DIR = Path.cwd()

# 分析配置
a = Analysis(
    ['main.py'],  # 主入口文件
    pathex=[str(ROOT_DIR)],  # 搜索路径
    binaries=[],  # 二进制文件
    datas=[
        # 包含资源文件
        ('resources/icons/*.ico', 'resources/icons'),
        ('resources/icons/*.png', 'resources/icons'),
    ],
    hiddenimports=[
        # PySide6 相关
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'PySide6.QtWebEngineWidgets',
        'PySide6.QtWebEngineCore',
        'PySide6.QtPrintSupport',
        
        # Markdown 扩展
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.nl2br',
        'markdown.extensions.attr_list',
        'markdown.extensions.def_list',
        'markdown.extensions.footnotes',
        'markdown.extensions.toc',
        'markdown.extensions.sane_lists',
        'markdown.extensions.smarty',
        
        # 其他依赖
        'beautifulsoup4',
        'bs4',
        'colorsys',
        'uuid',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的模块
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',  # 运行时不需要PIL
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# 创建PYZ文件
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None
)

# EXE配置
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='XiaohongshuEditor',  # 可执行文件名
    debug=False,  # 是否开启调试
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 使用UPX压缩
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False=窗口程序，True=控制台程序
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    
    # Windows 特定配置
    version='version_info.txt',  # 版本信息文件
    icon='resources/icons/app.ico',  # 应用图标
    
    # 额外的Windows资源
    uac_admin=False,  # 不需要管理员权限
    uac_uiaccess=False,
)

# 如果需要打包成单个文件夹（推荐用于首次测试）
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='XiaohongshuEditor'
# )