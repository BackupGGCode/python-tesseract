#!/usr/bin/env python
"""
setup.py file for SWIG
written by FreeToGo@gmail.com
"""
from distutils.core import setup, Extension
from distutils.command.clean import clean
import sys,os,platform,glob

#osname=platform.uname()[0]
osname=sys.platform
extra_objects=" ".split()
prefix=sys.prefix
sources="tesseract.i main_dummy.cpp".split()
extra_link_args=[]
if osname=='darwin':
	prefix="/opt/local"
	sources="tesseract.i main_dummy.cpp fmemopen.c".split()
elif osname=="cygwin":
	#extra_link_args = "/usr/lib/libtesseract_api.a /usr/lib/libtesseract_main.a /usr/lib/libtesseract_cube.a /usr/lib/libtesseract_neural.a /usr/lib/libtesseract_textord.a /usr/lib/libtesseract_classify.a /usr/lib/libtesseract_dict.a /usr/lib/libtesseract_ccstruct.a /usr/lib/libtesseract_image.a /usr/lib/libtesseract_cutil.a /usr/lib/libtesseract_viewer.a /usr/lib/libtesseract_ccutil.a /usr/lib/libtesseract_main.a /usr/lib/libtesseract_wordrec.a /usr/lib/libtesseract_textord.a /usr/lib/libtesseract_wordrec.a /usr/lib/libtesseract_classify.a /usr/lib/libtesseract_dict.a /usr/lib/libtesseract_ccstruct.a /usr/lib/libtesseract_image.a /usr/lib/libtesseract_cutil.a /usr/lib/libtesseract_viewer.a /usr/lib/libtesseract_ccutil.a".split()
	extra_link_args = "/usr/lib/libtesseract_main.a /usr/lib/libtesseract_textord.a /usr/lib/libtesseract_wordrec.a".split()      #must come first but why?
	extra_link_args += glob.glob(os.path.join(prefix,"lib/libtess*.a"))
	extra_link_args +="/usr/lib/libwebp.a".split()
	extra_link_args +="-lgif -ljpeg -lpng -ltiff".split()
	extra_link_args +="-llept".split()
	#extra_link_args +="-lstdc++ -llept -lSM -luuid -lintl -liconv -lICE -lX11 -lxcb -lXau -lXdmcp  -ljbig -lpthread -lz".split()
	
incl=os.path.join(prefix,"include")
print "include path=%s"%incl
version_number=os.getcwd().split("-")[-1]
print "Current Version : %s"%version_number


class CleanCommand(clean):
    #description = "custom clean command that forcefully removes dist/build directories"
	#user_options = [('build-base=', 'b', "base build directory (default: 'build.build-base')"), 
		#('build-lib=', None, "build directory for all modules (default: 'build.build-lib')"), 
		#('build-temp=', 't', "temporary build directory (default: 'build.build-temp')"), 
		#('build-scripts=', None, "build directory for scripts (default: 'build.build-scripts')"), 
		#('bdist-base=', None, 'temporary directory for built distributions'), 
		#('all', 'a', 'remove all build output, not just temporary by-products')]
	def initialize_options(self):
		self.cwd = None
		clean.initialize_options(self)
		
	def finalize_options(self):
		self.cwd = os.getcwd()
		clean.finalize_options(self)
		
	def run(self):
		clean.run(self)
		assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
		#os.system('rm -rf ./build ./dist')
	
        

def inclpath(mlib):
	return os.path.join(incl,mlib)
	
tesseract_module = Extension('_tesseract',
									sources=sources,
									swig_opts=["-c++", "-I"+inclpath('tesseract'),
													"-I"+incl,
													"-I"+inclpath('leptonica')],
									extra_objects=extra_objects,
									include_dirs=['.',inclpath('tesseract'),
													incl,
													inclpath('leptonica')],
									#libraries=['stdc++','tesseract_api','lept'],
									libraries=['tesseract_api'],
									extra_link_args=extra_link_args
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
       
