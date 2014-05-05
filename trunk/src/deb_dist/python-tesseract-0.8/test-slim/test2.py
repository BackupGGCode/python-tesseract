import tesseract
import cv2
import cv2.cv as cv

#image0=cv.LoadImage("p.bmp", cv.CV_LOAD_IMAGE_UNCHANGED )     #cv.CV_LOAD_IMAGE_UNCHANGED // cv.CV_LOAD_IMAGE_GRAYSCALE
image0=cv2.imread("eurotext.jpg")
print image0
print image0.shape
#### you may need to thicken the border in order to make tesseract feel happy to ocr your image #####
offset=20
IPL_BORDER_REPLICATE=1
IPL_BORDER_CONSTANT=0

height,width,channel = image0.shape
#image=cv2.createImage((cols+offset*2, rows+offset*2), cv.IPL_DEPTH_8U, 3 ) 
#image=cv.CreateImage((image0.width+offset*2, image0.height+offset*2), cv.IPL_DEPTH_8U, 3 ) 
image1=image0
image1=cv2.copyMakeBorder(image0,offset,offset,offset,offset,cv2.BORDER_CONSTANT,value=(255,255,255)) 

cv2.namedWindow("Test")
cv2.imshow("Test", image1)
cv2.waitKey(0)
cv2.destroyWindow("Test")
#####################################################################################################
api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
##api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
api.SetPageSegMode(tesseract.PSM_AUTO)
height1,width1,channel1=image1.shape
image = cv.CreateImageHeader((width1,height1), cv.IPL_DEPTH_8U, 3)
cv.SetData(image, image1.tostring(), 
           image1.dtype.itemsize * 3 * (width1))
print image
tesseract.SetCvImage(image,api)
text=api.GetUTF8Text()
conf=api.MeanTextConf()
image=None
print text
print conf
