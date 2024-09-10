# pyinstaller drug_management_system.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  # 主程序文件
    pathex=['.'],  # 搜索路径，'.'表示当前目录
    binaries=[],  # 这里可以加入额外的二进制文件
    datas=[  # 打包的数据文件
        ('inventory.db', '.'),  # 将inventory.db打包到根目录下
        ('material.db', '.'),  # 将materials.db打包到根目录下
        ('suppliers.db', '.'),  # 将suppliers.db打包到根目录下
    ],
    hiddenimports=[],  # 隐藏导入的模块列表，如果PyInstaller无法检测到，可以在这里手动添加
    hookspath=[],  # 钩子路径
    hooksconfig={},
    runtime_hooks=[],  # 运行时钩子
    excludes=[],  # 排除的模块
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,  # 加密配置
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DrugManagementSystem',  # 可执行文件的名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 使用UPX压缩可执行文件
    console=False  # 设置为True则会显示控制台窗口
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DrugManagementSystem'
)
