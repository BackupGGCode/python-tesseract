#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import print_function
import tesseract
import ctypes
import os
import gc
import pprint
#print "HAVE_LIBLEPT=",tesseract.isLibLept()
#print dir("tesseract")
#print tesseract.MAX_NUM_INT_FEATURES
api = tesseract.TessBaseAPI()
api.SetOutputName("outputName");
#api.Init(".","eng")
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
mImgFile = "eurotext.jpg"


print "Method 1: Leptonica->pixRead"
pixImage=tesseract.pixRead(mImgFile)
print "Type of pixiamge=",type(pixImage)
print "repr(pixiamge)=",repr(pixImage)
api.SetImage(pixImage)
#tesseract.SetImage(pixImage,api)
#outText=api.GetUTF8Text()
#print("OCR output:\n%s"%outText);
#api.End()
#outText=None
#tesseract.pixDestroy(pixImage)


#print "Test ProcessPagesWrapper"
#result = tesseract.ProcessPagesWrapper(mImgFile,api)
#print "result(ProcessPagesWrapper)=",result

#print "Test ProcessPagesFileStream"
#result = tesseract.ProcessPagesFileStream(mImgFile,api)
#print "result(ProcessPagesFileStream)=",result

##print "Test ProcessPagesRaw2"
##result = tesseract.ProcessPagesRaw2(mImgFile,api)
##print "result(ProcessPagesRaw2)",result

#print "Test ProcessPagesBuffer"
#f=open(mImgFile,"rb")
#mBuffer=f.read()
#f.close()
#result = tesseract.ProcessPagesBuffer(mBuffer,len(mBuffer),api)
#mBuffer=None
#print "result(ProcessPagesBuffer)=",result



#print "Test ProcessPagesRaw"
#result = tesseract.ProcessPagesRaw(mImgFile,api)
#print "result(ProcessPagesRaw)",result

#for r in gc.get_referents(api):
    #pprint.pprint(r)
#n = gc.collect()
#print 'Unreachable objects:', n
#print 'Remaining Garbage:', 
#pprint.pprint(gc.garbage)
#print
#api.End()
