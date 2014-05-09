import mklibWin64 as m, os

cwd=os.getcwd()
progNames=["lept168","tesseract302"]
dll_dir="..\\x64\\dlls"
for progName in progNames:
	m.genLib(cwd,dll_dir,progName)

