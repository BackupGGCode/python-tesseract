import struct,sys,glob, os, subprocess
arch=8 * struct.calcsize("P")
print(sys.executable, arch)

def getMingwPaths():
	mingwPaths={}
	mingwPaths[32]=[]
	mingwPaths[64]=[]
	mdirs=sorted(glob.glob(r'c:\Program Files*\mingw-w64\*\mingw*\bin'))
	for mdir in mdirs:
		if "mingw32" in mdir:
			mingwPaths[32].append(mdir)
		elif "mingw64" in mdir:
			mingwPaths[64].append(mdir)
	return mingwPaths

def setEnviron(mdirs):
	oldPath=os.environ["PATH"]
	os.environ["PATH"]=""
	for mdir in mdirs:
		os.environ["PATH"]+=os.pathsep+mdir
	os.environ["PATH"]+=os.pathsep+oldPath

mingwPaths=getMingwPaths()
print(mingwPaths)
if len(mingwPaths[arch])==0:
	prints("Can't find MingwPath for python %d"%arch)
	sys.exit()
mingwBinPath=mingwPaths[arch][-1]
pythonExe=sys.executable
mypaths=[mingwBinPath]+sys.path+["c:\swig","c:\cygwin64\bin"]
setEnviron(mypaths)
print os.environ['PATH']
cmdList=[]
for param in ["clean", "build", "install"]:
	cmd="%s setup.py %s"%(pythonExe,param)
	print(cmd)
	process1 = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)        
	print process1.communicate()[0]
	

