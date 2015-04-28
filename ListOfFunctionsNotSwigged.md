# Introduction #

Usually it is because I am too dumb to swig these functions. They are therefore commented out so that I could complete the compilation.

# Files #
They are added into a dictionary called "patchDict" in patchEngine.py.
```
def run(tess_version):
	if PYTHON3:		
		patchDict=collections.OrderedDict([
			("leptonica:allheaders.h",["setPixMemoryManager"]),
			("leptonica:pix.h",None),
			("tesseract:publictypes.h",["char* kPolyBlockNames"]),
			("tesseract:baseapi.h",["Dict", "ImageThresholder","ProbabilityInContextFunc"]),
			("tesseract:pageiterator.h",None),
			("tesseract:ltrresultiterator.h",["ChoiceIterator"]),
			("tesseract:thresholder.h",None),
			("tesseract:resultiterator.h",None),
			("tesseract:renderer.h",None),
			])
	else:
		patchDict=collections.OrderedDict([
			("leptonica:allheaders.h",["setPixMemoryManager"]),
			("leptonica:pix.h",None),
			("tesseract:publictypes.h",["char* kPolyBlockNames"]),
			("tesseract:baseapi.h",["Dict", "ImageThresholder","ProbabilityInContextFunc"]),
			("tesseract:capi.h",["TessBaseAPIInit","TessBaseAPISetFillLatticeFunc","TessDictFunc","TessProbabilityInContextFunc"]),
			("tesseract:pageiterator.h",None),
			("tesseract:ltrresultiterator.h",["ChoiceIterator"]),
			("tesseract:thresholder.h",None),
			("tesseract:resultiterator.h",None),
			("tesseract:renderer.h",None),
			])
		if tess_version<"3.03":
			#patchDict["tesseract:publictypes.h"].append("PageIterator")
			patchDict["tesseract:baseapi.h"]+=["iterator","PageIterator","GetLastInitLanguage"]
			patchDict["tesseract:ltrresultiterator.h"].append("PageIterator")
			#del patchDict["tesseract:pageiterator.h"]
			#del patchDict["tesseract:resultiterator.h"]
			del patchDict["tesseract:renderer.h"]
```