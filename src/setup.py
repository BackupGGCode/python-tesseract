#!/usr/bin/env python
from __future__ import print_function
"""
setup.py file for SWIG
written by FreeToGo@gmail.com
"""
PACKAGE="python-tesseract"
#VERSION=os.getcwd().split("-")[-1]
VERSION="0.9"
from setuptools import setup, Extension, Command, find_packages
import sys,os,platform,glob,subprocess,sys,distutils
import os
try:
	import jfunc
except:
	import src.jfunc as jfunc
j=jfunc.jfunc()
puts=j.puts
USE_CV=True

osname=j.osname
#library_dirs=[]
#include_dirs=['.']

IncludeLines=["#include \"config.h\"","bool isLibTiff();","bool isLibLept();",
		#	"int Iter_next(tesseract::ResultIterator* ri, tesseract::PageIteratorLevel  level);",
			"int*  AllWordConfidences(tesseract::TessBaseAPI* api);",
			"char* ProcessPagesWrapper(const char* image,tesseract::TessBaseAPI* api);",
			"char* ProcessPagesPix(const char* image,tesseract::TessBaseAPI* api);",
			"char* ProcessPagesFileStream(const char* image,tesseract::TessBaseAPI* api);",
			"char* ProcessPagesBuffer(char* buffer, int fileLen, tesseract::TessBaseAPI* api);",
#			"char* ProcessPagesRaw2(const char* image,tesseract::TessBaseAPI* api);",
			"char* ProcessPagesRaw(const char* image,tesseract::TessBaseAPI* api);"]

cvIncludeLines=["void SetCvImage(PyObject* o, tesseract::TessBaseAPI* api);",
			#	"void SetImage(PyObject* o, tesseract::TessBaseAPI* api);",
			#	"void SetMat(PyObject* o, tesseract::TessBaseAPI* api);",
				"bool SetVariable(const char* var, const char* value, tesseract::TessBaseAPI* api);",
				"char* GetUTF8Text(tesseract::TessBaseAPI* api);"]
from distutils.sysconfig import get_config_vars
def removeFlag(flagName,mflag):
	(opt,) = get_config_vars(mflag)
	if opt:
		os.environ[mflag] = " ".join(
			flag for flag in opt.split() if flag != flagName
			)

def writeIncludeLines(fp,lines) :
	for line in lines:
		fp.write(line+"\n");

def cmd(cmdList):
	process = subprocess.Popen(cmdList.split(), stdout=subprocess.PIPE)
	out, err = process.communicate()
	return out
def pkgconfig(*packages, **kw):
	flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
	ret=cmd("pkg-config --libs --cflags %s" % ' '.join(packages))
	print("ret",ret)
	for token in ret.split():
		if token[:2] in flag_map:
			kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])
		else: # throw others to extra_link_args
			kw.setdefault('extra_link_args', []).append(token)

	for k, v in kw.items(): # remove duplicated
		kw[k] = list(set(v))
	return kw

def listFiles(mdir):
	files=os.listdir(mdir);
	list_files=[]
	for mfile in files:
		if not USE_CV and "opencv" in mfile:
			print(mfile, end=' ')
			print("&"*200)
			continue
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


def my_clean():
	#print "runtime directory:",os.path.dirname(os.path.realpath(__file__))
	pwd=os.path.abspath(os.path.dirname(sys.argv[0]))
	print(pwd)
	rmDirs="build dist deb_dist tesseract.egg-info python_tesseract.egg-info".split(" ")
	rmFiles="main.h config.h tesseract.py *wrap.cpp setuptools* *tar.gz* *.pyc".split(" ")
	print("remove Dirs")
	j.runRm4Dirs(pwd,rmDirs)
	print("remove Files")
	j.runRm4Files(pwd,rmFiles)
	print("[my_clean]Done")
	#old_packages=glob.glob('%s_%s*'%(PACKAGE,VERSION))
	#for package in old_packages:
		#os.system(package)
	
def my_uninstall():
	rmPaths=[]
	files=["*tesseract*"]
	#if osname=='darwin' and j.brew_prefix:
	for rmPath in j.sitepackagesLocations:
		print(rmPath)
		j.runRm4Dirs(rmPath,files)
		j.runRm4Files(rmPath,files)
	os.remove("config.h")
	os.remove("main.h")
	print("Uninstalling is done")

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
		my_clean()
		print("Cleaning is done")
		pass
		return 0
		#_clean.run(self)

class UninstallCommand(_clean):
	description = "custom uninstall command that forcefully removes dist/build directories"
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
		my_uninstall()
		print("*"*100)
			#_clean.run(self)



class GenVariablesLinux:
	def __init__(self, osname,fp_config_h,fp_main_h,sources):
		self.sources=sources
		self.include_dirs=['.']
		self.data_files=[]
		self.osname=osname
		self.fp_config_h=fp_config_h
		self.fp_main_h=fp_main_h
		self.fp_config_h.write("#include <Python.h>\n")
		self.libraries=['stdc++','tesseract','lept']
		self.clang_incls=['tesseract','leptonica']
		self.initialize()
		if osname=="mingw":
			self.mingw_initialise()
			if USE_CV and self.isOpenCVInstalled() :
				self.setCVLibraries()
				self.libraries=["opencv_core248"]+self.libraries
			self.setPaths()
		else:
			if USE_CV and self.isOpenCVInstalled() :
				self.setCVLibraries()

		self.setIncls()
		self.idefine(fp_config_h,osname)
		#if osname!="mingw" and self.isOpenCVInstalled() :
		self.fp_config_h.close()
		self.fp_main_h.close()

	def mingw_initialise(self):
		self.sources.append('ms_fmemopen.c')
		if "64" in sys.version:
			self.mingwPath=os.path.abspath("../mingw32/x86_64-w64-mingw32.static")
		else:
			self.mingwPath=os.path.abspath("../mingw32/i686-pc-mingw32.static")
		
		self.mingwLibPath=os.path.join(self.mingwPath,"lib")
		#self.libraries+=['ws2_32','png','z',"jpeg","tiff","webp"]
		self.libraries+=['opengl32','glu32','ws2_32','z','jpeg']
		self.pathOffset=self.mingwPath
		self.clang_incls.append(os.path.join(self.mingwPath,'include'))
		print("mingwPath=%s"%self.mingwPath)
		self.incls.append(os.path.join(self.mingwPath,"include"))


	def setPaths(self):

		xDir=""
		self.inclPath=os.path.join(self.pathOffset,xDir,"include")
		self.libPath=os.path.join(self.pathOffset,xDir,"lib")
		#self.dllPath=os.path.join(self.pathOffset,xDir,"dll")
		self.pydPath=os.path.join(self.pathOffset,xDir,"pyd")
		self.fp_config_h.write('#include "fmemopen.h"\n')
		self.data_files=[("DLLS", listFiles(self.pydPath))]
		#("Lib\site-packages", listFiles("../dlls"))]
		#(".", listFiles(self.dllPath))]
		self.libs.append(self.libPath)
	def setIncls(self):
		for incl in self.clang_incls:
			mincl=self.inclpath(incl)
			print("!"*500)
			print("mincl=%s\n"%repr(mincl))
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
			self.include_dirs.append(os.path.join(".","cygwin","include"))
			self.include_dirs.append(os.path.join("cygwin/includes/"))


	def inclpath(self,mlib):
		try:
			ipath=checkPath(self.incls,mlib)
		except:
			print(self.incls,mlib)
		#print self.incls,mlib
		if ipath:
			return ipath
		else:
			return None
		assert False, 'Include directory %s was not found' % mlib

	def libpath(self, mlib):
		print("()"*100)
		print(self.libs)
		print("(x)"*100)
		if hasattr(self,"libPath"):
			print(self.libPath)

		ret=checkPath(self.libs,mlib)
		if not ret:
			print("(*)"*100)
			print(("Waring!!!! canot find %s in %s"%(repr(mlib), repr(self.libs))))
		return ret

	def isOpenCVInstalled(self):
		if not USE_CV:
			return 0
		hasOpenCV = 0
		print("$"*200)
		if self.inclpath("opencv2/core/core_c.h"):
			print("%"*200)
			self.idefine(self.fp_config_h,"opencv2")
			self.fp_config_h.write("#include <opencv2/core/core_c.h>\n")
			self.clang_incls.append('opencv2')
			writeIncludeLines(self.fp_main_h,cvIncludeLines)
			hasOpenCV = 1

		#if self.inclpath("opencv/cv.h") :
			#print("@"*200)
			#self.idefine(self.fp_config_h,"opencv")
			#self.fp_config_h.write("#include <opencv/cv.h>\n")
			#self.clang_incls.append('opencv')
			#writeIncludeLines(self.fp_main_h,cvIncludeLines)
			#hasOpenCV = 1
		if hasOpenCV:
			print("*"*200)
		return hasOpenCV

	def setCVLibraries(self):
		if not USE_CV:
			return
		if osname is not "mingw":
			cv_pc=pkgconfig("opencv")
			cv_pc_keys=list(cv_pc.keys())
			print("~~~cv_pc~~~")
			print(cv_pc)
			print(cv_pc_keys)
			if 'libraries' in cv_pc_keys:
				for item in cv_pc['libraries']:
					print(item)
					self.libraries.append(item) 
			elif 'extra_link_args' in cv_pc_keys:
				for item in cv_pc['extra_link_args']:
					print ("Item=",item)
					subItems=item.decode('utf-8').split("open")
					print (subItems)
					libname="open"+subItems[1].split(".")[0]
					print("add lib: %s"%libname)
					if libname!="opencv":
						self.libraries.append(libname)
		else:
			print("No pkg-config support!")
			#if libpath('libopencv_core.so') or libpath('libopencv_core.dylib') or libpath('libopencv_core.dll.a')  or hasOpenCV:
			if self.libpath('libopencv_core.so') or self.libpath('libopencv_core.dylib') or self.libpath('libopencv_core.dll.a')  :
				#if 'opencv_core' not in libraries:
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

		print("===========%s==========="%self.libraries)
		print(self.include_dirs)

	def do(self):
		extra_compile_args=["-Wall", "-O0", '-funroll-loops','-g']
		extra_link_args=[]
		if osname=="mingw":
			extra_link_args.append("-L%s"%self.mingwLibPath)
			if "64" in sys.version:
				extra_compile_args.append("-D MS_WIN64")
			#extra_compile_args.append("-static-libgcc")
			#extra_compile_args.append("-optl-static")
		
		tesseract_module = Extension('_tesseract',
				sources=self.sources,
				#extra_compile_args=["-DEBUG -O0 -pg "],
				#extra_compile_args=["-O0","-g"],
				#extra_compile_args = ["-Wall", "-Wextra", "-O0", '-funroll-loops','-g'],
				extra_compile_args = extra_compile_args,
				extra_link_args = extra_link_args,
				swig_opts=[
								"-c++",
								 "-I"+self.inclpath('tesseract'),
				#				"-I"+os.path.dirname(config.__file__),
								"-I"+self.inclpath('leptonica'),
								"-I"+self.inclpath('opencv2')],
				include_dirs=self.include_dirs,
				#library_dirs=library_dirs,
				libraries=self.libraries,
				)
		return tesseract_module, self.data_files


class GenVariablesDarwin(GenVariablesLinux):
	def __init__(self, osname,fp_config_h,fp_main_h,sources):
		#print "()"*10,get_config_vars('CFLAGS')
		removeFlag("-mno-fused-madd",'CFLAGS')
		#os.system("sed -i .bak 's/baseapi_mini.h/baseapi_mini_darwin.h/g' tesseract.i")
		os.environ["ARCHFLAGS"]="-arch x86_64"
		brew_prefix=subprocess.getstatusoutput('brew --prefix')[1]
		python_version=subprocess.getstatusoutput('python --version')[1].split(" ")[1]
		python_version="python"+".".join(python_version.split(".")[:-1])
		sitePackagesPath=os.path.join(brew_prefix,"lib",python_version,"site-packages")
		if "PYTHONPATH" in os.environ:
			os.environ["PYTHONPATH"]="%s:%s"%(sitePackagesPath,os.environ["PYTHONPATH"])
		else:
			os.environ["PYTHONPATH"]=sitePackagesPath

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


def checkOnePath(mpath,mlib,mext):
	path_to = os.path.join(mpath,mlib)
	if os.path.exists(path_to+"."+mext):
		return path_to
	else:
		files=glob.glob(path_to+"*"+"."+mext)
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print(files)
		print(mext)
		if files and len(files) > 0:
			print(">>>%s"%files[0])
			return files[0][:-4]
		else:
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>> No lib path for path_to=%s mext=%s"%(repr(path_to),repr(mext)))
			#sys.exit(-1)

class GenVariablesWindows:
	def __init__(self,osname,fp_config_h,fp_main_h,sources):
		self.osname=osname
		self.fp_config_h=fp_config_h
		self.fp_main_h=fp_main_h
		self.sources=sources
		self.idefine(fp_config_h,osname)
		self.clang_incls=['tesseract','leptonica']
		self.include_dirs=['.']
		name='python'
		description = """Python Wrapper for Tesseract-OCR """
		self.sources.append('ms_fmemopen.c')
		if osname=="mingw":
			self.pathOffset="..\\mingw"
		else:
			self.pathOffset="..\\vs2008"
		self.initialize()
		self.setCVLibraries()
		self.setIncls()
		self.fp_config_h.close()
		self.fp_main_h.close()
		#print "===========%s==========="%libraries

	def idefine(self, fp, name):
		fp.write("#define __%s__\n\n"%name)


	def initialize(self):
		if "64" not in sys.version:
			xDir="x86"
		else:
			xDir="x64"
		print(("--os is %s"%xDir))
		self.inclPath=os.path.join(self.pathOffset,"include")
		self.libPath=os.path.join(self.pathOffset,xDir,"lib")
		self.dllPath=os.path.join(self.pathOffset,xDir,"dll")
		self.pydPath=os.path.join(self.pathOffset,xDir,"pyd")
		self.fp_config_h.write('#include "fmemopen.h"\n')
		self.data_files=[("DLLS", listFiles(self.pydPath)),
			#("Lib\site-packages", listFiles("../dlls"))]
			(".", listFiles(self.dllPath))]

	def setIncls(self):
		for incl in self.clang_incls:
			mincl=self.inclpath(incl)
			#print "mincl=%s\n"%repr(mincl)
			if mincl:
				self.include_dirs.append(mincl)
		#fp_config_h.write("#endif // __CONFIG_H__\n")


	def inclpath(self,name):
		return checkOnePath(self.inclPath,name,"")
	def libpath(self,name):
		if osname=="mingw":
			libext="a"
		else:
			libext="lib"
		return checkOnePath(self.libPath, name,libext)

	def setCVLibraries(self):
		self.libraries=[self.libpath('libtesseract'),self.libpath('liblept')]
		incl="."
		if not USE_CV:
			return
		cv2IncPath=self.inclpath("opencv2\core\core_c.h")
		print(cv2IncPath)
		if  os.path.exists(cv2IncPath):
			self.idefine(self.fp_config_h,"opencv2")
			self.fp_config_h.write('#include "%s"\n'%cv2IncPath)
			self.fp_config_h.write("#include <Python.h>\n")
			self.libraries.append(self.libpath('opencv_core'))
			self.clang_incls.append('opencv2')
			self.clang_incls.append('.')
			writeIncludeLines(self.fp_main_h,cvIncludeLines)
		else:
			clang_incls.append('opencv')
			writeIncludeLines(self.fp_main_h,cvIncludeLines)

	def do(self):
		tesseract_module = Extension( '_tesseract',
			sources=self.sources,
			#extra_compile_args=["-DEBUG -O0 -pg "],
			#extra_compile_args=["-O0","-g"],
			#extra_compile_args = ["-Wall", "-Wextra", "-O0", '-funroll-loops','-g'],
			#extra_compile_args = [ "-O0", '-funroll-loops','-g'],
			#extra_compile_args = ["-Wall", "-Wextra"],

			swig_opts=[
					"-c++",
					"-I"+self.inclpath('tesseract'),
				#	"-I"+os.path.dirname(config.__file__),
					"-I"+self.inclpath('leptonica'),
				#	"-I"+self.inclpath('opencv2')
				],
			include_dirs=self.include_dirs,
			libraries=self.libraries,
			)
		return tesseract_module, self.data_files

def main():
	data_files=None
	tesseract_module=None
	sources=['tesseract.i','main.cpp']
	description = r"""${python:Provides} Wrapper for Python-${python:Versions}"""


	removeFlag('-Wstrict-prototypes','OPT')


	print("Current Version : %s"%VERSION)

	fp_config_h=open("config.h","w")
	fp_main_h=open("main.h","w")
	fp_config_h.write(
r"""
#ifdef TESS_EXPORTS
#define TESS_API __declspec(dllexport)
#elif defined(TESS_IMPORTS)
#define TESS_API __declspec(dllimport)
#else
#define TESS_API
#define TESS_LOCAL
#define LEPT_DLL

#define TESS_CAPI_INCLUDE_BASEAPI
#endif
"""
#define CV_EXPORTS
#define CV_EXPORTS_W
#define CV_EXPORTS_AS
)

	fp_config_h.write("#pragma once\n")
	writeIncludeLines(fp_main_h,IncludeLines)
	isLinux=osname in ["linux","cygwin"]

	print("os=%s"%osname)

	if osname=="darwin":
		gvl=GenVariablesDarwin(osname,fp_config_h,fp_main_h,sources)
		tesseract_module, data_files=gvl.do()

	elif isLinux or osname=="mingw" :
		gvl=GenVariablesLinux(osname,fp_config_h,fp_main_h,sources)
		tesseract_module, data_files=gvl.do()

	elif osname=="windows":
		gvw=GenVariablesWindows(osname,fp_config_h,fp_main_h,sources)
		tesseract_module, data_files=gvw.do()

	if data_files:
		new_data_files=[]
		for data_file in data_files:
			if not USE_CV and "opencv" in data_file :
				cotinue
			else:
				new_data_files.append(data_file)
		print("$$$data_files=%s"%repr(data_files))
		data_files=new_data_files

	setup (name = PACKAGE,
			version = VERSION,
			author	  = "FreeToGo Nowhere",
			author_email="freetogo@gmail.com",
			maintainer = "FreeToGo Nowhere",
			maintainer_email="freetogo@gmail.com",
			description = description,
			ext_modules = [tesseract_module],
			py_modules = ["tesseract"],
			cmdclass={
			'clean': CleanCommand,
			'uninstall' : UninstallCommand
			},
			packages =
				find_packages(
					#exclude=['distribute_setup']
				),
				data_files=data_files,
			#	 data_files=[('.',['test.py','eurotext.tif','eurotext.jpg']),],
			#data_files=data_files
			license='MIT',
			keywords='geocode geocoding gis geographical maps earth distance',
			classifiers=["Development Status :: 5 - Production/Stable",
				"Intended Audience :: Developers",
				"Intended Audience :: Science/Research",
				"License :: OSI Approved :: MIT License",
				"Operating System :: OS Independent",
				"Programming Language :: Python",
				"Topic :: Scientific/Engineering :: GIS",
				"Topic :: Software Development :: Libraries :: Python Modules",
				"Programming Language :: Python :: 2",
				"Programming Language :: Python :: 3",
				]
		   )


if __name__ == "__main__":
	main()
