from __future__ import print_function
import platform, os, commands,glob
import __builtin__ 
DEBUG=True
WARNING_LEVEL=10
osname=platform.uname()[0].lower()
__builtin__.print("Your os is:%s"%osname)

class jfunc():
	def __init__(self):
		self.osname=self.getOsName()
		self.defineSitePackagesLocations()
	
	def print(self,*argv):
		mlen=len(argv)
		if not DEBUG or (mlen>=2 and argv[1] < WARNING_LEVEL):
			return 
		if isinstance(argv[0], (list, tuple)):
			for arg in argv[0]:
				__builtin__.print(arg)
		else:
			__builtin__.print(argv[0])

	def getOsName(self):
		return platform.uname()[0].lower().strip()
	
	def defineSitePackagesLocations(self):
		if osname=="darwin":
			brew_prefix=commands.getstatusoutput('brew --prefix')[1]
			self.sitepackagesLocations=[
				os.path.expanduser("~/Library/Python/2.7/lib/python/site-packages"),
				"/usr/local/lib/python2.7/site-packages/",
				"/Library/Python/2.7/site-packages"
				]
		elif osname=="linux":
			self.sitepackagesLocations=[
				os.path.expanduser("~/.local/lib/python2.7/site-packages"),
				"/usr/local/lib/python2.7/dist-packages",
				"/usr/lib/python2.7/dist-packages",
				"/usr/lib/python2.7/site-packages",
				]
		elif osname=="windows":
			self.sitepackagesLocations=[
				os.path.expanduser("~\\appdata\\roaming\\python\\python27\\site-packages"),
				"C:\\Python27\\Lib\\site-packages"
				]
		else:
			self.sitepackagaesLocations=[]
		
	def runCmd4Files(self,pwd,cmd,mfiles):
		for mfile in mfiles:
			#print mfile
			mfile=os.path.join(pwd,mfile)
			mfiles=glob.glob(mfile)
			for mfile in mfiles:
				if  os.path.exists(mfile):
					rmStr='%s %s'%(cmd,mfile)
					print(rmStr)
					os.system(rmStr)
				else:
					print("%s cannot be removed"%mfile)

	def runRm4Dirs(self,pwd,mfiles):
		if self.osname != "windows":
			rmDirCmd="rm -rf"
		else:
			rmDirCmd="rd /S /Q"

		self.runCmd4Files(pwd,rmDirCmd,mfiles)

	def runRm4Files(self,pwd,mfiles):
		self.print([self.osname,len(self.osname)])
		self.print("------------------")
		if self.osname != "windows":
			self.print("????")
			rmFileCmd="rm -rf"
			self.print("removed")
		else:
			self.print([self.osname,len(self.osname)])
			self.print("........")
			rmFileCmd="del /S /Q"
		self.print("****************")
		self.runCmd4Files(pwd,rmFileCmd,mfiles)
		self.print("*****-----***********")

if __name__ == "__main__":
	j=jfunc()
	j.print("os is %s"%osname,11)
	j.print("Warining Level is %s"%8,8)
	j.print("Warining Level is %s"%11,11)
