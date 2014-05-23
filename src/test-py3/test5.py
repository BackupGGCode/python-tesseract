#!/usr/bin/env python
import os, tesseract
lang = "eng"
filename = "eurotext.jpg"
TESSDATA_PREFIX = "."
tesseract_version = tesseract.TessVersion()
api = tesseract.TessBaseAPICreate()
rc = tesseract.TessBaseAPIInit3(api, TESSDATA_PREFIX, lang)
if (rc):
    tesseract.TessBaseAPIDelete(api)
    print("Could not initialize tesseract.\n")
    exit(3)
print('Tesseract-ocr version', tesseract_version)
text_out = tesseract.TessBaseAPIProcessPages(api, filename, None, 0)
print(text_out)

