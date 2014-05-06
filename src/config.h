#pragma once
#include "fmemopen.h"
#define HAVE_LIBLEPT
#include <Python.h>
#ifndef __darwin__
	#define __darwin__
#endif
#ifndef __opencv2__
	#define __opencv2__
#endif
#include <opencv2/core/core_c.h>
#ifndef __opencv__
	#define __opencv__
#endif
#include <opencv/cv.h>
