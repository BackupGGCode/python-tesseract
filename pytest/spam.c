#include <Python.h>

static PyObject *SpamError;

static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;
    if(!PyArg_ParseTuple(args, "s", &command))return NULL;

    fprintf(stderr,"this is string \"%s\"\n",command);
    sts = strlen(command);
    if(!sts){
        PyErr_SetString(SpamError, "Empty string received!");
        return NULL;
    }
    return PyLong_FromLong(sts);
}


static PyMethodDef SpamMethods[] = {
    {"system",  spam_system, METH_VARARGS,
     "Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyMODINIT_FUNC
initspam(void)
{
    PyObject *m;

    m = Py_InitModule("spam", SpamMethods);
    if(m == NULL)return;

    SpamError = PyErr_NewException("spam.error", NULL, NULL);
    Py_INCREF(SpamError);
    PyModule_AddObject(m, "error", SpamError);
}

