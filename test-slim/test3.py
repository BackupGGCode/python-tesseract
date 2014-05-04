import cv2.cv as cv
import tesseract

api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)

image=cv.LoadImage("eurotext.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
tesseract.SetCvImage(image,api)
text=api.GetUTF8Text()
conf=api.MeanTextConf()
print text,len(text)
print "Cofidence Level: %d %%"%conf
print "Confidences of All word"
confOfText=api.AllWordConfidences()
confOfText=tesseract.intArray_frompointer(confOfText)
for i in range(len(text)):
	print i,confOfText[i]
