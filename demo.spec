# -*- mode: python -*-

block_cipher = None


a = Analysis(['demo.py'],
             pathex=['F:\\net\\facedemo2'],
             binaries=[],
             datas=[],
             hiddenimports=["pywt","pywt._extensions._cwt"],
             hookspath=["F:\\net\\facedemo2\\hooks"],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='demo',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
