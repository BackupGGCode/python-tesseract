#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import print_function
import tesseract
import gc
import pprint

api = tesseract.TessBaseAPI()
api.SetOutputName("outputName");
#api.Init(".","eng")
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
mImgFile = "eurotext.jpg"

print("Method 1: Leptonica->pixRead")
pixImage=tesseract.pixRead(mImgFile)
print("Type of pixiamge=",type(pixImage))
print("repr(pixiamge)=",repr(pixImage))
api.SetImage(pixImage)
outText=api.GetUTF8Text()
print(("OCR output:\n%s"%outText));
api.End()
outText=None
tesseract.pixDestroy(pixImage)


