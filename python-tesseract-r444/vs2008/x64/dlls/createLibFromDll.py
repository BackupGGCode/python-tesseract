import sys
import os
import os.path
import glob
#must run within a vs2008 command prompt"
def genLib(dllpath, arch, outdir):
    dirname = os.path.dirname(dllpath)
    dllname = os.path.basename(dllpath).split(".")[0]
    deftemp = "%s/%s_temp.temp"%(dirname, dllname)
    defout = "%s/%s.def"%(dirname, dllname)
    if outdir == "":
        outdir = dirname
    if deftemp[0] == "/":
        deftemp = deftemp[1:]
        defout = defout[1:]
    defcmd = "dumpbin %s /exports /out:%s"%(dllpath, deftemp)
    print defcmd
    os.system(defcmd)
    f_temp = open(deftemp, "r")
    f_out = open(defout, "wb")
    f_out.write("LIBRARY %s\n"%(dllname))
    f_out.write("EXPORTS\n")
    begin = False
    for line in f_temp:
        line_s = line.strip().split()
        if len(line_s) < 1:
            continue
        if line_s[0] == "ordinal":
            begin = True
            continue
        if line_s[0] == "Summary":
            begin = False
            break
        if begin == True:
            f_out.write("\t%s\n"%(line_s[3]))
        #print "line_s:%s"%line_s[0]
    f_out.close()
    f_temp.close()
    os.remove(deftemp)
    outlib = "%s/%s.lib"%(outdir, dllname)
    if outlib[0] == "/":
        outlib = outlib[1:]
    libcmd = "lib /def:%s /MACHINE:%s /out:%s"%(defout, arch, outlib)
    print libcmd
    os.system(libcmd)

def main():
    wildcard = sys.argv[1]
    arch = "X86"
    if len(sys.argv) > 2:
        arch = sys.argv[2]
    outdir = ""
    if len(sys.argv) > 3:
        outdir = sys.argv[3]
    if not os.path.exists(outdir) and outdir != "":
        os.makedirs(outdir)
    names = glob.glob(wildcard)
    for dllpath in names:
        genLib(dllpath, arch, outdir)
	
if __name__ == "__main__":
	genLib("liblept168.dll","amd64","")
	genLib("libtesseract302.dll","amd64","")

