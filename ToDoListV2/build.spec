# -*- mode: python -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['/home/ehsan/python_projects/ToDoList/ToDoListV2'],
             binaries=[],
             datas=[('exceptions.py', '.'), 
                   ('tasks.txt', '.'),
                   ('completed_tasks.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)