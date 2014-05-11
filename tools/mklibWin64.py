#!/usr/bin/python
# filename: mklib-win64.py
# make import x86_64 import-lib from windows x64 dll
# author: cheungmine@gmail.com
# date: 2013-5
# version: 0.1
#
# MinGW:
#   $ python build-win64.py target_dll
#   $ python build-win64.py libtiff-5.dll
#   $ python build-win64.py libtiff-5
#   $ python build-win64.py tiff-5
#   $ python build-win64.py c:/path/to/libtiff-5
# ERROR: $ python build-win64.py c:\path\to\libtiff-5
#
# file operation:
# import shutil
#
## copy file:
#   shutil.copy(myfile, tmpfile)
#
## copy time of file:
#   shutil.copy2(myfile, tmpfile)
#
## copy file dir tree, the 3rd parameter means:
##   True: symbol link
##   False: use phyical copy
#   shutil.copytree(root_of_tree, destination_dir, True)
###############################################################################

import os
import platform
import time
import getopt
import optparse
import sys
import string


###############################################################################
# get installed VS???COMNTOOLS environment:
###############################################################################
def get_vspath():
  _vspath = os.getenv('VS110COMNTOOLS')
  if not _vspath:
    _vspath = os.getenv('VS100COMNTOOLS')
    if not _vspath:
      _vspath = os.getenv('VS90COMNTOOLS')
      if not _vspath:
        _vspath = os.getenv('VS80COMNTOOLS')
        if not _vspath:
          print "VS??COMNTOOLS not found"
          sys.exit()
        else:
          print "VS80COMNTOOLS =", _vspath
      else:
        print "VS90COMNTOOLS =", _vspath
    else:
      print "VS100COMNTOOLS =", _vspath
  else:
    print "VS110COMNTOOLS =", _vspath
  return _vspath
vs_path = get_vspath() + "..\\..\\VC\\"
###############################################################################
# step (1): create a windows module definition: target_lib.def
#   MSCMD:
#     > dumpbin /EXPORTS target_lib.dll > ~target_lib.def
#   or MinGW:
#     $ pexports target_lib.dll > target_lib.def
# step (2): use this target_lib.def to create module import file: target_lib.lib
#   MSCMD:
#     > lib /def:target_lib.def /machine:amd64 /out:target_lib.lib
###############################################################################
def patchDef(fname):
	print "Patching %s"%fname
	basename=fname.split(".")[0]
	lines=open(fname).readlines()
	print lines[0]
	lines[0]="LIBRARY %s.dll\n"%basename
	print lines[0]
	fp=open(fname,"w")
	fp.write("".join(lines))
	fp.close()
	
def make_lib(dll_path,cwd_path,tgtname):
  print "[2-1] create a windows module definition: lib%s.def" % tgtname
  #dump_def = 'cd "%s" & pexports %s\%s.dll > %s.def' % (cwd_path, dll_path,tgtname, tgtname)
  def_fname="%s.def"%(tgtname)
  dll_fname="%s\%s.dll"%(dll_path, tgtname )
  dump_def = 'cd "%s" & dlltool -z %s --export-all-symbol %s' % (cwd_path, def_fname, dll_fname) 
  print dump_def
  ret = os.system(dump_def)
  patchDef("%s.def"%tgtname)
    
  if ret == 0:
    print "[2-2] use (%s.def) to create import module: %s.lib" % (tgtname, tgtname)
    lib_cmd = 'cd "%s"&lib /def:%s.def /machine:amd64 /out:%s.lib' % (cwd_path, tgtname, tgtname)
    cmds = 'cd "%s"&vcvarsall.bat x86_amd64&%s&cd "%s"' % (vs_path, lib_cmd, cwd_path)
    ret = os.system(cmds)
       
    if ret == 0:
      print "INFO: mklib (%s/%s.lib) success." % (cwd_path, tgtname)
      return 0;
    else:
      print "ERROR: mklib (%s/%s.lib) failed." % (cwd_path, tgtname)
      return (-2)
  else:
    print "ERROR: mklib (%s/%s.def) failed." % (cwd_path, tgtname)
    return (-1);

###############################################################################
# current directory:


# lib name == parent folder name
target_dll = "ERROR_dll_not_found"
def main():
	if sys.argv.__len__() == 1:
	  work_dir, target_dll = os.path.split(cwd_path)
	elif sys.argv.__len__() == 2:
	  work_dir = os.path.dirname(sys.argv[1])
	  target_dll = os.path.basename(sys.argv[1])
	else:
	  print "ERROR: invalid argument"
	  sys.exit(-1)

	if target_dll[0:3] == "lib":
	  target_dll = target_dll[3:]
	tgtname, extname = os.path.splitext(target_dll)

	if extname != ".dll":
	  tgtname = target_dll

	if work_dir == "":
	  work_dir = cwd_path

	print "working directory:", work_dir
	print "======== make import (lib%s.lib) from (lib%s.dll) ========" % \
	  (tgtname, tgtname)
	cwd_path = os.getcwd()
	genLib(cwd_path,tgtname)

def genLib(src_dir,tgtname):
	cwd_path=os.getcwd()
	#work_dir = "./"
	dll_dir=os.path.join(src_dir,"dlls")
	lib_dir=os.path.join(src_dir,"libs")
	print dll_dir
	make_lib(dll_dir,cwd_path,tgtname)
	libName=os.path.join(".","%s.lib"%tgtname)
	libName2=os.path.join(lib_dir,"%s.lib"%tgtname)
	print libName,libName2
	if os.path.exists(libName2):
		os.remove(libName2)
	os.rename(libName,libName2)
	#

if __name__=="__main__":
	main()
	sys.exit(0)
