#include <stdlib.h>
#include <stdio.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <cv.h>
#include <baseapi.h>
#include <allheaders.h>
#include <sys/time.h>
using namespace cv;

/// Global Variables
Mat src, dst;
int top, bottom, left, right;
int borderType;
Scalar value;

int main( int argc, char** argv )
{
	IplImage *image0,*image;
	image0=cvLoadImage("p.bmp", CV_LOAD_IMAGE_UNCHANGED);
	int offset=5;        // when offset is set to <=4, tesseract will fail to ocr the p.bmp
	int conf;
	char *text;
	image=cvCreateImage(cvSize(image0->width+offset*2, image0->height+offset*2), IPL_DEPTH_8U, 3 ) ;
	value = Scalar(255,255,255);
	cvCopyMakeBorder(image0,image, cvPoint(offset,offset), IPL_BORDER_CONSTANT, value);
	//cvNamedWindow("Test");
	//cvShowImage("Test", image);
	//cvWaitKey(0);
	//cvDestroyWindow("Test");
	
	tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();
	api->Init(".","eng",tesseract::OEM_DEFAULT);
	api->SetPageSegMode(tesseract::PSM_AUTO);
	api->SetImage( (unsigned char*) image->imageData,  image->width, image->height, image->nChannels, image->widthStep);
	text=api->GetUTF8Text();
	conf=api->MeanTextConf();
	cvReleaseImage(&image);
	cvReleaseImage(&image0);
	printf("[%d]%s",conf,text);
	
}
