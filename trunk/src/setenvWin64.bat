SET PYTHONPATH=C:\Python27_64
SET OLDPATH=%PATH%
SET PATH="%PYTHONPATH%;C:\Program Files\mingw-w64\x86_64-4.9.0-posix-seh-rt_v3-rev1\mingw64\bin;c:\swig;c:\cygwin64\bin"
%PYTHONPATH%\python --version
%PYTHONPATH%\python setup.py clean
%PYTHONPATH%\python setup.py build
