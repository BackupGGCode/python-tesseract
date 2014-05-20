import mklibWin64 as m, os, glob

cwd=os.getcwd()
progNames=["liblept168","libtesseract302_vc90","opencv_core249_vc90"]
dll_dir="..\\x64\\dlls"
for progName in progNames:
	m.genLib(cwd,dll_dir,progName)

