from __future__ import print_function
import platform, os, commands,glob
import __builtin__ 
DEBUG=True
WARNING_LEVEL=10
colors={'LIST':'\033[95m',
		'BLACK':'\033[0m',
		'FLOAT' : '\033[95m',
		'INT' : '\033[94m',
		'STR' : '\033[92m',
		'WARNING' : '\033[93m',
		'DICT' : '\033[95m',
		'OKBLUE' : '\033[94m',
		'OKGREEN' : '\033[92m',
		'WARNING' : '\033[93m',
		'FAIL' :'\033[91m',
		'ENDC' : '\033[0m',
		}
colorkeys=colors.keys()
class jfunc():
	def __init__(self):
		self.osname=self.getOsName()
		self.defineSitePackagesLocations()
		
	def type(self,a):
		return repr(type(a)).split(" ")[-1][1:-2].upper()

	def puts(self,*argv,**kwargs):
		END=kwargs.get("END","\t")
		START=kwargs.get("START","")
		mlen=len(argv)
		if mlen> 1 and isinstance( argv[-1], ( int, long ) ):
			warning=argv[-1]
			argv=argv[:-1]
		else:
			warning=0
							
		if not DEBUG or (warning < WARNING_LEVEL):
			return 
		
		for arg in argv:
			argType=self.type(arg)
			if argType in colorkeys:
				START_=colors[argType]+"[%s]"%argType+START
				END_=END+colors['ENDC']
			__builtin__.print(START_,repr(arg).strip(),end=END_)
		__builtin__.print()

	def defineSitePackagesLocations(self):
		osname=self.osname
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

			

	def getOsName(self):
		return platform.uname()[0].lower().strip()
	
		
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
		self.puts([self.osname,len(self.osname)])
		self.puts("------------------")
		if self.osname != "windows":
			self.puts("????")
			rmFileCmd="rm -rf"
			self.puts("removed")
		else:
			self.puts([self.osname,len(self.osname)])
			self.puts("........")
			rmFileCmd="del /S /Q"
		self.puts("****************")
		self.runCmd4Files(pwd,rmFileCmd,mfiles)
		self.puts("*****-----***********")

j=jfunc()
osname=j.osname
sitepackagesLocations=j.sitepackagesLocations
__builtin__.print("Your os is:%s"%osname)

def puts(*argv,**kwargs):
	j.puts(*argv,**kwargs)

if __name__ == "__main__":
	puts("os is %s"%osname,11)
	puts("Warining Level is %s"%8,8)
	puts("Warining Level is %s"%11,11)
	puts(1.21,3,"apple",[1,2,3],192)
	puts(1.21,3,"apple",[1,2,3],192,END=" ")
	puts(1.21,3,"apple",[1,2,3],192,START="*"*10,END="%s,\n"%("^"*10))
