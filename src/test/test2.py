import cv2.cv as cv
import tesseract

image=cv.LoadImage("eurotext.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)

api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
#api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
api.SetPageSegMode(tesseract.PSM_AUTO)
tesseract.SetCvImage(image,api)
text=api.GetUTF8Text()
conf=api.MeanTextConf()
image=None
print text
print conf
