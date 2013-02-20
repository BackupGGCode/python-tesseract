//#include "mfcpch.h"
// #define USE_VLD //Uncomment for Visual Leak Detector.
#if (defined _MSC_VER && defined USE_VLD)
#include "mfcpch.h"
#include <vld.h>
#endif

// Include automatically generated configuration file if running autoconf
#include "config.h"

#include "allheaders.h"
#include "baseapi.h"
#include "img.h"
#include "strngs.h"

#include "main.h"
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


char* retParser(const char* a) {
	int mlen=strlen(a);
	char *retStr=new char[mlen+1];
	retStr[mlen]=0;
	memcpy(retStr,a,mlen);
	//strcpy (retStr,a);
	return retStr;
}


char* ProcessPagesWrapper(const char* image,tesseract::TessBaseAPI* api) {
	//printf("ok->%s",text_out);
	STRING mstr;
	api->ProcessPages(image, NULL, 0, &mstr);
	//return mstr.string();
	return retParser(mstr.string());
 }


char* ProcessPagesPix(const char* image,tesseract::TessBaseAPI* api) {
	STRING mstr;
	int page=0;
	Pix *pix;
	pix = pixRead(image);
	api->ProcessPage(pix, page, NULL, NULL, 0, &mstr);
	free(pix->data);
	free(pix->text);
	return retParser(mstr.string());

}


char* ProcessPagesFileStream(const char* image,tesseract::TessBaseAPI* api) {

	Pix *pix;
	STRING mstr;
	int page=0;
	FILE *fp=fopen(image,"rb");
	pix=pixReadStream(fp,0);
	fclose(fp);
	api->ProcessPage(pix, page, NULL, NULL, 0, &mstr);
	free(pix->data);
	free(pix->text);
	return retParser(mstr.string());
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
	if (stream == NULL)
		return "Error";
	Pix *pix;
	int page=0;
	STRING mstr;

	pix=pixReadStream(stream,0);
	if (stream != NULL)
		fclose(stream);
	api->ProcessPage(pix, page, NULL, NULL, 0, &mstr);
	free(pix->data);
	free(pix->text);
	return retParser(mstr.string());

 }

#include <iostream>
#include <fstream>
using namespace std;
char* ProcessPagesRaw(const char* image,tesseract::TessBaseAPI* api) {
	//puts(image);
	ifstream fs(image, ios::in|ios::binary|ios::ate);
	if ( !fs.is_open()) {
		char msg[200];
		sprintf(msg,"Cannot Open File:%s\n",image);
		return (char*)msg;
	}
	int size =(int) fs.tellg()  ;
	char *buffer = new char [size+1];
	fs.seekg (0, ios::beg);
	fs.read (buffer, size);
	fs.close();

	//cout << "the complete file content is in memory";

	if (!buffer)
	{
		fprintf(stderr, "Memory error!");
        return NULL ;
	}

	//dump_buffer(buffer,size);
	char* retStr;
	//printf("size=%d\n",size);
	retStr=ProcessPagesBuffer(buffer,size, api);
	delete[] buffer;
	//free(buffer);
	return retStr;
 }

char* ProcessPagesRaw2(const char* image,tesseract::TessBaseAPI* api) {
	/* no good, it will crash in M$ ???not thread-safe ????*/
	FILE *fp=fopen(image,"rb");
	//Get file length
	fseek(fp, 0, SEEK_END);
	int size=ftell(fp);
	fseek(fp, 0, SEEK_SET);
	//Allocate memory
	//buffer=(char *)malloc(size+1);
	char *buffer = new char [size+1];
	if (!buffer)
	{
		fprintf(stderr, "Memory error!");
        fclose(fp);
		return NULL ;
	}
	int n;
	n = fread(buffer,size, 1, fp);
	fclose(fp);
	//printf("n=%d\n",n);
	//dump_buffer(buffer,size);
	char* retStr;
	//printf("size=%d\n",size);
	retStr=ProcessPagesBuffer(buffer,size, api);
	delete[] buffer;
	//free(buffer);
	return retStr;
 }
#if defined(__opencv__) || defined(__opencv2__)
//#ifdef __opencv2__
 /* from PyBLOB project
  http://code.google.com/p/pyblobs/issues/attachmentText?id=2&aid=4459562154860045232&name=iplimage_t.h&token=ed989cead6fe486664a024d538bccc2b
  */
#include "cv_original.h"

void SetCvImage(PyObject* o, tesseract::TessBaseAPI* api)
{
    IplImage* img;
    int res =  convert_to_IplImage(o, &img);
	printf("res=%d\n",res);
    //if successfull
    if ( res == 1 )
    {
      api->SetImage( (unsigned char*) img->imageData,  img->width, img->height, img->nChannels, img->widthStep);
    }

}
/*
namespace bp = boost::python;
void SetMat(PyObject* o, tesseract::TessBaseAPI* api)
{
	CvMat *img0;
    int res =  convert_to_CvMat(o, &img0);
	IplImage objImg, *img;
	objImg=(IplImage)*img0;
	img=&objImg;
    //if successfull
    api->SetImage( (unsigned char*) img->imageData,  img->width, img->height, img->nChannels, img->widthStep);

}
*/

/*
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
*/
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
