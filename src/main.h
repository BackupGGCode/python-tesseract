#include "config.h"
bool isLibTiff();
bool isLibLept();
int*  AllWordConfidences(tesseract::TessBaseAPI* api);
char* ProcessPagesWrapper(const char* image,tesseract::TessBaseAPI* api);
char* ProcessPagesPix(const char* image,tesseract::TessBaseAPI* api);
char* ProcessPagesFileStream(const char* image,tesseract::TessBaseAPI* api);
char* ProcessPagesBuffer(char* buffer, int fileLen, tesseract::TessBaseAPI* api);
char* ProcessPagesRaw(const char* image,tesseract::TessBaseAPI* api);
void SetCvImage(PyObject* o, tesseract::TessBaseAPI* api);
bool SetVariable(const char* var, const char* value, tesseract::TessBaseAPI* api);
char* GetUTF8Text(tesseract::TessBaseAPI* api);
void SetCvImage(PyObject* o, tesseract::TessBaseAPI* api);
bool SetVariable(const char* var, const char* value, tesseract::TessBaseAPI* api);
char* GetUTF8Text(tesseract::TessBaseAPI* api);
