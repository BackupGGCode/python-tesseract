#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import print_function
import tesseract
import ctypes
import os
#print "HAVE_LIBLEPT=",tesseract.isLibLept()
#print dir("tesseract")
#print tesseract.MAX_NUM_INT_FEATURES
api = tesseract.TessBaseAPI()
api.SetOutputName("outputName");
#api.Init(".","eng")
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
mImgFile = "eurotext.jpg"

print "Test ProcessPagesWrapper"
result = tesseract.ProcessPagesWrapper(mImgFile,api)
print "result(ProcessPagesWrapper)=",result
#api.ProcessPages(mImgFile,None, 0, result)
#print "abc"

print "Test ProcessPagesFileStream"
result = tesseract.ProcessPagesFileStream(mImgFile,api)
print "result(ProcessPagesFileStream)=",result

#print "Test ProcessPagesRaw"
#result = tesseract.ProcessPagesRaw(mImgFile,api)
#print "result(ProcessPagesRaw)",result

#print "Test ProcessPagesBuffer"
#f=open(mImgFile,"rb")
#mBuffer=f.read()
#f.close()
#result = tesseract.ProcessPagesBuffer(mBuffer,len(mBuffer),api)
#mBuffer=None
#print "result(ProcessPagesBuffer)=",result
