import sys,pickle,os
vspath = os.getenv('VS90COMNTOOLS')+ "..\\..\\VC"
osSetVSEnviron="cd %s & vcvarsall.bat x86_amd64"%vspath
def runCmd(cmdStr):
	cmdStr="%s & %s"%(osSetVSEnviron,cmdStr)
	print cmdStr
	ret=os.system(cmdStr)
	if ret!=0:
		print "fatal error!"
		print cmdStr
		sys.exit(-1)

def genDumpDef(dllFile, defFile):
	runCmd("dumpbin %s /exports > %s"%(dllFile, defFile))

def genLib(defFile,libFile):
	runCmd("lib /def:%s /machine:amd64 /out:%s"%(defFile,libFile))

def convertDef(dumpDefFile,pexportDefFile):
	newlines=[]
	lines=open(dumpDefFile).readlines()
	dumpLine=lines[4]
	print dumpLine
	dumpList=dumpLine.strip().split(" ")
	if  " ".join(dumpList[:-1]) != "Dump of file":
		print "fatal Error!"
		print "Can't read dump file name:",dumpLine
		sys.exit(-1)
	fname=dumpList[-1].split("\\")
	header="LIBRARY %s"%fname[-1]
	print header
	newlines.append(header)
	newlines.append("EXPORTS")
	for line in lines[19:]:
		items=line.split()
		if len(items)<4:
			break
		#print items[3]
		newlines.append(items[3])
	fp2=open(pexportDefFile,"w")
	fp2.writelines("\n".join(newlines))
	fp2.close()
	
def genLibFromName(x64Path, name):
	dllPath=os.path.join(x64Path,"dlls")
	libPath=os.path.join(x64Path,"libs")
	dllFile=os.path.join(dllPath,name+".dll")
	libFile=os.path.join(libPath,name+".lib")
	defDumpFile=os.path.abspath(name+".def_dump")
	defFile=os.path.abspath(name+".def")
	genDumpDef(dllFile,defDumpFile)
	convertDef(defDumpFile,defFile)
	genLib(defFile,libFile)
	
if __name__=="__main__":
	x64Path=os.path.abspath(r"..\\mingw\x64")
	names=["libtesseract-3","liblept-4","opencv_core249_vc90"]
	for name in names:
		genLibFromName(x64Path,name)
