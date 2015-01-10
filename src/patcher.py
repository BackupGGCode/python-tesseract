import os,collections,sys
class patcher:
	def __init__(self,incName,incFile,keywords):

		self.fName=incFile
		self.fMinName="%s_mini.h"%incFile[:-2]
		self.incName=incName
		self.keywords=keywords
		self.lines=self.getLines(self.fName,incName)
		self.patching()
	def getLines(self, fName,incName):
		mPaths=["/usr","/usr/local","/opt","/opt/local"]
		fullNames=[os.path.join(mPath,"include",incName,fName) for mPath in mPaths]
		#print fullNames
		for fullName in fullNames:
			if not os.path.exists(fullName):
				continue
			lines=open(fullName).read().split(";")
			return lines

	def lineParser(self,line,keywords):
		if "include" in line:
			KEYWORD_FOUND=None
			return line
		for s in keywords:
			if s not in line:
				continue
			head=[]
			slines=line.split("\n")
			for j,sline in enumerate(slines):
				if s not in sline:
					head.append(sline)
				else:
					headStr="\n".join(head)
					tailStr="\n"+"\n".join(slines[j:])
					KEYWORD_FOUND=s
					return s, headStr, tailStr
		return line

	def patching(self):
		fMinName,lines,keywords=self.fMinName,self.lines,self.keywords
		if not lines:
			print("%s not existed"%self.fName)
			print("Have you installed %s?"%self.incName)
			sys.exit()
		newLines=[]
		COMMENT_ON=False

		for i,line in enumerate(lines):
			ret=self.lineParser(line,keywords)
			if isinstance(ret,basestring):
				line=ret
				KEYWORD_FOUND=None
			else:
				#print ret
				s, headStr, line=ret
				if len(headStr.strip())!=0 :
					newLines.append(headStr)
				KEYWORD_FOUND=True

			if ( COMMENT_ON or KEYWORD_FOUND) :
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

			#line=line.strip()
			#if len(line)!=0:
			if len(line.strip())!=0 :
				newLines.append(line)
		header='#include "config.h"'
		fp=open(fMinName,"w")
		fp.write("%s\n%s"%(header,";".join(newLines)))
		fp.close()

def patchAll(patchDict):
	for key,value in patchDict.items():
		if not value:
			continue
		incName,incFile=key.split(":")
		patcher(incName,incFile,value)

def genSwigI(patchDict):
	lines=open("tesseract.i.template").readlines()
	a=[]
	b=[]
	for key,value in patchDict.items():
		incName,incFile=key.split(":")
		a.append('#include "%s"\n'%incFile)
		if value:
			b.append('%%include "%s_mini.h"\n'%incFile[:-2])
		else:
			b.append('%%include "%s"\n'%incFile)
	lines+=['\n%{\n']+a+['\n%}\n\n']
	lines+=['\n']+b+['\n']
	fp=open("tesseract.i","w")
	fp.write(''.join(lines))
	fp.close()


def run():
	patchDict=collections.OrderedDict([
			#(":config.h",None),
			("leptonica:allheaders.h",["setPixMemoryManager"]),
			("leptonica:pix.h",None),
			("tesseract:publictypes.h",["char* kPolyBlockNames"]),
			("tesseract:baseapi.h",["Dict", "ImageThresholder","iterator"]),
			("tesseract:capi.h",["TessBaseAPIInit(","TessBaseAPISetFillLatticeFunc"]),
			("tesseract:pageiterator.h",None),
			("tesseract:ltrresultiterator.h",["ChoiceIterator"]),
			("tesseract:thresholder.h",None),
			("tesseract:resultiterator.h",None),
			("tesseract:renderer.h",None),
			(":main.h",None),
			])
	patchAll(patchDict)
	genSwigI(patchDict)


if __name__=="__main__":
	run()
