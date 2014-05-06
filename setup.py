#!/usr/bin/env python
"""
setup.py file for SWIG
written by FreeToGo@gmail.com
"""
import os

pwd=os.path.dirname(os.path.realpath(__file__))
srcPath=os.path.join(pwd,'src')
os.chdir(srcPath)

if not os.path.exists("__init__.py"):
	fp=open("__init__.py","w")
	fp.write('\n')
	fp.close()
import src.setup,sys


src.setup.main()
if len(sys.argv)==2 and sys.argv[1]=="clean":
	os.chdir("../")
	src.setup.my_clean()
	
