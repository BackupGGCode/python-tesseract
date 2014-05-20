import mklibWin64 as m, os, glob

#progNames=["liblept168","libtesseract302_vc90","opencv_core249_vc90"]
progNames=["libtesseract-3","liblept-4"]
src_dir="..\\mingw\\x64"

for progName in progNames:
	m.genLib(src_dir,progName)

