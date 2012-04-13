#include "config.h"
#if !defined(__windows__) && !defined(__darwin__)
	#include <opencv/cv.h>
#endif 

#include <Python.h>

bool isLibTiff(); 
bool isLibLept(); 
char* ProcessPagesWrapper(const char* image,tesseract::TessBaseAPI* api);
char* ProcessPagesPix(const char* image,tesseract::TessBaseAPI* api);
char* ProcessPagesFileStream(const char* image,tesseract::TessBaseAPI* api);
char* ProcessPagesBuffer(char* buffer, int fileLen, tesseract::TessBaseAPI* api);
char* ProcessPagesRaw(const char* image,tesseract::TessBaseAPI* api);
#if !defined(__windows__) && !defined(__darwin__)
	void SetCvImage(PyObject* o, tesseract::TessBaseAPI* api);
	bool SetVariable(const char* var, const char* value, tesseract::TessBaseAPI* api);
	char* GetUTF8Text(tesseract::TessBaseAPI* api);
#endif
