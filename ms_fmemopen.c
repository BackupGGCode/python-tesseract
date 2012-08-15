#include <stdio.h>
#include <assert.h>

FILE *fmemopen (void *buf, size_t size, const char *opentype)
{
FILE *f;
assert(strcmp(opentype, "r") == 0);
f = tmpfile();
fwrite(buf, 1, size, f);
rewind(f);
return f;
}
