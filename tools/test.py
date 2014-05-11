fname="liblept168_vc90.def"
def patchDef(fname):
	basename=fname.split(".")[0]
	lines=open(fname).readlines()
	print lines[0]
	lines[0]="LIBRARY %s.dll\n"%basename
	print lines[0]
	fp=open(fname,"w")
	fp.write("".join(lines))
	fp.close()
	
patchDef(fname)
