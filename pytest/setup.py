import os, sys, distutils.sysconfig

pylibpath = []
C = distutils.sysconfig.get_config_vars()
pylib = "python" + C["VERSION"]
tools = ['default']
if sys.platform.startswith("win"):
	pylibpath = [os.path.join(C["prefix"],"Libs")]
	tools = ['mingw']
	pylib = [pylib] #,'msvcr90','gcc']


env = Environment(tools = tools
	,ENV=os.environ
	,SWIGFLAGS=['-python']
	,CFLAGS = ['-g','-O2','-Wall']
	,CPPPATH=[distutils.sysconfig.get_python_inc()]	
)


# for MinGW-w64, we need to remap the name of GCC...
if os.environ.get('HOST_PREFIX'):
	env["CC"]=os.environ['HOST_PREFIX'] + "-gcc"


env.SharedLibrary('spam', ['spam.c']
	,LIBPATH=pylibpath
	,LIBS=pylib
	,SHLIBPREFIX=""
	,SHLIBSUFFIX=C["SO"]
)

