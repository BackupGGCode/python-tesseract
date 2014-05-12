import glob, sys, os
mingwPackage="x86_64-w64-mingw32.shared"
srcBasePath="/opt/mxe/usr"
srcPath=os.path.join(srcBasePath,mingwPackage)
destPath=os.path.abspath(mingwPackage)

def getfiles(mpath,name):
	fullName=os.path.join(srcPath,mpath,name)
	files=glob.glob(fullName)
	if not files:
		print "Cannot find file with name=%s"%name
		#sys.exit()
	return files

def makeDestPath(name):
	mPath=os.path.join(destPath,name)
	if not os.path.exists(mPath):
		os.system("mkdir %s"%mPath)
	
slist=["gcc_s_seh","lept","png","jpeg","webp","tiff","stdc","tesseract","opencv","z"]
inclDirs=["tesseract","leptonica"]
fDict={}
fDict["lib"]=[]
fDict["dll"]=[]
fDict["include"]=[]
includeDirs=[]
for item in slist:
	fDict['lib']+=getfiles("lib","lib%s*.a"%item)
	fDict['dll']+=getfiles("bin","*%s*.dll"%item)
for mdir in inclDirs:
	fDict["include"]+=getfiles("include",mdir) 

destPaths=[""]+fDict.keys()
for mpath in destPaths:
	makeDestPath(mpath)
cmds=[]

for key in fDict.keys():
	for mfile in fDict[key]:
		if os.path.isdir(mfile):
			cmd="cp -Rf %s %s/%s "%(mfile,destPath,key)
		else:
			cmd="cp %s %s/%s "%(mfile,destPath,key)
		
		cmds.append(cmd)

for cmd in cmds:
	ret=os.system(cmd)
	if ret!=0:
		print cmd
		
