import tesseract
import re
from string import punctuation
from distutils.sysconfig import get_config_vars
import commands,platform,os


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
	print "%s %s %s"%(stars,mstr,stars)

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
	import cv2.cv as cv
	api = tesseract.TessBaseAPI()
	api.Init(".","eng",tesseract.OEM_DEFAULT)
	api.SetPageSegMode(tesseract.PSM_AUTO)

	image=cv.LoadImage("eurotext.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
	tesseract.SetCvImage(image,api)
	text=api.GetUTF8Text()
	conf=api.MeanTextConf()
	print text,len(text)
	print "Cofidence Level: %d %%"%conf
	print "Confidences of All words"
	header("Method 1","*"*10)
	confOfText=api.AllWordConfidences()

	print confOfText
	print "Number of Words:"
	print "counted by tesseract: %d"%len(confOfText) 
	print "counted by me: %d[%d]"%(countWords(text), countWords2(text))
	if len(confOfText)!=countWords(text):
		print "Why the words counted by tesseract are different from mine!!!!"
	header("Method 2","*"*10)
	confs=tesseract.AllWordConfidences(api)
	print confs, len(confs)


def setEnvironmentDarwin():
	brew_prefix=commands.getstatusoutput('brew --prefix')[1]
	if not brew_prefix:
		return 
	print "homebrew installed"
	opencv_version=commands.getstatusoutput('brew ls --versions opencv')[1]
	if not opencv_version:
		print "please install opencv by \n'brew install homebrew/science/opencv'"
	else:
		print "your opencv version is %s"%opencv_version
	python_version=commands.getstatusoutput('python --version')[1].split(" ")[1]
	python_version="python"+".".join(python_version.split(".")[:-1])
	print python_version		
	PYTHONPATH=os.path.join(brew_prefix,"lib",python_version,"site-packages")
	print PYTHONPATH
	bashrc_fname=os.path.expanduser("~/.bashrc")
	bashrc_lines=open(bashrc_fname).read()
	if os.environ['PYTHONPATH'] not in bashrc_lines :
		fp=open(bashrc_fname,"a")
		fp.write("\nexport PYTHONPATH=%s\n"%os.environ['PYTHONPATH'])
		fp.close()
	if 'PYTHONPATH' not in os.environ :
		return 
	if PYTHONPATH not in os.environ['PYTHONPATH']:
		os.environ['PYTHONPATH']=" ".join(PYTHONPATH,os.environ['PYTHONPATH'])
		print os.environ['PYTHONPATH']



if __name__=="__main__":
	osname=platform.uname()[0].lower()
	if osname=='darwin':
		setEnvironmentDarwin()
	
