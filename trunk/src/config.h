#pragma once
#ifndef __darwin__
	#define __darwin__
#endif
#include "fmemopen.h"
#define HAVE_LIBLEPT
#ifndef __opencv2__
	#define __opencv2__
#endif
#include <opencv2/core/core_c.h>
#ifndef __opencv__
	#define __opencv__
#endif
#include <cv.h>
#include <Python.h>
