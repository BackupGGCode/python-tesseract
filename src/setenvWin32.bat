SET PYTHONPATH=C:\Python27_32
SET CROSSCOMPILERPATH="C:\Program Files (x86)\mingw-w64\i686-4.9.0-posix-dwarf-rt_v3-rev1\mingw32\bin"
SET OLDPATH=%PATH%
SET TEMPPATH="%PYTHONPATH%;%CROSSCOMPILERPATH%;c:\swig;c:\cygwin64\bin"
for /f "skip=2 tokens=3*" %a in ('reg query HKCU\Environment /v PATH') do @if [%b]==[] ( @setx PATH "@TEMPPATH;%~a" ) else ( @setx PATH "@TEMPPATH;%~a %~b" )
python --version
#%PYTHONPATH%\python setup.py clean
#%PYTHONPATH%\python setup.py build

