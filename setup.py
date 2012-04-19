#!/usr/bin/env python
"""
setup.py file for SWIG
written by FreeToGo@gmail.com
"""
#from distutils.core import setup, Extension, Command, find_packages
from setuptools import setup, Extension, Command, find_packages
import sys,os,platform
osname=platform.uname()[0].lower()

sources=['tesseract.i','' 'main_dummy.cpp']

version_number=os.getcwd().split("-")[-1]
print "Current Version : %s"%version_number
fp=open("config.h","w")


def listFiles(mdir):
	files=os.listdir(mdir);
	list_files=[]
	for mfile in files:
		list_files.append(os.path.join(mdir,mfile))
	return list_files

def idefine(fp,name):
	fp.write("#ifndef __%s__\n"%name)
	fp.write("\t#define __%s__\n"%name)
	fp.write("#endif\n")

idefine(fp,osname)

class CleanCommand(Command):
	description = "custom clean command that forcefully removes dist/build directories"
	user_options = []
	def initialize_options(self):
		self.cwd = None
	def finalize_options(self):
		self.cwd = os.getcwd()
	def run(self):
		assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
		if osname != "windows":
			os.system('rm -rf ./build ./dist ./deb_dist')
		else:
			os.system('del /S /Q build dist deb_dist')

def inclpath(mlib):
	return checkPath(incls,mlib)
	assert False, 'Include directory %s was not found' % mlib		
	
if osname=="darwin" or osname=="linux" :
	data_files=[]
	sources.append('fmemopen.c')
	if osname=='darwin':
		prefix="/opt/local"
		incls = ['/opt/local/include']
		libs=['/opt/local/lib']
	else:
		prefix=sys.prefix
		incls = ['/usr/include', '/usr/local/include']
		libs=['/usr/lib', '/usr/local/lib']

#	incl=os.path.join(prefix,"include")
#	print "include path=%s"%incl
	

	

	def checkPath(paths,mlib):
		for pref in paths:
			path_to = os.path.join(pref, mlib)
			if os.path.exists(path_to):
				return path_to
	 
	

	def libpath(mlib):
		return checkPath(libs,mlib)
		

	
	if osname=='darwin':
		fp.write('#include "fmemopen.h"\n')
		
	if inclpath("opencv/cv.h")  :
		idefine(fp,"opencv")
		fp.write("#include <opencv/cv.h>\n")
		fp.write("#include <Python.h>\n")
	elif inclpath("opencv2/core/core_c.h"):
		idefine(fp,"opencv2")
		fp.write("#include <opencv2/core/core_c.h>\n")
		fp.write("#include <Python.h>\n")


	libraries=['stdc++','tesseract','lept']
	if libpath('libopencv_core.so'):
		libraries.append('opencv_core')

elif osname=="windows":
	
	fp.write('#include "util-fmemopen.h"\n')
	sources.append('util-fmemopen.cpp')
	
	pathOffset="../vs2008"
	inclPath=os.path.join(pathOffset,"include")
	libPath=os.path.join(pathOffset,"lib")
	def inclpath(name):
		return os.path.join(inclPath,name)
	def libpath(name):
		return os.path.join(libPath,'lib%s.lib'%name)
		
	
	libraries=['libtesseract302','liblept']
	incl="."
	cv2IncPath=inclpath("opencv2/core/core_c.h")
	if  cv2IncPath:
		idefine(fp,"opencv2")
		fp.write('#include "opencv2/core/core_c.h"\n')
		fp.write("#include <Python.h>\n")
		libraries.append('opencv_core240')
	
	
	data_files=[("DLLs", listFiles("../pyds")),
					(".", listFiles("../dlls"))]

fp.close()
print "===========%s==========="%libraries
tesseract_module = Extension('_tesseract',
									sources=sources,
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
		},
		packages = find_packages(exclude=['distribute_setup']),
		#	 data_files=[('.',['test.py','eurotext.tif','eurotext.jpg']),],
		data_files=data_files
	   )
	   
