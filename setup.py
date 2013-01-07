#!/usr/bin/env python
"""
setup.py file for SWIG
written by FreeToGo@gmail.com
"""

from setuptools import setup, Extension, Command, find_packages
import sys,os,platform,glob

def writeIncludeLines(fp,lines) :
	for line in lines:
		fp.write(line+"\n");


osname=platform.uname()[0].lower()
print "os=%s"%osname
sources=['tesseract.i','' 'main_dummy.cpp']
name = 'python-tesseract'
description = """${python:Provides} Wrapper for Python-${python:Versions} """,
version_number=os.getcwd().split("-")[-1]
print "Current Version : %s"%version_number
include_dirs=['.']

fp=open("config.h","w")
fp.write("#pragma once\n")
#fp.write("#ifndef __CONFIG_H__\n")
#fp.write("#define __CONFIG_H__\n")
clang_incls=['tesseract','leptonica']
fp2=open("main_dummy.h","w")

IncludeLines=["#include \"config.h\"","bool isLibTiff();","bool isLibLept();",
			"char* ProcessPagesWrapper(const char* image,tesseract::TessBaseAPI* api);",
			"char* ProcessPagesPix(const char* image,tesseract::TessBaseAPI* api);",
			"char* ProcessPagesFileStream(const char* image,tesseract::TessBaseAPI* api);",
			"char* ProcessPagesBuffer(char* buffer, int fileLen, tesseract::TessBaseAPI* api);",
			"char* ProcessPagesRaw2(const char* image,tesseract::TessBaseAPI* api);",
			"char* ProcessPagesRaw(const char* image,tesseract::TessBaseAPI* api);"]


cvIncludeLines=["void SetCvImage(PyObject* o, tesseract::TessBaseAPI* api);",
				"bool SetVariable(const char* var, const char* value, tesseract::TessBaseAPI* api);",
				"char* GetUTF8Text(tesseract::TessBaseAPI* api);"]
writeIncludeLines(fp2,IncludeLines)


def listFiles(mdir):
	files=os.listdir(mdir);
	list_files=[]
	for mfile in files:
		list_files.append(os.path.join(mdir,mfile))
	return list_files

def idefine(fp,name):
	if osname=="windows":
		fp.write("#define __%s__\n\n"%name)
	else:
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
			os.system('del /S /Q build dist')

def inclpath(mlib):
	ipath=checkPath(incls,mlib)
	if ipath:
		return ipath
	else:
		return None
	assert False, 'Include directory %s was not found' % mlib

if osname=="darwin" or osname=="linux" or "cygwin" in osname:
	data_files=[]

	if osname=='darwin':
		sources.append('ag5_fmemopen.c')
		if os.path.exists("/usr/local/Cellar"):
			prefix="/usr/local"
		else:
			prefix="/opt/local"
		incls = [os.path.join(prefix,'include')]
		libs=[os.path.join(prefix,'lib')]
		fp.write('#include "fmemopen.h"\n')
	else:
		prefix=sys.prefix
		incls = ['/usr/include', '/usr/local/include']
		libs=['/usr/lib', '/usr/local/lib']
		if "cygwin" in osname:
			include_dirs.append(os.path.join(".","cygwin","includes"))
#	incl=os.path.join(prefix,"include")
#	print "include path=%s"%incl

	def checkPath(paths,mlib):
		for pref in paths:
			path_to = os.path.join(pref, mlib)
			#print "path_to=%s\n"%repr(path_to)
			if os.path.exists(path_to):
				return path_to

	def libpath(mlib):
		return checkPath(libs,mlib)

	if inclpath("opencv2/core/core_c.h"):
		idefine(fp,"opencv2")
		fp.write("#include <opencv2/core/core_c.h>\n")
		clang_incls.append('opencv2')
		writeIncludeLines(fp2,cvIncludeLines)
	elif inclpath("opencv/cv.h")  :
		idefine(fp,"opencv")
		fp.write("#include <opencv/cv.h>\n")
		clang_incls.append('opencv')
		writeIncludeLines(fp2,cvIncludeLines)
	fp.write("#include <Python.h>\n")


	libraries=['stdc++','tesseract','lept']
	if libpath('libopencv_core.so') or libpath('libopencv_core.dylib') or libpath('libopencv_core.dll.a'):
		libraries.append('opencv_core')

elif osname=="windows":
	name='python'
	description = """Python Wrapper for Tesseract-OCR """
	sources.append('ms_fmemopen.c')

	pathOffset="vs2008"
	inclPath=os.path.join(pathOffset,"includes")
	libPath=os.path.join(os.getcwd(),pathOffset,"libs")
	dllPath=os.path.join(pathOffset,"dlls")
	pydPath=os.path.join(pathOffset,"pyds")
	def checkOnePath(mpath,mlib,mext):
		path_to = os.path.join(mpath,mlib)
		print "****************path_to=%s %s\n"%(repr(path_to),os.path.exists(path_to+"."+mext))
		if os.path.exists(path_to+"."+mext):
			return path_to
		else:
			files=glob.glob(path_to+"*")
			print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
			print files
			if files and len(files) > 0:
				print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>%s"%files[0]
				
				return files[0][:-4]

	
	def inclpath(name):
		return checkOnePath(inclPath,name,"")
	def libpath(name):
		return checkOnePath(libPath, name,"lib")


	libraries=[libpath('libtesseract'),libpath('liblept')]
	incl="."
	cv2IncPath="opencv2/core/core_c.h"
	if  cv2IncPath:
		idefine(fp,"opencv2")
		fp.write('#include "opencv2/core/core_c.h"\n')
		fp.write("#include <Python.h>\n")
		libraries.append(libpath('opencv_core'))
		clang_incls.append('opencv2')
		writeIncludeLines(fp2,cvIncludeLines)
	else:
		clang_incls.append('opencv')
		writeIncludeLines(fp2,cvIncludeLines)
	fp.write('#include "fmemopen.h"\n')
	data_files=[("DLLS", listFiles(pydPath)),
					#("Lib\site-packages", listFiles("../dlls"))]
					(".", listFiles(dllPath))]

#fp.write("#endif // __CONFIG_H__\n")
fp.close()
fp2.close()
print "===========%s==========="%libraries


for incl in clang_incls:
	mincl=inclpath(incl)
	#print "mincl=%s\n"%repr(mincl)
	if mincl:
		#print "what the fuck"
		include_dirs.append(mincl)
print "aaaaaaaaaaaaaaaaaaaaaaaaaaa"
print repr(include_dirs)
tesseract_module = Extension('_tesseract',
									sources=sources,
									#extra_compile_args=["-DEBUG -O1 -pg "],
									swig_opts=["-c++", "-I"+inclpath('tesseract'),
									#				"-I"+os.path.dirname(config.__file__),
													"-I"+inclpath('leptonica')],
									include_dirs=include_dirs,
									libraries=libraries,

									)

setup (name = name,
		version = version_number,
		author	  = "FreeToGo Nowhere",
		description = description,
		ext_modules = [tesseract_module],
		py_modules = ["tesseract"],
		cmdclass={
		'clean': CleanCommand
		},
		packages = find_packages(exclude=['distribute_setup']),
		data_files=data_files
		#	 data_files=[('.',['test.py','eurotext.tif','eurotext.jpg']),],
		#data_files=data_files
	   )


