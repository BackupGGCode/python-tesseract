from __future__ import print_function
import platform, os, commands
import __builtin__ 

DEBUG=True
WARNING_LEVEL=10

def print(*argv):
	mlen=len(argv)
	if not DEBUG or (mlen>=2 and argv[1] < WARNING_LEVEL):
		return 
	__builtin__.print(argv[0])

osname=platform.uname()[0].lower()
__builtin__.print("Your os is:%s"%osname)
if osname=="darwin":
	brew_prefix=commands.getstatusoutput('brew --prefix')[1]
	sitepackagesLocations=[
		os.path.expanduser("~/Library/Python/2.7/lib/python/site-packages"),
		"/usr/local/lib/python2.7/site-packages/",
		"/Library/Python/2.7/site-packages"
		]
elif osname=="linux":
	sitepackagesLocations=[
		os.path.expanduser("~/.local/lib/python2.7/site-packages"),
		"/usr/local/lib/python2.7/dist-packages",
		"/usr/lib/python2.7/dist-packages",
		"/usr/lib/python2.7/site-packages",
		]
elif osname=="windows":
	sitepackagesLocations=[
		os.path.expanduser("~\\appdata\\roaming\\python\\python27\\site-packages"),
		"C:\\Python27\\Lib\\site-packages"
		]
def runCmd4Files(pwd,cmd,mfiles):
	for mfile in mfiles:
		#print mfile
		mfile=os.path.join(pwd,mfile)
		if "*" in mfile or os.path.exists(mfile):
			rmStr='%s %s'%(cmd,mfile)
			print(rmStr)
			os.system(rmStr)
		else:
			print("%s cannot be removed"%mfile)

def runRm4Dirs(pwd,mfiles):
	if osname != "windows":
		rmDirCmd="rm -rf"
	else:
		rmDirCmd="rd /S /Q"

	runCmd4Files(pwd,rmDirCmd,mfiles)

def runRm4Files(pwd,mfiles):
	if osname != "windows":
		rmFileCmd="rm -rf"
	else:
		rmFileCmd="del /S /Q"

	runCmd4Files(pwd,rmFileCmd,mfiles)

if __name__ == "__main__":
	print("os is %s"%osname,11)
	print("Warining Level is %s"%8,8)
	print("Warining Level is %s"%11,11)
