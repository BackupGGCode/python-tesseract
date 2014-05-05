#!/usr/bin/env python
"""
setup.py file for SWIG
written by FreeToGo@gmail.com
"""

from setuptools import setup, Extension, Command, find_packages
import sys,os,platform,glob,commands,sys

IncludeLines=["#include \"config.h\"","bool isLibTiff();","bool isLibLept();",
			"int*  AllWordConfidences(tesseract::TessBaseAPI* api);",
			"char* ProcessPagesWrapper(const char* image,tesseract::TessBaseAPI* api);",
			"char* ProcessPagesPix(const char* image,tesseract::TessBaseAPI* api);",
			"char* ProcessPagesFileStream(const char* image,tesseract::TessBaseAPI* api);",
			"char* ProcessPagesBuffer(char* buffer, int fileLen, tesseract::TessBaseAPI* api);",
#			"char* ProcessPagesRaw2(const char* image,tesseract::TessBaseAPI* api);",
			"char* ProcessPagesRaw(const char* image,tesseract::TessBaseAPI* api);"]

cvIncludeLines=["void SetCvImage(PyObject* o, tesseract::TessBaseAPI* api);",
			#	"void SetMat(PyObject* o, tesseract::TessBaseAPI* api);",
				"bool SetVariable(const char* var, const char* value, tesseract::TessBaseAPI* api);",
				"char* GetUTF8Text(tesseract::TessBaseAPI* api);"]

def removeFlag(flagName):
	import os
	from distutils.sysconfig import get_config_vars
	(opt,) = get_config_vars('OPT')
	os.environ['OPT'] = " ".join(
		flag for flag in opt.split() if flag != flagName
		)

def writeIncludeLines(fp,lines) :
	for line in lines:
		fp.write(line+"\n");

def pkgconfig(*packages, **kw):
	flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
	for token in commands.getoutput("pkg-config --libs --cflags %s" % ' '.join(packages)).split():
		if flag_map.has_key(token[:2]):
			kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])
		else: # throw others to extra_link_args
			kw.setdefault('extra_link_args', []).append(token)

	for k, v in kw.iteritems(): # remove duplicated
		kw[k] = list(set(v))
	return kw

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


removeFlag('-Wstrict-prototypes')
osname=platform.uname()[0].lower()
print "os=%s"%osname
library_dirs=[]

sources=['tesseract.i','main.cpp']
name = 'python-tesseract'
description = """${python:Provides} Wrapper for Python-${python:Versions} """,
version_number=os.getcwd().split("-")[-1]
print "Current Version : %s"%version_number
include_dirs=['.']

fp=open("config.h","w")
fp.write("#pragma once\n")
clang_incls=['tesseract','leptonica']
fp2=open("main.h","w")

writeIncludeLines(fp2,IncludeLines)
idefine(fp,osname)
isLinux=osname in ["darwin","linux","cygwin"]


if isLinux:
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
		fp.write('#define HAVE_LIBLEPT\n')
	else:
		prefix=sys.prefix
		incls = ['/usr/include', '/usr/local/include']
		libs=['/usr/lib', '/usr/local/lib']
		if "cygwin" in osname:
			include_dirs.append(os.path.join(".","cygwin","includes"))
			include_dirs.append(os.path.join("cygwin/includes/"))

	def inclpath(mlib):
		ipath=checkPath(incls,mlib)
		if ipath:
			return ipath
		else:
			return None
		assert False, 'Include directory %s was not found' % mlib


	def checkPath(paths,mlib):
		for pref in paths:
			path_to = os.path.join(pref, mlib)
			#print "path_to=%s\n"%repr(path_to)
			if os.path.exists(path_to):
				return path_to

	def libpath(mlib):
		return checkPath(libs,mlib)
	hasOpenCV = 0
	if inclpath("opencv2/core/core_c.h"):
		idefine(fp,"opencv2")
		fp.write("#include <opencv2/core/core_c.h>\n")
		clang_incls.append('opencv2')
		writeIncludeLines(fp2,cvIncludeLines)
		hasOpenCV = 1

	if inclpath("opencv/cv.h")  :
		idefine(fp,"opencv")
		fp.write("#include <cv.h>\n")
		clang_incls.append('opencv')
		writeIncludeLines(fp2,cvIncludeLines)
		hasOpenCV = 1

	fp.write("#include <Python.h>\n")
	libraries=['stdc++','tesseract','lept']

	cv_pc=pkgconfig("opencv")
	cv_pc_keys=cv_pc.keys()
	print "~~~cv_pc~~~"
	print cv_pc
	print cv_pc_keys
	if 'libraries' in cv_pc_keys:
		libraries= libraries + cv_pc['libraries']
	elif 'extra_link_args' in cv_pc_keys:
		for item in cv_pc['extra_link_args']:
			libname="open"+item.split("libopen")[1].split(".")[0]
			print "add lib: %s"%libname
			libraries.append(libname)
	else:
		print "*"*100
		print "No pkg-config support!"
		if libpath('libopencv_core.so') or libpath('libopencv_core.dylib') or libpath('libopencv_core.dll.a')  or hasOpenCV:
			if 'opencv_core' not in libraries:
				libraries.append('opencv_contrib')
				libraries.append('opencv_highgui')
				libraries.append('opencv_calib3d')
				#libraries.append('opencv_nonfree')
				libraries.append('opencv_flann')
				libraries.append('opencv_gpu')
				libraries.append('opencv_features2d')
				libraries.append('opencv_video')
				libraries.append('opencv_objdetect')
				libraries.append('opencv_core')
				libraries.append('opencv_ml')
				libraries.append('opencv_legacy')

elif osname=="windows":
	name='python'
	description = """Python Wrapper for Tesseract-OCR """

	sources.append('ms_fmemopen.c')
	pathOffset="vs2008"
#	if "64" not in sys.version:
#		xDir="x86"
#	else:
#		xDir="x64"
	xDir="x86"
	print("--os is %s"%xDir)
	inclPath=os.path.join(pathOffset,"includes")
	libPath=os.path.join(pathOffset,xDir,"libs")
	dllPath=os.path.join(pathOffset,xDir,"dlls")
	pydPath=os.path.join(pathOffset,xDir,"pyds")
	def checkOnePath(mpath,mlib,mext):
		path_to = os.path.join(mpath,mlib)
		print "****************path_to=%s %s\n"%(repr(path_to),os.path.exists(path_to+"."+mext))
		if os.path.exists(path_to+"."+mext):
			return path_to
		else:
			files=glob.glob(path_to+"*"+"."+mext)
			print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
			print files
			print mext
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
		clang_incls.append('.')
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

print repr(include_dirs)
tesseract_module = Extension('_tesseract',
									sources=sources,
									#extra_compile_args=["-DEBUG -O0 -pg "],
									#extra_compile_args=["-O0","-g"],
									#extra_compile_args = ["-Wall", "-Wextra", "-O0", '-funroll-loops','-g'],
									extra_compile_args = ["-Wall", "-O0", '-funroll-loops','-g'],
									swig_opts=[
													"-c++",
													 "-I"+inclpath('tesseract'),
									#				"-I"+os.path.dirname(config.__file__),
													"-I"+inclpath('leptonica')],
									include_dirs=include_dirs,
									library_dirs=library_dirs,
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


