# Code Snippets #

Example 1
```
import cv2.cv as cv
import tesseract

image=cv.LoadImage("foo.png", cv.CV_LOAD_IMAGE_GRAYSCALE)

api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
#api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
api.SetPageSegMode(tesseract.PSM_AUTO)
tesseract.SetCvImage(image,api)
text=api.GetUTF8Text()
conf=api.MeanTextConf()
print text
```


Example 2
```
import tesseract
api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetVariable("tessedit_char_whitelist", "0123456789abcdefghijklmnopqrstuvwxyz")
api.SetPageSegMode(tesseract.PSM_AUTO)

mImgFile = "eurotext.jpg"
mBuffer=open(mImgFile,"rb").read()
result = tesseract.ProcessPagesBuffer(mBuffer,len(mBuffer),api)
print "result(ProcessPagesBuffer)=",result
intPtr=api.AllWordConfidences()
print str(intPtr)
pyPtrRaw=tesseract.cdata(intPtr,300)
print len(pyPtrRaw),len(mBuffer)
pyPtr=[ord(data) for i,data in enumerate(pyPtrRaw)]
print pyPtr
tesseract.delete_intp(intPtr) 
```

Example 3
**How to get confidences of each word by AllWordConfidences**

```
import cv2.cv as cv
import tesseract
import re
from string import punctuation
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
```
Example 4
