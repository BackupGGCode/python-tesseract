import collections,os,sys
PYTHON3=True if sys.version_info >= (3,0) else False

def isKeywordsInStr(keywords,mstr):
	if keywords is None:
		return False
	for keyword in keywords:
		if keyword in mstr:
			return True
	return False
		
def commentingLines(lines,keywords):
	COMMENTING=0
	numOfOpenBracket=0
	lines2=[]
	for line in lines:
		line=line.strip()
		line0=line
		if line[:2] in ["* ","/*"] or line[-2:] in ["*/"] or (len(line)>2 and "//"==line[:2]) :
			lines2.append(line+"\n")
			continue
		HAS_KEYWORDS=isKeywordsInStr(keywords,line)
		if COMMENTING>0 or HAS_KEYWORDS:
			if "{" in line:
				numOfOpenBracket+=1
		if COMMENTING>0 or numOfOpenBracket>0 :
			if "}" in line:
				if numOfOpenBracket>0:
					numOfOpenBracket-=1
					COMMENTING+=100
				else:
					COMMENTING=0
				line+="\t//..<<numof()=%d>><<COMMENTING=%d>>\t"%(numOfOpenBracket,COMMENTING)
		
		if numOfOpenBracket>0 or COMMENTING>0  or HAS_KEYWORDS:
			if not isKeywordsInStr(["#ifdef",'#ifndef',"#endif"],line):
				line="//..__<<numof()=%d>><<COMMENTING=%d>>\t"%(numOfOpenBracket,COMMENTING)+line
		else:
			if numOfOpenBracket>0 or COMMENTING>0:
				line+="//..<<numof()=%d>><<COMMENTING=%d>>\t"%(numOfOpenBracket,COMMENTING)
		line2=line0
		if "//" in line:
			line2=line0.split("//")[0].strip()
			print(line2)
			print(line)
		if HAS_KEYWORDS:
			if "#include" == line2.strip()[:8] or "#define" ==line2.strip()[:7] or (line2!="" and line2[-1]==";") or (line2!="" and line2[-1] in ["\\",")"]):
				COMMENTING=0
			else:
				COMMENTING=10000
				line+="//................<%s>%s"%(line2,line)
		elif numOfOpenBracket<0:
			COMMENTING=0
			numOfOpenBracket=0
		elif line2!="":
			if (len(line2)>1 and line2[-2:]=="*/"):
				COMMENTING=0
				numOfOpenBracket=0
			elif numOfOpenBracket==0  and line2[-1]==";":
				COMMENTING=0
				numOfOpenBracket=0
			elif numOfOpenBracket>0 and line2[-1] in [",",")"]:
				COMMENTING+=1000
				line+="//................................."
			elif numOfOpenBracket>0 or COMMENTING>0:
				COMMENTING+=1
	
		lines2.append(line+"\n")
	return lines2

def getLines(mdir,mfile):
	mPaths=["/usr","/usr/local","/opt","/opt/local"]
	fullNames=[os.path.join(mPath,"include",mdir,mfile) for mPath in mPaths]
	#print fullNames
	for fullName in fullNames:
		if not os.path.exists(fullName):
			continue
		lines=open(fullName).readlines()
		return lines

def genSwigI(patchDict):
	lines=open("tesseract.i.template").readlines()
	defines=[	"#define TESS_API\n",
				"#define TESS_LOCAL\n",
				"#define LEPT_DLL\n"]
	if not PYTHON3:
		defines.append("#define TESS_CAPI_INCLUDE_BASEAPI\n")
	a=list(defines)
	b=list(defines)
	for key,value in list(patchDict.items()):
		incName,incFile=key.split(":")
		
		if value:
			b.append('%%include "%s_mini.h"\n'%incFile[:-2])
			a.append('#include "%s_mini.h"\n'%incFile[:-2])
			#b.append('%%include "%s"\n'%incFile)
			#a.append('#include "%s"\n'%incFile)
		else:
			b.append('%%include "%s"\n'%incFile)
			a.append('#include "%s"\n'%incFile)
	a.append('#include "%s"\n'%"main.h")
	b.append('%%include "%s"\n'%"main.h")
	lines+=['\n%{\n']+a+['\n%}\n\n']
	lines+=['\n']+b+['\n']
	fp=open("tesseract.i","w")
	fp.write(''.join(lines))
	fp.close()



def run(tess_version):
	if PYTHON3:		
		patchDict=collections.OrderedDict([
			#(":config.h",None),
			("leptonica:allheaders.h",["setPixMemoryManager"]),
			("leptonica:pix.h",None),
			("tesseract:publictypes.h",["char* kPolyBlockNames","PSM_","PT_","ORIENTATION_","TEXTLINE_","WRITING_","RIL_"]),
			("tesseract:baseapi.h",["Dict", "ImageThresholder","ProbabilityInContextFunc","GetUTF8Text"]),
			("tesseract:capi.h",["TessBaseAPIInit","TessBaseAPISetFillLatticeFunc","OEM_"]),
			("tesseract:pageiterator.h",None),
			("tesseract:ltrresultiterator.h",["ChoiceIterator"]),
			("tesseract:thresholder.h",None),
			("tesseract:resultiterator.h",None),
			("tesseract:renderer.h",None),
			#(":main.h",None),
			])
	else:
		patchDict=collections.OrderedDict([
			#(":config.h",None),
			("leptonica:allheaders.h",["setPixMemoryManager"]),
			("leptonica:pix.h",None),
			("tesseract:publictypes.h",["char* kPolyBlockNames"]),
			("tesseract:baseapi.h",["Dict", "ImageThresholder","ProbabilityInContextFunc","GetUTF8Text"]),
			("tesseract:capi.h",["TessBaseAPIInit","TessBaseAPISetFillLatticeFunc","TessDictFunc","TessProbabilityInContextFunc"]),
			("tesseract:pageiterator.h",None),
			("tesseract:ltrresultiterator.h",["ChoiceIterator"]),
			("tesseract:thresholder.h",None),
			("tesseract:resultiterator.h",None),
			("tesseract:renderer.h",None),
			#(":main.h",None),
			])
		if tess_version<"3.03":
			patchDict["tesseract:publictypes.h"].append("PageIterator")
			patchDict["tesseract:baseapi.h"]+=["iterator","PageIterator","GetLastInitLanguage"]
			patchDict["tesseract:ltrresultiterator.h"].append("PageIterator")
			del patchDict["tesseract:pageiterator.h"]
			del patchDict["tesseract:resultiterator.h"]
			
	for mfile, commentedKeys in list(patchDict.items()):
		print(mfile, commentedKeys)
		mdir,mfile=mfile.split(":")
		lines=getLines(mdir,mfile)
		#print lines
		lines=commentingLines(lines,commentedKeys)
			
		#fp=open(mfile,"w")
		fp=open("%s_mini.h"%mfile[:-2],"w")
		fp.write("".join(lines))
		fp.close()
	genSwigI(patchDict)
	
if __name__=="__main__":
	run("3.0.2")
	#lines="""LEPT_DLL extern void setPixMemoryManager ( void * (  ( *allocator ) ( size_t ) ), void  (  ( *deallocator ) ( void * ) ) );
#LEPT_DLL extern PIX * pixCreate ( l_int32 width, l_int32 height, l_int32 depth );
#LEPT_DLL extern PIX * pixCreateNoInit ( l_int32 width, l_int32 height, l_int32 depth );""".split("\n")
	#print commentingLines(lines,["setPixMemoryManager"])
	
	
	
