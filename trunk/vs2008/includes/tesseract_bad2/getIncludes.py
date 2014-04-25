sourceDir=r'C:\Program Files (x86)\Tesseract-OCR\tesseract-ocr'
import fnmatch
import os

matches = []
for root, dirnames, filenames in os.walk(sourceDir):
  for filename in fnmatch.filter(filenames, '*.h'):
      matches.append(os.path.join(root, filename))
import shutil

for mfile in matches:
	shutil.copy2(mfile, '.')	
	
