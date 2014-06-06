mingBinPath=r"""C:\Program Files (x86)\mingw-w64\i686-4.9.0-posix-dwarf-rt_v3-rev2\mingw32\bin"""
pythonBinPath=r"""c:\python27\bin"""
cmdStr=b"""\
move C:\Python27_32 C:\Python27
SET PYTHONPATH=C:\Python27
SET OLDPATH=%PATH%
SET PATH="%s;%s;c:\swig;c:\cygwin64\bin"
%PYTHONPATH%\python --version
%PYTHONPATH%\python setup.py clean
%PYTHONPATH%\python setup.py build
%PYTHONPATH%\python setup.py install
move C:\Python27 C:\Python27_32
"""%(pythonBinPath,pythonBinPath)

print cmdStr


