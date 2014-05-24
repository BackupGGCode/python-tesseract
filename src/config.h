
#ifdef TESS_EXPORTS
#define TESS_API __declspec(dllexport)
#elif defined(TESS_IMPORTS)
#define TESS_API __declspec(dllimport)
#else
#define TESS_API
#define TESS_LOCAL
#define LEPT_DLL

#define TESS_CAPI_INCLUDE_BASEAPI
#endif
#pragma once
#include <Python.h>
#ifndef __opencv2__
	#define __opencv2__
#endif
#include <opencv2/core/core_c.h>
#ifndef __linux__
	#define __linux__
#endif
