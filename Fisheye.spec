# -*- mode: python -*-

block_cipher = None

a = Analysis(['Fisheye_SFR.py'],
             pathex=['/usr/local/google/home/fanchang/Clifford/example'],
             binaries=None,
             datas=[('/usr/local/google/home/fanchang/Clifford/clifford/exe/clifford.gif', 'clifford/exe'),
             ('/usr/local/lib/python2.7/dist-packages/GTAL/GTAL.ctf','GTAL'),
             ('/usr/local/google/home/fanchang/Clifford/clifford/output/server_info.json','clifford/output')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Fisheye_SFR',
          debug=False,
          strip=False,
          upx=True,
          console=False )
