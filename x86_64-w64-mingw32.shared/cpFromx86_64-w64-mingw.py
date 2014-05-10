import shutil, errno, os
import glob

def jcopy(src, dst):
	print src,dst
	#return	
	try:
		shutil.copytree(src, dst)
	except OSError as exc: # python >2.5
		if exc.errno == errno.ENOTDIR:
			shutil.copy(src, dst)
		else: raise

srcRoot="/opt/mxe/usr/x86_64-w64-mingw32.shared"

def setSrcDir(*args):
	return os.path.join(srcRoot,*args)

if __name__=="__main__" :
	shoppingList={
		"include": {"include":["tesseract","leptonica"]},
		"dlls": {"bin":["*tess*.dll","*lept*.dll"]},
		"libs": {"lib":["*tess*","*lept*"]}
		}
	for dst in shoppingList.keys():
		print dst
		if not os.path.exists(dst):
			os.makedirs(dst)

		srcs=shoppingList[dst]
		for srcDir in srcs.keys():
			for item in srcs[srcDir]:
				srcPath=setSrcDir(srcDir,item)
				print item,srcPath
				if "*" not in item:
					jcopy(srcPath, os.path.join(dst,item))
				else:
					subItems=glob.glob(srcPath)
					for subItem in subItems:
						jcopy(subItem, dst)
		 
