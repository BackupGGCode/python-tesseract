#include "config.h"

//#include <Python.h>
#define __opencv2__
//  <---- needed by vc9   <--- can't read #define from config.h
// if everyone knows why, please contact me
bool isLibTiff(); 
bool isLibLept(); 
char* ProcessPagesWrapper(const char* image,tesseract::TessBaseAPI* api);
char* ProcessPagesPix(const char* image,tesseract::TessBaseAPI* api);
char* ProcessPagesFileStream(const char* image,tesseract::TessBaseAPI* api);
char* ProcessPagesBuffer(char* buffer, int fileLen, tesseract::TessBaseAPI* api);
char* ProcessPagesRaw(const char* image,tesseract::TessBaseAPI* api);

#if defined(__opencv__) || defined(__opencv2__)
	void SetCvImage(PyObject* o, tesseract::TessBaseAPI* api);
	bool SetVariable(const char* var, const char* value, tesseract::TessBaseAPI* api);
	char* GetUTF8Text(tesseract::TessBaseAPI* api);
#endif
