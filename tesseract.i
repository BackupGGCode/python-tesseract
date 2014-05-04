// written by FreeToGo@gmail.com
%module tesseract
%include "cpointer.i"
%pointer_functions(int,intp)
%include "carrays.i"
%include "cdata.i"
%array_class(int, intArray);


%{
#include "config.h"
#include "publictypes.h"
//#include "thresholder.h"
//#include "baseapi_mini.h"
#include "baseapi.h"
//#include "cv_original.h"
#include "main.h"


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
/*
%include <stdint.i>
%typemap(in,numinputs=0,noblock=1) size_t *len  {
  size_t templen;
  $1 = &templen;
}
*/
%typemap(out) int* AllWordConfidences {
  int i;
  //$1, $1_dim0, $1_dim1
  int templen = 0;
  while ($1[templen] >=0) templen++;
  //templen=100;
  $result = PyList_New(templen);
  for (i = 0; i < templen ; i++) {
    PyObject *o = PyInt_FromLong((int) $1[i]);
    PyList_SetItem($result,i,o);
  }
}

%include "config.h"
%include "publictypes.h"
//%include "thresholder.h"
%include "baseapi_mini.h"
//%include "cv_original.h"
%include "main.h"

//#confOfText=tesseract.intArray_frompointer(confOfText)
//#confs=tesseract.intArray(len(text))



