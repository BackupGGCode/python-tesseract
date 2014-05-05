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
pyPtr=tesseract.cdata(intPtr,100)
for i in range(10):
	print ord(pyPtr[i])
tesseract.delete_intp(intPtr) 

