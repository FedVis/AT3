#include <Python.h>
#include "mbf.h"
#include "i2m.h"

static PyObject *
ex_m2i(PyObject *self, PyObject *args)
{
float m,i;
if (!PyArg_ParseTuple(args, "f", &m)) return NULL;
i=m2i(m);
return Py_BuildValue("f", i);
}

static PyObject *
ex_i2m(PyObject *self, PyObject *args)
{
float m,i;
if (!PyArg_ParseTuple(args, "f", &m)) return NULL;
i=i2m(m);
return Py_BuildValue("f", i);
}

static PyMethodDef m2ipy_methods[] = {
	{"m2i", ex_m2i, 1, "m2i() Take a microsofot basic format floating point number and returns an ieee number"},
	{"i2m", ex_i2m, 1, "i2m() Take an ieee number and returns a microsofot basic format floating point number"},
	{NULL, NULL}
};


void
initm2ipy(void)
{
	Py_InitModule("m2ipy", m2ipy_methods);
}
