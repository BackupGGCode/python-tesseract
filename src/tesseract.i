// written by FreeToGo@gmail.com  in  May 2014
%module tesseract
%include "cpointer.i"
%pointer_functions(int,intp)
%include "carrays.i"
%include "cdata.i"
%array_class(int, intArray);
%newobject retParser;


%{


#define TESS_API
#define TESS_LOCAL
#define LEPT_DLL
#define TESS_CAPI_INCLUDE_BASEAPI


#include "config.h"
//#include "pix.h"
#include "allheaders.h"
#include "publictypes.h"
#include "thresholder.h"
#include "capi.h"
//#include pageiterator.h
#include "ltrresultiterator.h"
#include "resultiterator.h"
#include "baseapi.h"
#include "unichar.h"
#include "renderer.h"


//#include "cv_original.h"
#include "main.h"
char* retParser(const char* a);


%}
/* Input typemap: convert from Python input object to C/C++ IplImage

   Note:
    - $input corresonds to the input Python object that is to be converted (i.e. PyObject*)
    - $1 refers to the corresponding C/C++ variable, i.e the recipient of the conversion (i.e. IplImage* )
*/
%typemap(in) IplImage *{

    if (!convert_to_IplImage($input, &($1), ""))
    {
        SWIG_exception( SWIG_TypeError, "%%typemap: could not convert input argument to an IplImage");
    }
}

%typemap(in, numinputs=0) STRING *text_out (STRING temp) {
  $1 = &temp;
}

%typemap(argout) STRING *text_out {
 $result = PyString_FromString($1->string());
}


#%typemap(out) int* AllWordConfidences {
%typemap(out) int* {
  int i, len;
  //$1, $1_dim0, $1_dim1
  len = 0;
  while ($1[len]>=0) len++;
  $result = PyList_New(len);
  for (i = 0; i < len ; i++) {
    PyObject *o = PyInt_FromLong((int) $1[i]);
    PyList_SetItem($result,i,o);
  }
}

#define TESS_API
#define TESS_LOCAL
#define LEPT_DLL
#define TESS_CAPI_INCLUDE_BASEAPI
%ignore setPixMemoryManager;
%include "config.h"
%include "pix.h"
%include "allheaders_mini.h"
//%include "allheaders.h"
%include "publictypes.h"
%include "baseapi_mini.h"
%include "capi_mini.h"
%include "thresholder.h"
%include "pageiterator.h"
%include "ltrresultiterator.h"
%include "resultiterator.h"
%include "renderer.h"
%include "main.h"
