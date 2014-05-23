#!/usr/bin/env python
import tesseract
import gc, pprint

api = tesseract.TessBaseAPI()
api.SetOutputName("outputName");
#api.Init(".","eng")
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
mImgFile = "eurotext.jpg"

print("Test ProcessPagesWrapper")
result = tesseract.ProcessPagesWrapper(mImgFile,api)
print("result(ProcessPagesWrapper)=",result)

print("Test ProcessPagesFileStream")
result = tesseract.ProcessPagesFileStream(mImgFile,api)
print("result(ProcessPagesFileStream)=",result)

print("Test ProcessPagesRaw")
result = tesseract.ProcessPagesRaw(mImgFile,api)
print("result(ProcessPagesRaw)",result)

for r in gc.get_referents(api):
    pprint.pprint(r)
n = gc.collect()
print('Unreachable objects:', n)
print('Remaining Garbage:')
pprint.pprint(gc.garbage)
print()
api.End()
