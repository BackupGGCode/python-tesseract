# Python3-Tesseract Examples #

Although python3-opencv is not ready, I still decide to go ahead to build python3-tesseract first.

## the download link ##

[Download ](https://bitbucket.org/3togo/python-tesseract/downloads)

## Test1 ##
```
#!/usr/bin/env python
import tesseract
api = tesseract.TessBaseAPI()
api.SetOutputName("outputName");
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
mImgFile = "eurotext.jpg"
pixImage=tesseract.pixRead(mImgFile)
api.SetImage(pixImage)
outText=api.GetUTF8Text()
print(("OCR output:\n%s"%outText));
api.End()
outText=None
pixImage=None
```
## Test2 ##
```
#!/usr/bin/env python
import tesseract
import gc, pprint

api = tesseract.TessBaseAPI()
api.SetOutputName("outputName");
#api.Init(".","eng")
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
mImgFile = "eurotext.jpg"

print("Test ProcessPagesWrapper")
result = tesseract.ProcessPagesWrapper(mImgFile,api)
print("result(ProcessPagesWrapper)=",result)

print("Test ProcessPagesFileStream")
result = tesseract.ProcessPagesFileStream(mImgFile,api)
print("result(ProcessPagesFileStream)=",result)

print("Test ProcessPagesRaw")
result = tesseract.ProcessPagesRaw(mImgFile,api)
print("result(ProcessPagesRaw)",result)

for r in gc.get_referents(api):
    pprint.pprint(r)
n = gc.collect()
print('Unreachable objects:', n)
print('Remaining Garbage:', end=' ')
pprint.pprint(gc.garbage)
print()
api.End()

```

## Test 3 ##
```
import tesseract
api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
mImgFile = "eurotext.jpg"
pixImage=tesseract.pixRead(mImgFile)
api.SetImage(pixImage)
api.Recognize(None)
ri=api.GetIterator()
level=tesseract.RIL_WORD
count=0
while (ri):
	word = ri.GetUTF8Text(level)
	conf = ri.Confidence(level)
	print("[%03d]:\tword(confidence)=%s(%.2f%%)"%(count,word,conf))
	#ri.BoundingBox(level,x1,y1,x2,y2)
	count+=1
	if not ri.Next(level):
		break
pixImage=None
api.End()

```
## Test 4 ##
```
#!/usr/bin/env python
import os, tesseract
lang = "eng"
filename = "eurotext.jpg"
TESSDATA_PREFIX = "."
tesseract_version = tesseract.TessVersion()
api = tesseract.TessBaseAPICreate()
rc = tesseract.TessBaseAPIInit3(api, TESSDATA_PREFIX, lang)
if (rc):
    tesseract.TessBaseAPIDelete(api)
    print("Could not initialize tesseract.\n")
    exit(3)
print('Tesseract-ocr version', tesseract_version)
text_out = tesseract.TessBaseAPIProcessPages(api, filename, None, 0)
print(text_out)
```
## Test 5 ##
```
import tesseract
import re
from string import punctuation
from distutils.sysconfig import get_config_vars
import subprocess,platform,os


def removeFlag(flagName,mflag):
	(opt,) = get_config_vars(mflag)
	os.environ[mflag] = " ".join(
		flag for flag in opt.split() if flag != flagName
		)
def addFlag(flagName,mflag):
	(opt,) = get_config_vars(mflag)
	os.environ[mflag] = flagName.join(
		flag for flag in opt.split() 
		)
def header(mstr,stars):
	print("%s %s %s"%(stars,mstr,stars))

def countWords(strs):
	r = re.compile(r'[{}]'.format(punctuation))
	new_strs = r.sub(' ',strs)
	return len(new_strs.split())

def countWords2(strs):
	strs=strs.strip()
	words=re.split(r'[^0-9A-Za-z]+',strs)
	#print words
	return len(words)


def ocr():
	api = tesseract.TessBaseAPI()
	api.Init(".","eng",tesseract.OEM_DEFAULT)
	api.SetPageSegMode(tesseract.PSM_AUTO)

	mImgFile = "eurotext.jpg"
	pixImage=tesseract.pixRead(mImgFile)
	api.SetImage(pixImage)
	text=api.GetUTF8Text()
	conf=api.MeanTextConf()
	print(text,len(text))
	print("Cofidence Level: %d %%"%conf)
	print("Confidences of All words")
	header("Method 1","*"*10)
	confOfText=api.AllWordConfidences()

	print(confOfText)
	print("Number of Words:")
	print("counted by tesseract: %d"%len(confOfText)) 
	print("counted by me: %d[%d]"%(countWords(text), countWords2(text)))
	if len(confOfText)!=countWords(text):
		print("Why the words counted by tesseract are different from mine!!!!")
	header("Method 2","*"*10)
	confs=tesseract.AllWordConfidences(api)
	print(confs, len(confs))


def setEnvironmentDarwin():
	brew_prefix=subprocess.getstatusoutput('brew --prefix')[1]
	if not brew_prefix:
		return 
	print("homebrew installed")
	opencv_version=subprocess.getstatusoutput('brew ls --versions opencv')[1]
	if not opencv_version:
		print("please install opencv by \n'brew install homebrew/science/opencv'")
	else:
		print("your opencv version is %s"%opencv_version)
	python_version=subprocess.getstatusoutput('python --version')[1].split(" ")[1]
	python_version="python"+".".join(python_version.split(".")[:-1])
	print(python_version)		
	PYTHONPATH=os.path.join(brew_prefix,"lib",python_version,"site-packages")
	print(PYTHONPATH)
	bashrc_fname=os.path.expanduser("~/.bashrc")
	bashrc_lines=open(bashrc_fname).read()
	if 'PYTHONPATH' not in os.environ :
		os.environ['PYTHONPATH']=PYTHONPATH
		print(os.environ['PYTHONPATH'])
		
	if os.environ['PYTHONPATH'] not in bashrc_lines :
		fp=open(bashrc_fname,"a")
		fp.write("\nexport PYTHONPATH=%s\n"%os.environ['PYTHONPATH'])
		fp.close()
	
	if PYTHONPATH not in os.environ['PYTHONPATH']:
		os.environ['PYTHONPATH']=" ".join(PYTHONPATH,os.environ['PYTHONPATH'])
		print(os.environ['PYTHONPATH'])



if __name__=="__main__":
	osname=platform.uname()[0].lower()
	if osname=='darwin':
		setEnvironmentDarwin()
	ocr()

```