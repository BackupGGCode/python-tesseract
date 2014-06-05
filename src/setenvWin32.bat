rem move C:\Python27_32 C:\Python27
SET PYTHONPATH=C:\Python27
SET OLDPATH=%PATH%
SET PATH="%PYTHONPATH%;C:\Program Files (x86)\mingw-w64\i686-4.9.0-posix-dwarf-rt_v3-rev1\mingw32\bin;c:\swig;c:\cygwin64\bin"
%PYTHONPATH%\python --version
%PYTHONPATH%\python setup.py clean
%PYTHONPATH%\python setup.py build
%PYTHONPATH%\python setup.py install

rem move C:\Python27 C:\Python27_32

