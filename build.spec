# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(SPEC))

# 收集transformers相关的数据文件
transformers_datas = collect_data_files('transformers')
torch_datas = collect_data_files('torch')
tokenizers_datas = collect_data_files('tokenizers')

# 收集项目数据文件
datas = [
    (os.path.join(project_root, 'ui'), 'ui'),
    (os.path.join(project_root, 'models'), 'models'),
]

# 添加第三方库的数据文件
datas.extend(transformers_datas)
datas.extend(torch_datas)
datas.extend(tokenizers_datas)

# 收集隐藏导入
hiddenimports = [
    'transformers',
    'torch',
    'tokenizers',
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'sentencepiece',
    'safetensors',
    'huggingface_hub',
    'requests',
    'tqdm',
    'numpy',
    'regex',
    'packaging',
    'filelock',
    'typing_extensions',
]

# 收集transformers的所有子模块
hiddenimports.extend(collect_submodules('transformers'))
hiddenimports.extend(collect_submodules('torch'))
hiddenimports.extend(collect_submodules('tokenizers'))

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'notebook',
        'IPython',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='本地翻译器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 设置为False以隐藏控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_root, 'ui', 'logo.ico') if os.path.exists(os.path.join(project_root, 'ui', 'logo.ico')) else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='本地翻译器',
)
