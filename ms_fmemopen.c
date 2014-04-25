#include <windows.h>
#include <tchar.h>
#include <stdio.h>

/*
#include <assert.h>

FILE *fmemopen (void *buf, size_t size, const char *opentype)
{
FILE *f;
assert(strcmp(opentype, "r") == 0);
//f = tmpfile(); 
//errno_t err; 
tmpfile_s(&f);
fwrite(buf, 1, size, f);
rewind(f);
return f;
}
*/
#define MAX_PATH 260
char temppath[MAX_PATH - 13];
char filename[MAX_PATH + 1];
FILE *f;
FILE *fmemopen(void *buf, size_t size, const char *mode) {
		//puts("??????????------????????????????");
		if (0 == GetTempPath(sizeof(temppath), temppath)) {
			puts("Can't get Temp Path");
			return NULL;
		}
		
		if (0 == GetTempFileName(temppath, "SC", 0, filename)) {
			puts("Can't get Temp filename");
			return NULL;
		}
		f = fopen(filename, "wb");
		if (NULL == f) {
			puts("Can't open file");
			return NULL;
		}
		fwrite(buf, size, 1, f);
		fclose(f);
		//puts("OK");
		return fopen(filename, mode);
		
		}
	
