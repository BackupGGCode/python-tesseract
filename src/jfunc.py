import platform, os, commands

osname=platform.uname()[0].lower()
if osname=="darwin":
	brew_prefix=commands.getstatusoutput('brew --prefix')[1]
	sitepackagesLocations=[
		os.path.expanduser("~/Library/Python/2.7/lib/python/site-packages"),
		"/usr/local/lib/python2.7/site-packages/",
		"/Library/Python/2.7/site-packages"
		]
def runCmd4Files(pwd,cmd,mfiles):
	for mfile in mfiles:
		#print mfile
		mfile=os.path.join(pwd,mfile)
		if "*" in mfile or os.path.exists(mfile):
			rmStr='%s %s'%(cmd,mfile)
			print rmStr
			os.system(rmStr)
		else:
			print "%s cannot be removed"%mfile

def runRm4Dirs(pwd,mfiles):
	if osname != "windows":
		rmDirCmd="rm -rf"
	else:
		rmDirCmd="rmdir /s /q"

	runCmd4Files(pwd,rmDirCmd,mfiles)

def runRm4Files(pwd,mfiles):
	if osname != "windows":
		rmFileCmd="rm -rf"
	else:
		rmFileCmd="del /S /Q"

	runCmd4Files(pwd,rmFileCmd,mfiles)	
		
