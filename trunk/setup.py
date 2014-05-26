#!/usr/bin/env python
"""
setup.py file for SWIG
written by FreeToGo@gmail.com
"""
import sys
import os
import src.jfunc
j=src.jfunc.jfunc()
osname=j.osname
argv=sys.argv
def setInit():
	if not os.path.exists("__init__.py"):
		fp=open("__init__.py","w")
		fp.write('\n')
		fp.close()

def main():
	argLen=len(argv)
	if argLen <2 :
		print("Need at least 2 parameters not %d"%argLen)
		print(argv)
		return
	cmd=argv[1]
	pwd=os.path.dirname(os.path.realpath(__file__))
	srcPath=os.path.join(pwd,'src')
	os.chdir(srcPath)
	setInit()
	import src.setup,sys
	if cmd=="uninstall":
		src.setup.my_uninstall()
		return
	print("..........")
	if cmd=="clean":
		os.chdir("../")
		src.setup.my_clean()
		j.remove("python-tesseract_*")
		print("*"*100,os.getcwd)
		j.remove("*.deb")
		
	src.setup.main()
if __name__=="__main__":
	main()
