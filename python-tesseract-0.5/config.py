import platform

osname=platform.uname()[0]
fp=open("config.h","w")
fp.write("#define __%s__\n"%osname.lower())
fp.close()
