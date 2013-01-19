// written by FreeToGo@gmail.com
%module tesseract
%include "cpointer.i"
%pointer_functions(int,intp)
%include "carrays.i"
%include "cdata.i"

%{
#include "config.h"
#include "publictypes.h"
//#include "thresholder.h"
#include "baseapi_mini.h"
#include "main_dummy.h"

%}
%include "config.h"
%include "publictypes.h"
//%include "thresholder.h"
%include "baseapi_mini.h"
%include "main_dummy.h"





