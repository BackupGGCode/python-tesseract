#!/usr/bin/env python
"""
setup.py file for SWIG
written by FreeToGo@gmail.com
"""
from distutils.core import setup, Extension, Command
import sys,os,platform
osname=platform.uname()[0]
if osname=='Darwin':
	prefix="/opt/local"
else:
	prefix=sys.prefix
incl=os.path.join(prefix,"include")
incls = ['/usr/include', '/usr/local/include']
print "include path=%s"%incl
version_number=os.getcwd().split("-")[-1]
print "Current Version : %s"%version_number


class CleanCommand(Command):
    description = "custom clean command that forcefully removes dist/build directories"
    user_options = []
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system('rm -rf ./build ./dist')
        

def inclpath(mlib):
    for pref in incls:
        path_to_incl = os.path.join(pref, mlib)
        if os.path.exists(path_to_incl):
            return path_to_incl
    assert False, 'Include directory %s was not found' % mlib
	
tesseract_module = Extension('_tesseract',
									sources=['tesseract.i','' 'main_dummy.cpp','fmemopen.c'],
									#extra_compile_args=["-DEBUG -O1 -pg "],
									swig_opts=["-c++", "-I"+inclpath('tesseract'),
													"-I"+incl,
													"-I"+inclpath('leptonica')],
									include_dirs=['.',inclpath('tesseract'),
													incl,
													inclpath('leptonica')],
									libraries=['stdc++','tesseract','lept','opencv_core'],
								
									)
									
setup (name = 'python-tesseract',
       version = version_number,
       author      = "FreeToGo Nowhere",
       description = """${python:Provides} Wrapper for Python-${python:Versions} """,
       ext_modules = [tesseract_module],
       py_modules = ["tesseract"],
       cmdclass={
        'clean': CleanCommand
        }
  #     data_files=[('.',['test.py','eurotext.tif','eurotext.jpg']),],
       )
       
