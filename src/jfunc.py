from __future__ import print_function
import platform, os, subprocess,glob
import subprocess

DEBUG=True
WARNING_LEVEL=10
USE_MINGW=True
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
colorkeys=list(colors.keys())
class jfunc():
	def __init__(self):
		self.osname=self.getOsName()
		#print(self.osname)
		self.defineSitePackagesLocations()
	
	def listDoer(self,doer,anyFile):
		mfiles=glob.glob(anyFile)
		for mfile in mfiles:
			doer(mfile)
	def remove(self,mfile):
		self.listDoer(self.removeOneFile,mfile)
		
	def removeOneFile(self, mfile):
		try:
			os.remove(mfile)
		except:
			print("Cannot Remove: %s"%mfile)
			if not os.path.exists(mfile):
				print("File not existed")
				
	def type(self,a):
		return repr(type(a)).split(" ")[-1][1:-2].upper()

	def puts(self,*argv,**kwargs):
		END=kwargs.get("END","\t")
		START=kwargs.get("START","")
		mlen=len(argv)
		if mlen> 1 and isinstance( argv[-1], int ):
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
			builtins.print(START_,repr(arg).strip(),end=END_)
		builtins.print()

	def defineSitePackagesLocations(self):
		osname=self.osname
		if osname=="darwin":
			#brew_prefix=subprocess.getstatusoutput('brew --prefix')[1]
			brew_prefix=self.cmd('brew --prefix')
			self.sitepackagesLocations=[
				os.path.expanduser("~/Library/Python/2.7/lib/python/site-packages"),
				"/usr/local/lib/python2.7/site-packages/",
				"/Library/Python/2.7/site-packages"
				]
		elif osname=="linux":
			pyVers=["2.7","3","3.4"]
			pyDirFmt=[os.path.expanduser("~/.local/lib/python%%/site-packages"),
				"/usr/local/lib/python%%/dist-packages",
				"/usr/lib/python%%/dist-packages",
				"/usr/lib/python%%/site-packages"]
			self.sitepackagesLocations=[]
			for pyVer in pyVers:
				self.sitepackagesLocations+= [ mdir.replace("%%",pyVer) for mdir in pyDirFmt ]
			#print(self.sitepackagesLocations)


		elif osname=="windows" or osname=="mingw":
			self.sitepackagesLocations=[
				os.path.expanduser("~\\appdata\\roaming\\python\\python27\\site-packages"),
				"C:\\Python27\\Lib\\site-packages"
				]
		else:
			self.sitepackagaesLocations=[]



	def getOsName(self):
		osname=platform.uname()[0].lower().strip()
		if osname=="windows":
			if self.isMinGW():
				osname="mingw"
		return osname

	def isMinGW(self):
		results=subprocess.Popen("gcc --version", stdout=subprocess.PIPE).stdout.read()
		if USE_MINGW and "MinGW" in results:
			return True

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
		if self.osname == "windows" or self.osname=="mingw":
			rmDirCmd="rd /S /Q"
		else:
			rmDirCmd="rm -rf"


		self.runCmd4Files(pwd,rmDirCmd,mfiles)

	def runRm4Files(self,pwd,mfiles):
		self.puts([self.osname,len(self.osname)])
		self.puts("------------------")


		if self.osname == "windows" or self.osname=="mingw":
			self.puts([self.osname,len(self.osname)])
			self.puts("........")
			rmFileCmd="del /S /Q"
		else:
			self.puts("????")
			rmFileCmd="rm -rf"
			self.puts("removed")

		self.puts("****************")
		self.runCmd4Files(pwd,rmFileCmd,mfiles)
		self.puts("*****-----***********")

	def getTesseractVersion(self):
		result=self.cmd("tesseract -v")
		for item in result.split("\n"):
			subItems=item.split()
			if len(subItems)!=2:
				continue
			name, version=subItems
			if name.strip().lower()=="tesseract":
				return version.strip()

		return None
	def cmd(self, cmdStr):
		result=subprocess.check_output(cmdStr.split(),stderr=subprocess.STDOUT)
		return result.decode('utf-8')


j=jfunc()
osname=j.osname
sitepackagesLocations=j.sitepackagesLocations
print("Your os is:%s"%osname)

def puts(*argv,**kwargs):
	j.puts(*argv,**kwargs)

if __name__ == "__main__":
	#puts("os is %s"%osname,11)
	#puts("Warining Level is %s"%8,8)
	#puts("Warining Level is %s"%11,11)
	#puts(1.21,3,"apple",[1,2,3],192)
	#puts(1.21,3,"apple",[1,2,3],192,END=" ")
	#puts(1.21,3,"apple",[1,2,3],192,START="*"*10,END="%s,\n"%("^"*10))
	print(j.osname)
