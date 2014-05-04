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
%include "config.h"
%include "publictypes.h"
//%include "thresholder.h"
%include "baseapi_mini.h"
//%include "cv_original.h"
%include "main.h"





