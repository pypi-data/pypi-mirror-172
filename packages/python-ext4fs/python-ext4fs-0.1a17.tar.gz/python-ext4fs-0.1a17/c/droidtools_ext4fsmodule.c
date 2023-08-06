/* tell python that PyArg_ParseTuple(t#) means Py_ssize_t, not int */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#if (PY_VERSION_HEX < 0x02050000)
	typedef int Py_ssize_t;
#endif

/* This is required for compatibility with Python 2. */
#if PY_MAJOR_VERSION >= 3
	#include <bytesobject.h>
	#define y "s"
#else
	#define PyBytes_FromStringAndSize PyString_FromStringAndSize
	#define y "t"
#endif


#include "ext4_utils/ext4_utils.h"
#include "ext4_utils/make_ext4fs.h"

extern struct fs_info info;

//int make_ext4fs(unsigned char* *filename, unsigned char *directory,
//                unsigned char *mountpoint, int android, int gzip, int sparse);


static PyObject *
makeExt4Fs(PyObject *self, PyObject *args)
{
    const char *filename;
    const char *directory;
    const char *mountpoint;
    const char *len;

    Py_ssize_t filenamelen, directorylen, mountpointlen, lenlen, mode, extent;


    if (!PyArg_ParseTuple(args, y"#"y"#"y"#"y"#ii:generate",&filename, &filenamelen, &directory, &directorylen, &mountpoint, &mountpointlen, &len, &lenlen, &mode, &extent)) {
        return NULL;
    }
    printf("filename: %s, dir: %s, mountpoint: %s, len: %s, mode: %i, extent: %i\n", filename, directory, mountpoint, len, mode, extent);

    reset_ext4fs_info();
    info.len = parse_num(len);
    //const char *filename,*directory,*mountpoint, int android,             int gzip, int sparse
    int sparse  =  (int)mode == 1 ? 1: 0;
    int gzip    =  (int)mode == 2 ? 1: 0;
    int android =  mountpoint[0] != '\0'? 1: 0;
    if (directorylen == 0) directory = NULL;


    printf("ANDROID: %i, GZIP: %i, SPARSED: %i", android, gzip, sparse);
    make_ext4fs(filename, directory, mountpoint, android, gzip, sparse, extent);

    return Py_BuildValue("i", 1);

}


static PyMethodDef
ext4_functions[] = {
    {"make_ext4fs", makeExt4Fs, METH_VARARGS, "filename+directory+mountpoint->valid"},
    {NULL, NULL, 0, NULL},
};


#if PY_MAJOR_VERSION >= 3
    static struct PyModuleDef
    ext4_module = {
        PyModuleDef_HEAD_INIT,
        "droidtools.ext4fs",
        NULL,
        NULL,
        ext4_functions,
    };

    PyObject *
    PyInit_ext4fs(void)
    {
        return PyModule_Create(&ext4_module);
    }
#else

    PyMODINIT_FUNC
    initext4fs(void)
    {
        (void)Py_InitModule("droidtools.ext4fs", ext4_functions);
    }

#endif
