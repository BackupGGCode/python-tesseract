
#ifdef TESS_EXPORTS
#define TESS_API __declspec(dllexport)
#elif defined(TESS_IMPORTS)
#define TESS_API __declspec(dllimport)
#else
#define TESS_API
#define TESS_LOCAL
#endif
#pragma once
#include <Python.h>
#include "fmemopen.h"
#ifndef __mingw__
	#define __mingw__
#endif
