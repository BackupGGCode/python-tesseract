#include "mfcpch.h"
// #define USE_VLD //Uncomment for Visual Leak Detector.
#if (defined _MSC_VER && defined USE_VLD)
#include <vld.h>
#endif

// Include automatically generated configuration file if running autoconf
#include "config.h"

#ifdef USING_GETTEXT
#include <libintl.h>
#include <locale.h>
#define _(x) gettext(x)
#else
#define _(x) (x)
#endif
#include "allheaders.h"
#include "baseapi.h"
#include "img.h"
#include "strngs.h"
#include "tprintf.h"
#include "tesseractmain.h"

#include "main_dummy.h"
#include "stdio.h"
#include "stdlib.h"

bool isLibLept() {

	#if defined(HAVE_LIBLEPT)
		return true;
	#else
		return false;
	#endif
	}
  
bool isLibTiff() {
	#if defined(HAVE_LIBLEPT)
		return true;
	#else
		return false;
	#endif
	}
//  useless <<<<<<<<
int readBuf(const char *fname,l_uint8 *buf) {
	FILE *fp;
	long len;
	fp=fopen(fname,"rb");
	fseek(fp,0,SEEK_END); //go to end
	len=ftell(fp); //get position at end (length)
	fseek(fp,0,SEEK_SET); //go to beg.
	buf=(l_uint8 *)malloc(len); //malloc buffer
	fread(buf,len,1,fp); //read into buffer
	fclose(fp);
	return len;
}


char* ProcessPagesWrapper(const char* image,tesseract::TessBaseAPI* api) {
	//printf("ok->%s",text_out);
	STRING mstr; 
	api->ProcessPages(image, NULL, 0, &mstr);
	const char *tmpStr=mstr.string();
	char *retStr = new char[strlen(tmpStr) + 1];
	strcpy (retStr,tmpStr);
	return retStr;
 }                


char* ProcessPagesPix(const char* image,tesseract::TessBaseAPI* api) {
	STRING mstr; 
	int page=0;
	Pix *pix;
	pix = pixRead(image);
	//l_uint8 buf[10000];
	//int len=readBuf(image,buf);
	//if (len < 0) 
	//	puts("Cannot Read Buffer");
	api->ProcessPage(pix, page, NULL, NULL, 0, &mstr);
	const char *tmpStr=mstr.string();
	char *retStr = new char[strlen(tmpStr) + 1];
	strcpy (retStr,tmpStr);
	//printf("ok->%s",retStr);
	return retStr;
 }
 
     
char* ProcessPagesFileStream(const char* image,tesseract::TessBaseAPI* api) {
	
	Pix *pix;
	STRING mstr;
	int page=0;
	FILE *fp=fopen(image,"rb");
	pix=pixReadStream(fp,0);
	api->ProcessPage(pix, page, NULL, NULL, 0, &mstr);
	const char *tmpStr=mstr.string();
	char *retStr = new char[strlen(tmpStr) + 1];
	strcpy (retStr,tmpStr);
	//printf("ok->%s",retStr);
	fclose(fp);
	return retStr;
 }
void dump_buffer(void *buffer, int buffer_size)
{
  int i;
  for(i = 0;i < buffer_size;++i)
     printf("%c", ((char *)buffer)[i]);
}

char* ProcessPagesBuffer(char* buffer, int fileLen, tesseract::TessBaseAPI* api) {
	
	FILE *stream;
	//int ch;
	stream=fmemopen((void*)buffer,fileLen,"rb");
	//int count;
	//while ((ch = fgetc (stream)) != EOF)
	//	printf ("Got %d:%c\n", count++,ch);
	//fclose (stream);
	//puts("''''''''''''''''''");
	
	Pix *pix;
	int page=0;
	STRING mstr;
	
	pix=pixReadStream(stream,0);
	api->ProcessPage(pix, page, NULL, NULL, 0, &mstr);
	const char *tmpStr=mstr.string();
	char *retStr = new char[strlen(tmpStr) + 1];
	strcpy (retStr,tmpStr);
	//printf("ok->%s",retStr);

	return retStr;
 }
 
char* ProcessPagesRaw(const char* image,tesseract::TessBaseAPI* api) {
	

	FILE *fp=fopen(image,"rb");
	//Get file length
	fseek(fp, 0, SEEK_END);
	int fileLen=ftell(fp);
	fseek(fp, 0, SEEK_SET);
	//printf("fileLen=%d\n",fileLen);
	char *buffer;
	//Allocate memory
	buffer=(char *)malloc(fileLen+1);
	if (!buffer)
	{
		fprintf(stderr, "Memory error!");
        fclose(fp);
		return NULL ;
	}
	int n;
	n = fread(buffer,fileLen, 1, fp);
	fclose(fp);
	//printf("n=%d\n",n);
	//dump_buffer(buffer,fileLen);
	char* retStr;
	retStr=ProcessPagesBuffer(buffer,fileLen, api);
	//Free memory
	free(buffer);
	return retStr;
 }
#if defined(__opencv__) || defined(__opencv2__)
 /* from PyBLOB project 
  http://code.google.com/p/pyblobs/issues/attachmentText?id=2&aid=4459562154860045232&name=iplimage_t.h&token=ed989cead6fe486664a024d538bccc2b
  */
struct iplimage_t {
    PyObject_HEAD
    IplImage *a;
    PyObject *data;
    size_t offset;
}; 
  
static PyTypeObject iplimage_Type = {
  PyObject_HEAD_INIT(&PyType_Type)
  0,                                      /*size*/
  "cv.iplimage",                          /*name*/
  sizeof(iplimage_t),                        /*basicsize*/
};

static int is_none(PyObject *o)
{
  //printf("is_none: %d\n", Py_None == o);
  return Py_None == o;
}

static int is_iplimage(PyObject *o)
{
  PyObject* to = PyObject_Type(o);
  const char* tp_name = ((PyTypeObject*) to)->tp_name;
  //printf("is_iplimage: %s, %d\n", tp_name, strcmp(tp_name, "cv.iplimage") == 0);
  return strcmp(tp_name, "cv.iplimage") >= 0;
}

/* convert_to_IplImage(): convert a PyObject* to IplImage*/
/* Note: this has been copied verbatim from <opencv_root>/interfaces/python/cv.cpp */
static int convert_to_IplImage(PyObject *o, IplImage **dst)
{
    iplimage_t *ipl = (iplimage_t*)o;
    void *buffer;
    Py_ssize_t buffer_len;

    if (!is_iplimage(o)) {
	return -1; //failmsg("Argument must be IplImage");
    } else if (PyString_Check(ipl->data)) {
	cvSetData(ipl->a, PyString_AsString(ipl->data) + ipl->offset, ipl->a->widthStep);
	assert(cvGetErrStatus() == 0);
	*dst = ipl->a;
	return 1;
    } else if (ipl->data && PyObject_AsWriteBuffer(ipl->data, &buffer, &buffer_len) == 0) {
	cvSetData(ipl->a, (void*)((char*)buffer + ipl->offset), ipl->a->widthStep);
	assert(cvGetErrStatus() == 0);
	*dst = ipl->a;
	return 1; 
    } else {
	return -1;// failmsg("IplImage argument has no data");
    }
}

void SetCvImage(PyObject* o, tesseract::TessBaseAPI* api)
{
    IplImage* img, *grayImg, *blackWhiteImg;
    int res =  convert_to_IplImage(o, &img);

    //if succesfull
    if ( res == 1 )
    {   
      api->SetImage( (unsigned char*) img->imageData,  img->width, img->height, img->nChannels, img->widthStep);
    }

}

char* GetUTF8Text(tesseract::TessBaseAPI* api)
{
  //puts("GetUTF8Text");
  bool failed = api->Recognize(NULL) < 0;
  //printf("failed=%s",(failed)?"true":"false");
  if ( failed) return 0;
  
  STRING mstr = api->GetUTF8Text();
  const char *tmpStr=mstr.string();
  //printf("tmpStr->%s",tmpStr);
  char *retStr = new char[strlen(tmpStr) + 1];
  strcpy (retStr,tmpStr);
  //printf("retStr->%s",retStr);
  return retStr;  
}

bool SetVariable(const char* var, const char* value, tesseract::TessBaseAPI* api)
{
  bool res = api->SetVariable(var, value);
  printf ("set variable %s result %d\n", var, res); 
  return res;
}

#endif
