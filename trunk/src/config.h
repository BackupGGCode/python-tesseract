
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
#define HAVE_LIBLEPT
#ifndef __darwin__
	#define __darwin__
#endif
