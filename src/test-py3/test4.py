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


