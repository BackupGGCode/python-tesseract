#!/usr/bin/env python
"""
setup.py file for SWIG
written by FreeToGo@gmail.com
"""
from distutils.core import setup, Extension, Command
import sys,os,platform
osname=platform.uname()[0].lower()
if osname=='darwin':
	prefix="/opt/local"
	incls = ['/opt/local/include']
	libs=['/opt/local/lib']
else:
	prefix=sys.prefix
	incls = ['/usr/include', '/usr/local/include']
	libs=['/usr/lib', '/usr/local/lib']

incl=os.path.join(prefix,"include")
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
		os.system('rm -rf ./build ./dist ./deb_dist')
		

def checkPath(paths,mlib):
	for pref in paths:
		path_to = os.path.join(pref, mlib)
		if os.path.exists(path_to):
			return path_to
 
def inclpath(mlib):
	return checkPath(incls,mlib)
	assert False, 'Include directory %s was not found' % mlib

def libpath(mlib):
	return checkPath(libs,mlib)
	

libraries=['stdc++','tesseract','lept']


def idefine(fp,name):
	fp.write("#ifndef __%s__\n"%name)
	fp.write("\t#define __%s__\n"%name)
	fp.write("#endif\n")

fp=open("config.h","w")
if osname=='darwin' or osname=='linux':
	if inclpath("opencv/cv.h")  :
		idefine(fp,"opencv");
		fp.write("#include <opencv/cv.h>\n");
		fp.write("#include <Python.h>\n");
	elif inclpath("opencv2/core/core_c.h"):
		idefine(fp,"opencv2");
		fp.write("#include <opencv2/core/core_c.h>\n");
		fp.write("#include <Python.h>\n");
fp.close()




if libpath('libopencv_core.so'):
	libraries.append('opencv_core')
	
tesseract_module = Extension('_tesseract',
									sources=['tesseract.i','' 'main_dummy.cpp','fmemopen.c'],
									#extra_compile_args=["-DEBUG -O1 -pg "],
									swig_opts=["-c++", "-I"+inclpath('tesseract'),
													"-I"+incl,
													"-I"+inclpath('leptonica')],
									include_dirs=['.',inclpath('tesseract'),
													incl,
													inclpath('leptonica')],
									libraries=libraries,
								
									)
									
setup (name = 'python-tesseract',
	   version = version_number,
	   author	  = "FreeToGo Nowhere",
	   description = """${python:Provides} Wrapper for Python-${python:Versions} """,
	   ext_modules = [tesseract_module],
	   py_modules = ["tesseract"],
	   cmdclass={
		'clean': CleanCommand
		}
  #	 data_files=[('.',['test.py','eurotext.tif','eurotext.jpg']),],
	   )
	   
