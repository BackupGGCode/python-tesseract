import sys,os
CROSSCOMPILERPATH={}
CROSSCOMPILERPATH[32]=r"""C:\Program Files (x86)\mingw-w64\i686-4.9.0-posix-dwarf-rt_v3-rev1\mingw32\bin"""
CROSSCOMPILERPATH[64]=r"""C:\Program Files\mingw-w64\x86_64-4.9.0-posix-seh-rt_v3-rev1\mingw64\bin"""
PYTHONPATH={}
PYTHONPATH[32]="C:\Python27_%2d"%32
PYTHONPATH[64]="C:\Python27_%2d"%64

def setPath(key):
	mpaths=os.environ['PATH'].split(";")
	newPaths=[]
	for mpath in mpaths:
		if "mingw" not in mpath and 'ython' not in mpath:
			newPaths.append(mpath)
	newPaths="%s;%s;%s;%s"%(PYTHONPATH[key],'%s\\Script'%PYTHONPATH[key], CROSSCOMPILERPATH[key], ";".join(newPaths))
	return newPaths

if len(sys.argv)!=2:
	print "cmd= '%s 32/64'"%os.path.basename(__file__)
else:	
	print setPath(int(sys.argv[1]))
	
