#!/usr/bin/env python
"""
setup.py file for SWIG
written by FreeToGo@gmail.com
"""
import sys
import os
import src.jfunc as j
osname=j.osname
argv=sys.argv

def my_uninstall():
	rmPaths=[]
	files=["*tesseract*"]
	#if osname=='darwin' and j.brew_prefix:
	for rmPath in j.sitepackagesLocations:
		print rmPath
		j.runRm4Dirs(rmPath,files)

def main():
	argLen=len(argv)
	if argLen <2 :
		print "Need at least 2 parameters not %d"%argLen
		print argv
		return
	cmd=argv[1]
	if cmd=="uninstall":
		my_uninstall()
		return
	pwd=os.path.dirname(os.path.realpath(__file__))
	srcPath=os.path.join(pwd,'src')
	os.chdir(srcPath)
	if not os.path.exists("__init__.py"):
		fp=open("__init__.py","w")
		fp.write('\n')
		fp.close()
	import src.setup,sys


	print ".........."
	src.setup.main()

	if cmd=="clean":
		os.chdir("../")
		src.setup.my_clean()
		os.system("rm python-tesseract_*")

if __name__=="__main__":
	main()
