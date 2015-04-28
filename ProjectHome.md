[![](http://python-tesseract.googlecode.com/files/sf_coffee_small.jpg)](https://www.paypal.com/cgi-bin/webscr?cmd=_cart&business=VD2Y4PZSK7T86&lc=HK&item_name=To%20support%20the%20development%20of%20python%2dtesseract&amount=5%2e00&currency_code=USD&button_subtype=products&add=1&bn=PP%2dShopCartBF%3abtn_cart_LG%2egif%3aNonHosted)     [If you find python-tesseract useful, please consider ](https://www.paypal.com/cgi-bin/webscr?cmd=_cart&business=VD2Y4PZSK7T86&lc=HK&item_name=To%20support%20the%20development%20of%20python%2dtesseract&amount=5%2e00&currency_code=USKD&button_subtype=products&add=1&bn=PP%2dShopCartBF%3abtn_cart_LG%2egif%3aNonHosted)**_[buying me a coffee.](https://www.paypal.com/cgi-bin/webscr?cmd=_cart&business=VD2Y4PZSK7T86&lc=HK&item_name=To%20support%20the%20development%20of%20python%2dtesseract&amount=5%2e00&currency_code=USKD&button_subtype=products&add=1&bn=PP%2dShopCartBF%3abtn_cart_LG%2egif%3aNonHosted)_**


# Beta Testing #
[Python3-Tesseract Beta Testing](https://code.google.com/p/python-tesseract/wiki/Python3Tesseract)
# Downloads #
## [Downloads Page in BitBucket](https://bitbucket.org/3togo/python-tesseract/downloads) ##
===_version 0.9 adds support to ResultIterator and AllWordConfidences()===__see example 4 below__####_For details, please refer to [example 3](https://code.google.com/p/python-tesseract/wiki/CodeSnippets) in wiki-codesnippets_####
remember to install opencv and numpy_
###  ###
Ubuntu Trusty x64 -[python-tesseract\_0.9-0.5ubuntu0\_amd64.deb](https://bitbucket.org/3togo/python-tesseract/downloads)

Windows 7  x64 -[python-tesseract-0.9-0.4.win-amd64-py2.7.exe](https://bitbucket.org/3togo/python-tesseract/downloads/python-tesseract-0.9-0.4.win-amd64-py2.7.exe)_<-thanks to Max Pole & Dustin Spicuzza_
### **remember to put tessdata in the same path with your python program!!** ###
Windows 7  x86 [python-tesseract-0.9-0.4.win32-py2.7.exe](https://bitbucket.org/3togo/python-tesseract/downloads/python-tesseract-0.9-0.3.win32-py2.7.exe)

Mac 10.10 (Homebrew)

For details, refer to the [wiki](https://code.google.com/p/python-tesseract/wiki/HowToCompileForHomebrewMac) page.
```
easy_install https://bitbucket.org/3togo/python-tesseract/downloads/python_tesseract-0.9.1-py2.7-macosx-10.10-x86_64.egg
```
# Python Wrapper Class for Tesseract #
## (Linux & Mac OS X & Windows) ##
Python-tesseract is a wrapper class for Tesseract OCR that allows any conventional image files (JPG, GIF ,PNG , TIFF and etc) to be read and decoded into readable languages. No temporary file will be created during the OCR processing.

**Windows versions are available now!**

&lt;BR&gt;


_remember to_

&lt;BR&gt;


1. set PATH:     e.g. PATH=%PATH%;C:\PYTHON27 [Details](http://pythoncentral.org/how-to-install-python-2-7-on-windows-7-python-is-not-recognized-as-an-internal-or-external-command/)

&lt;BR&gt;


2. set c:\python27\python.exe to be compatible to**Windows 7**_even though you are using windows 7. Otherwise the program might **crash** during runtime [Details](http://python-tesseract.googlecode.com/files/pythonCompatible.png)_

&lt;BR&gt;


3. _Download and install all of them_

&lt;BR&gt;


[python-opencv](http://www.lfd.uci.edu/~gohlke/pythonlibs/v92kqh5j/opencv-python-2.4.9.win32-py2.7.exe)
[numpy](http://www.lfd.uci.edu/~gohlke/pythonlibs/v92kqh5j/numpy-MKL-1.8.1.win32-py2.7.exe)

&lt;BR&gt;


4. unzip the sample code and keep your fingers crossed
[Sample Codes](http://python-tesseract.googlecode.com/files/test-slim.7z)

&lt;BR&gt;


5. python -u test.py 

&lt;BR&gt;


it is always safer to run python in unbuffered mode especially for windows XP


&lt;BR&gt;


**Example 1:**
```
import tesseract
api = tesseract.TessBaseAPI()
api.SetOutputName("outputName");
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
mImgFile = "eurotext.jpg"
pixImage=tesseract.pixRead(mImgFile)
api.SetImage(pixImage)
outText=api.GetUTF8Text()
print("OCR output:\n%s"%outText);
api.End()
```
**Example 2:**
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
api.End()
```
**Example 3:**
```
import cv2.cv as cv
import tesseract

api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)

image=cv.LoadImage("eurotext.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
tesseract.SetCvImage(image,api)
text=api.GetUTF8Text()
conf=api.MeanTextConf()
print text
api.End()
```

**Example 4:**
```
import tesseract
import cv2
import cv2.cv as cv

image0=cv2.imread("p.bmp")
#### you may need to thicken the border in order to make tesseract feel happy to ocr your image #####
offset=20
height,width,channel = image0.shape
image1=cv2.copyMakeBorder(image0,offset,offset,offset,offset,cv2.BORDER_CONSTANT,value=(255,255,255)) 
#cv2.namedWindow("Test")
#cv2.imshow("Test", image1)
#cv2.waitKey(0)
#cv2.destroyWindow("Test")
#####################################################################################################
api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
height1,width1,channel1=image1.shape
print image1.shape
print image1.dtype.itemsize
width_step = width*image1.dtype.itemsize
print width_step
#method 1 
iplimage = cv.CreateImageHeader((width1,height1), cv.IPL_DEPTH_8U, channel1)
cv.SetData(iplimage, image1.tostring(),image1.dtype.itemsize * channel1 * (width1))
tesseract.SetCvImage(iplimage,api)

text=api.GetUTF8Text()
conf=api.MeanTextConf()
image=None
print "..............."
print "Ocred Text: %s"%text
print "Cofidence Level: %d %%"%conf

#method 2:
cvmat_image=cv.fromarray(image1)
iplimage =cv.GetImage(cvmat_image)
print iplimage

tesseract.SetCvImage(iplimage,api)
#api.SetImage(m_any,width,height,channel1)
text=api.GetUTF8Text()
conf=api.MeanTextConf()
image=None
print "..............."
print "Ocred Text: %s"%text
print "Cofidence Level: %d %%"%conf
api.End()
```
**Example 6:**
```
import tesseract
import cv2
import cv2.cv as cv
image0=cv2.imread("eurotext.jpg")
offset=20
height,width,channel = image0.shape
image1=cv2.copyMakeBorder(image0,offset,offset,offset,offset,cv2.BORDER_CONSTANT,value=(255,255,255))

api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
height1,width1,channel1=image1.shape
print image1.shape
print image1.dtype.itemsize
width_step = width*image1.dtype.itemsize
print width_step

iplimage = cv.CreateImageHeader((width1,height1), cv.IPL_DEPTH_8U, channel1)
cv.SetData(iplimage, image1.tostring(),image1.dtype.itemsize * channel1 * (width1))
tesseract.SetCvImage(iplimage,api)
api.Recognize(None)
ri=api.GetIterator()
level=tesseract.RIL_WORD
count=0
while (ri):
	word = ri.GetUTF8Text(level)
	conf = ri.Confidence(level)
	print "[%03d]:\tword(confidence)=%s(%.2f%%)"%(count,word,conf)
	#ri.BoundingBox(level,x1,y1,x2,y2)
	count+=1
	if not ri.Next(level):
		break

iplimage=None
api.End()
```
[p.bmp](https://python-tesseract.googlecode.com/files/p.bmp)

[More Examples](http://code.google.com/p/python-tesseract/wiki/CodeSnippets)

[Sample Codes](http://python-tesseract.googlecode.com/files/test-slim.7z)