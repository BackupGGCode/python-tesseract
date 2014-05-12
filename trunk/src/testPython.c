#include <Python.h>
/* run with gcc -I c:\Python27\include -DMS_WIN64 testPython.c
int main()
{
    printf("sizeof(Py_intptr_t) = %d\n", sizeof(Py_intptr_t));
    return 0;
}
