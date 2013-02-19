import cv2.cv as cv
import tesseract

image=cv.LoadImage("eurotext.jpg")

api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
#api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
api.SetPageSegMode(tesseract.PSM_AUTO)
tesseract.SetCvImage(image,api)
text=api.GetUTF8Text()
conf=api.MeanTextConf()
print text
print conf

