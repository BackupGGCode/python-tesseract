import tesseract
import cv2
import cv2.cv as cv
image0=cv2.imread("eurotext.jpg")
#### you may need to thicken the border in order to make tesseract feel happy to ocr your image #####
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
while (ri):
	print ri
	word = ri.GetUTF8Text(level)
	print "word=",word
	#conf = ri.Confidence(level)
	#ri.BoundingBox(level,x1,y1,x2,y2)
	print "ri.Next(level)=",ri.Next(level)
	print ri
	ri.Next(level)
#print("word: '%s';  \tconf: %.2f; BoundingBox: %d,%d,%d,%d;\n"%
#               (word, conf, x1, y1, x2, y2))
image=None

