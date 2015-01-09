import os
class patcher:
	def __init__(self,baseFile,incName,keywords):
		self.fName="%s.h"%baseFile
		self.fMinName="%s_mini.h"%baseFile
		self.incName=incName
		self.keywords=keywords
		self.lines=self.getLines(self.fName,incName)
		self.patching()
	def getLines(self, fName,incName):
		mPath=os.path.join("/","usr","include",incName)
		fullName=os.path.join(mPath,fName)
		lines=open(fullName).read().split(";")
		return lines
	def patching(self):
		fMinName,lines,keywords=self.fMinName,self.lines,self.keywords 
		newLines=[]
		COMMENT_ON=False
		for line in lines:
			if  any( s in line for s in keywords) or COMMENT_ON:
				if "{" in line:
					COMMENT_ON=True
				if "}" in line:
					COMMENT_ON=False
					slines=line.split("}")
					head=slines[0].replace("\n","\n//")
					tail=slines[1:]
					line="}".join([head]+tail)
				else:
					line=line.replace("\n","\n//")
			newLines.append(line)
		header='#include "config.h"'
		fp=open(fMinName,"w")
		fp.write("%s\n%s"%(header,";".join(newLines)))
		fp.close()

def patchBaseAPI():
	keywords=["Dict", "ImageThresholder"]
	baseFiles=["baseapi"]
	baseFile=baseFiles[0]
	mPath="/usr/include/tesseract"
	patcher(baseFile,mPath,keywords)

def patchAllHeaders():
	keywords=["setPixMemoryManager"]
	patcher("allheaders","leptonica", keywords)
	
if __name__=="__main__":
	patchAllHeaders()
	patchBaseAPI()
