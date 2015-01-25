#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import print_function
import tesseract
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
print("1.Test api.ProcessPages")
mImgFile = "eurotext.jpg"
result=api.ProcessPages(mImgFile, None, 0)
print(("result(api.ProcessPages)=",result))

print("2.Test ProcessPagesWrapper")
result = tesseract.ProcessPagesWrapper(mImgFile,api)
print(("result(ProcessPagesWrapper)=",result))

print("3.Test ProcessPagesFileStream")
result = tesseract.ProcessPagesFileStream(mImgFile,api)
print(("result(ProcessPagesFileStream)=",result))


print("4.Test ProcessPagesRaw")
result = tesseract.ProcessPagesRaw(mImgFile,api)
print(("result(ProcessPagesRaw)",result))

for r in gc.get_referents(api):
    pprint.pprint(r)
n = gc.collect()
print(('Unreachable objects:', n))
print('Remaining Garbage:')
pprint.pprint(gc.garbage)
print('Endding')
result=None
api.End()
