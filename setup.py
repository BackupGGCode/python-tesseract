#!/usr/bin/env python
"""
setup.py file for SWIG
written by FreeToGo@gmail.com
"""
import os
import src.setup,sys
print "&"*200
print "runtime directory:",os.path.dirname(os.path.realpath(__file__))

os.chdir("src")
src.setup.main()
if len(sys.argv)==2 and sys.argv[1]=="clean":
	os.chdir("../")
	src.setup.my_clean()
	
