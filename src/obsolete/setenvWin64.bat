SET PYTHONPATH=C:\Python27_64
SET OLDPATH=%PATH%
SET PATH=%PYTHONPATH%;"C:\Program Files\mingw-w64\x86_64-4.9.0-posix-seh-rt_v3-rev1\mingw64\bin";"C:\Program Files (x86)\mingw-w64\i686-4.9.0-posix-dwarf-rt_v3-rev1\mingw32\i686-w64-mingw32\bin";c:\swig
%PYTHONPATH%\python --version
%PYTHONPATH%\python setup.py clean
%PYTHONPATH%\python setup.py build
