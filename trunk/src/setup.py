#!/usr/bin/env python
"""
setup.py file for SWIG
written by FreeToGo@gmail.com
"""
PACKAGE="python-tesseract"
#VERSION=os.getcwd().split("-")[-1]
VERSION="0.8"
from setuptools import setup, Extension, Command, find_packages
import sys,os,platform,glob,commands,sys,distutils
import os

#library_dirs=[]
#include_dirs=['.']
osname=platform.uname()[0].lower()
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
from distutils.sysconfig import get_config_vars
def removeFlag(flagName,mflag):
	(opt,) = get_config_vars(mflag)
	os.environ[mflag] = " ".join(
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


def checkPath(paths,mlib):
	for pref in paths:
		path_to = os.path.join(pref, mlib)
		#print "path_to=%s\n"%repr(path_to)
		if os.path.exists(path_to):
			return path_to

from distutils.command.clean import clean as _clean
#class CleanCommand(Command):
class CleanCommand(_clean):
	description = "custom clean command that forcefully removes dist/build directories"
	user_options = [("all", "a", ""),]
	def initialize_options(self):
		self.cwd = None
		self.all = None
		pass

	def finalize_options(self):
		self.cwd = os.getcwd()
		pass

	def run(self):
		assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
		if osname != "windows":
			os.system('rm -rf ./build ./dist ./deb_dist')
			old_packages=glob.glob('%s_%s*'%(PACKAGE,VERSION))
			for package in old_packages:
				os.system(package)
		else:
			os.system('del /S /Q build dist')
		#_clean.run(self)



class GenVariablesLinux:
	def __init__(self, osname,fp_config_h,fp_main_h,sources):
		self.sources=sources
		self.include_dirs=['.']
		self.data_files=[]
		self.osname=osname
		self.fp_config_h=fp_config_h
		self.fp_main_h=fp_main_h
		self.initialize()
		self.fp_config_h.write("#include <Python.h>\n")
		self.libraries=['stdc++','tesseract','lept']
		self.clang_incls=['tesseract','leptonica']
		self.setIncls()
		self.idefine(fp_config_h,osname)
		if self.isOpenCVInstalled():
			self.setCVLibraries()
		self.fp_config_h.close()
		self.fp_main_h.close()

	def setIncls(self):
		for incl in self.clang_incls:
			mincl=self.inclpath(incl)
			#print "mincl=%s\n"%repr(mincl)
			if mincl:
				self.include_dirs.append(mincl)

	def idefine(self,fp,name):
		fp.write("#ifndef __%s__\n"%name)
		fp.write("\t#define __%s__\n"%name)
		fp.write("#endif\n")

	
	def initialize(self):

		prefix=sys.prefix
		self.incls = ['/usr/include', '/usr/local/include']
		self.libs=['/usr/lib', '/usr/local/lib']
		if "cygwin" in osname:
			self.include_dirs.append(os.path.join(".","cygwin","includes"))
			self.include_dirs.append(os.path.join("cygwin/includes/"))

	def inclpath(self,mlib):
		ipath=checkPath(self.incls,mlib)
		if ipath:
			return ipath
		else:
			return None
		assert False, 'Include directory %s was not found' % mlib

	def libpath(self, mlib):
		return checkPath(self.libs,mlib)

	def isOpenCVInstalled(self):
		hasOpenCV = 0
		if self.inclpath("opencv2/core/core_c.h"):
			self.idefine(self.fp_config_h,"opencv2")
			self.fp_config_h.write("#include <opencv2/core/core_c.h>\n")
			self.clang_incls.append('opencv2')
			writeIncludeLines(self.fp_main_h,cvIncludeLines)
			hasOpenCV = 1

		if self.inclpath("opencv/cv.h") :
			self.idefine(self.fp_config_h,"opencv")
			self.fp_config_h.write("#include <opencv/cv.h>\n")
			self.clang_incls.append('opencv')
			writeIncludeLines(self.fp_main_h,cvIncludeLines)
			hasOpenCV = 1
		return hasOpenCV

	def setCVLibraries(self):
		cv_pc=pkgconfig("opencv")
		cv_pc_keys=cv_pc.keys()
		print "~~~cv_pc~~~"
		print cv_pc
		print cv_pc_keys
		if 'libraries' in cv_pc_keys:
			self.libraries= self.libraries + cv_pc['libraries']
		elif 'extra_link_args' in cv_pc_keys:
			for item in cv_pc['extra_link_args']:
				libname="open"+item.split("libopen")[1].split(".")[0]
				print "add lib: %s"%libname
				self.libraries.append(libname)
		else:
			print "*"*100
			print "No pkg-config support!"
			#if libpath('libopencv_core.so') or libpath('libopencv_core.dylib') or libpath('libopencv_core.dll.a')  or hasOpenCV:
			if libpath('libopencv_core.so') or libpath('libopencv_core.dylib') or libpath('libopencv_core.dll.a')  :
				if 'opencv_core' not in libraries:
					self.libraries.append('opencv_contrib')
					self.libraries.append('opencv_highgui')
					self.libraries.append('opencv_calib3d')
					#self.libraries.append('opencv_nonfree')
					self.libraries.append('opencv_flann')
					self.libraries.append('opencv_gpu')
					self.libraries.append('opencv_features2d')
					self.libraries.append('opencv_video')
					self.libraries.append('opencv_objdetect')
					self.libraries.append('opencv_core')
					self.libraries.append('opencv_ml')
					self.libraries.append('opencv_legacy')
		
		print "===========%s==========="%self.libraries
		print "&"*10,self.include_dirs

	def do(self):
		
		tesseract_module = Extension('_tesseract',
				sources=self.sources,
				#extra_compile_args=["-DEBUG -O0 -pg "],
				#extra_compile_args=["-O0","-g"],
				#extra_compile_args = ["-Wall", "-Wextra", "-O0", '-funroll-loops','-g'],
				extra_compile_args = ["-Wall", "-O0", '-funroll-loops','-g'],
				swig_opts=[
								"-c++",
								 "-I"+self.inclpath('tesseract'),
				#				"-I"+os.path.dirname(config.__file__),
								"-I"+self.inclpath('leptonica')],
				include_dirs=self.include_dirs,
				#library_dirs=library_dirs,
				libraries=self.libraries,
											)
		return tesseract_module, self.data_files


class GenVariablesDarwin(GenVariablesLinux):
	def __init__(self, osname,fp_config_h,fp_main_h,sources):
		print "()"*10,get_config_vars('CFLAGS')
		removeFlag("-mno-fused-madd",'CFLAGS')
		GenVariablesLinux.__init__(self,osname,fp_config_h,fp_main_h,sources)
		
	def initialize(self):
		self.sources.append('ag5_fmemopen.c')
		if os.path.exists("/usr/local/Cellar"):
			prefix="/usr/local"
		else:
			prefix="/opt/local"
		self.incls = [os.path.join(prefix,'include')]
		self.libs=[os.path.join(prefix,'lib')]
		self.fp_config_h.write('#include "fmemopen.h"\n')
		self.fp_config_h.write('#define HAVE_LIBLEPT\n')


def genVariablesWindows(osname,fp_config_h,fp_main_h,sources):
	idefine(fp_config_h,osname)
	clang_incls=['tesseract','leptonica']
	include_dirs=['.']
	name='python'
	description = """Python Wrapper for Tesseract-OCR """

	sources.append('ms_fmemopen.c')
	pathOffset="vs2008"
	
	def idefine(fp,name,osname):
		fp.write("#define __%s__\n\n"%name)

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
		fp_config_h.write('#include "opencv2/core/core_c.h"\n')
		fp_config_h.write("#include <Python.h>\n")
		libraries.append(libpath('opencv_core'))
		clang_incls.append('opencv2')
		clang_incls.append('.')
		writeIncludeLines(fp_main_h,cvIncludeLines)
	else:
		clang_incls.append('opencv')
		writeIncludeLines(fp_main_h,cvIncludeLines)
	fp_config_h.write('#include "fmemopen.h"\n')
	self.data_files=[("DLLS", listFiles(pydPath)),
					#("Lib\site-packages", listFiles("../dlls"))]
					(".", listFiles(dllPath))]

	#fp_config_h.write("#endif // __CONFIG_H__\n")
	fp_config_h.close()
	fp_main_h.close()
	print "===========%s==========="%libraries


	for incl in clang_incls:
		mincl=inclpath(incl)
		#print "mincl=%s\n"%repr(mincl)
		if mincl:
			#print "what the fuck"
			include_dirs.append(mincl)

	tesseract_module = Extension('_tesseract',
										sources=self.sources,
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
										#library_dirs=library_dirs,
										libraries=libraries,
										)

	return tesseract_module, self.data_files

def main():
	
	sources=['tesseract.i','main.cpp']
	description = """${python:Provides} Wrapper for Python-${python:Versions} """,

	
	removeFlag('-Wstrict-prototypes','OPT')


	print "Current Version : %s"%VERSION

	fp_config_h=open("config.h","w")
	fp_main_h=open("main.h","w")


	fp_config_h.write("#pragma once\n")
	writeIncludeLines(fp_main_h,IncludeLines)
	isLinux=osname in ["linux","cygwin"]

	print "os=%s"%osname
	
	if osname=="darwin":
		gvl=GenVariablesDarwin(osname,fp_config_h,fp_main_h,sources)
		tesseract_module, data_files=gvl.do()
	
	elif isLinux:
		gvl=GenVariablesLinux(osname,fp_config_h,fp_main_h,sources)
		tesseract_module, data_files=gvl.do()

	elif osname=="windows":
		tesseract_module, data_files=genVariablesWindows(osname,fp_config_h,fp_main_h,sources)


	setup (name = PACKAGE,
			version = VERSION,
			author	  = "FreeToGo Nowhere",
			author_email="freetogo@gmail.com",
			maintainer = "FreeToGo Nowhere",
			maintainer_email="freetogo@gmail.com",
			description = description,
			ext_modules = [tesseract_module],
			py_modules = ["tesseract"],
			license="LGPL/MIT",
			keywords=['tesseract', 'ocr' ],
			cmdclass={
			'clean': CleanCommand
			},
			packages =
				find_packages(
					#exclude=['distribute_setup']
				),
				data_files=data_files
			#	 data_files=[('.',['test.py','eurotext.tif','eurotext.jpg']),],
			#data_files=data_files
		   )


if __name__ == "__main__":
	main()
