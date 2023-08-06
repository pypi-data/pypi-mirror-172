/*
Copyright (c) 2022-2027 VisionFive

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#include "Python.h"
#include "c_gpio.h"
#include "py_constants.h"
#include "cpuinfo.h"
#include "../pwm/py_pwm.h"

int int_check(PyObject *tempobj, int *gpioport) {
	unsigned int gpiooffset;

#if PY_MAJOR_VERSION > 2
		if (PyLong_Check(tempobj)) {
			*gpioport = (int)PyLong_AsLong(tempobj);
#else
		if (PyInt_Check(tempobj)) {
			*gpioport = (int)PyInt_AsLong(tempobj);
#endif
		if (PyErr_Occurred())
			return 1;
		} else {
			PyErr_SetString(PyExc_ValueError, "gpioport must be an integer");
			return 1;
		}
		if (get_gpio_offset(gpioport, &gpiooffset))
			return 1;

		return 0;
}

int GPIO_Data_check(PyObject *gpiolist, PyObject *gpiotuple, int *gpioport, int *gpiocount) {

#if PY_MAJOR_VERSION > 2
		if (PyLong_Check(gpiolist)) {
			*gpioport = (int)PyLong_AsLong(gpiolist);
#else
		if (PyInt_Check(gpiolist)) {
			*gpioport = (int)PyInt_AsLong(gpiolist);
#endif
			if (PyErr_Occurred())
				return 1;
			gpiolist = NULL;
		} else if (PyList_Check(gpiolist)) {
			*gpiocount = PyList_Size(gpiolist);
		} else if (PyTuple_Check(gpiolist)) {
			gpiotuple = gpiolist;
			gpiolist = NULL;
			*gpiocount = PyTuple_Size(gpiotuple);
		} else {
			// raise exception
			PyErr_SetString(PyExc_ValueError, "gpioport must be an integer or list/tuple of integers");
			return 1;
		}
		return 0;
}

/*
* python function cleanup(gpioport=None)
**clean up GPIO0, tow different input format are allowed
*  	GPIO.cleanup(gp=0)
*  	GPIO.cleanup(0)
*
** clear up all GPIO ports
*   GPIO.cleanup()
*/
static PyObject *py_cleanup(PyObject *self, PyObject *args, PyObject *kwargs)
{
	int ret, i;
	int gpiocount = -255;
	int found = 0;
	int gpioport = -255;
	unsigned int gpiooffset;
	PyObject *gpiolist = NULL;
	PyObject *gpiotuple = NULL;
	PyObject *tempobj;
	static char *kwlist[] = {"gp", NULL};

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|O", kwlist, &gpiolist))
		return NULL;

	if (gpiolist == NULL) {  // gpioport kwarg not set
	// do nothing
	}
	else {
		ret = GPIO_Data_check(gpiolist, gpiotuple, &gpioport, &gpiocount);
		if (ret == 1)
			return NULL;
	}

	if (gpioport == -255 && gpiocount == -255) {
		for (i = 0; i < 49; i++) {
			if (gpio_direction[i] != -1) {
				setup_gpio(i, INPUT, PUD_OFF);
				gpio_direction[i] = -1;
				found = 1;
			}
		}
	} else if (gpioport != -255) {

	if (get_gpio_offset(&gpioport, &gpiooffset))
		return NULL;
	cleanup_one(gpioport, &found);

	} else {  
		// gpioport was a list/tuple

		for (i = 0; i < gpiocount; i++) {
			if (gpiolist) {
				if ((tempobj = PyList_GetItem(gpiolist, i)) == NULL) {
					return NULL;
				}
			} else { // assume gpiotuple
				if ((tempobj = PyTuple_GetItem(gpiotuple, i)) == NULL) {
					return NULL;
				}
			}

			ret = int_check(tempobj, &gpioport);
			if (ret == 1)
				return NULL;
			cleanup_one(gpioport, &found);
		}
	}


	// check if any gpioports set up - if not warn about misuse of GPIO.cleanup()
	if (!found ) {
		PyErr_WarnEx(NULL, "None of gpioports has been set up !", 1);
	}

	Py_RETURN_NONE;
}

/*
*
**different input format are allowed
*  	GPIO.setup(gp=0, dir=GPIO.OUT)
*  	GPIO.setup(0, GPIO.OUT)
**Also serveral GPIO ports can be set at one time
*   GPIO.setup(gp=[0, 2, 4], dir=GPIO.OUT)
*   GPIO.setup([0, 2, 4], GPIO.OUT)
*/
static PyObject *py_setup_gpioport(PyObject *self, PyObject *args, PyObject *kwargs)
{
	int gpioport = -255;
	int direction = -1;
	int initial = -1;
	int i = 0, ret = 0;
	int gpiocount = -255;
	int pud = PUD_OFF;
	unsigned int gpiooffset;
	static char *kwlist[] = {"gp", "dir", "pud", "init", NULL};
	PyObject *gpiolist = NULL;
	PyObject *gpiotuple = NULL;
	PyObject *tempobj;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "Oi|ii", kwlist, &gpiolist, &direction, &pud, &initial))
		return NULL;

	ret = GPIO_Data_check(gpiolist, gpiotuple, &gpioport, &gpiocount);
	if (ret == 1)
		return NULL;

	if (direction != INPUT && direction != OUTPUT) {
		PyErr_SetString(PyExc_ValueError, "An invalid direction was passed to setup()");
		return 0;
	}

	if (direction == OUTPUT && pud != PUD_OFF) {
		PyErr_SetString(PyExc_ValueError, "pull_up_down parameter is not valid for outputs");
		return 0;
	}

	if (direction == INPUT && initial != -1) {
		PyErr_SetString(PyExc_ValueError, "initial parameter is not valid for inputs");
		return 0;
	}

	if (pud != PUD_OFF && pud != PUD_DOWN && pud != PUD_UP) {
		PyErr_SetString(PyExc_ValueError, "Invalid value for pull_up_down - should be either PUD_OFF, PUD_UP or PUD_DOWN");
		return NULL;
	}

	if (gpioport != -255) {    // the type of gp is a single gpioport

	 if (get_gpio_offset(&gpioport, &gpiooffset))
		return NULL;

	 if (!setup_one(gpioport, direction, initial))
		return NULL;

	 Py_RETURN_NONE;
	}

	for (i = 0; i< gpiocount; i++) {
		if (gpiolist) {
			if ((tempobj = PyList_GetItem(gpiolist, i)) == NULL) {
				return NULL;
			}
		} else { // assume gpiotuple
			if ((tempobj = PyTuple_GetItem(gpiotuple, i)) == NULL) {
				return NULL;
			}
		}

		ret = int_check(tempobj, &gpioport);
		if (ret == 1)
			return NULL;

		if (!setup_one(gpioport, direction, initial))
			return NULL;
	}

   Py_RETURN_NONE;
}

// python function output_py(gpioport(s), value(s))
static PyObject *py_output_gpio(PyObject *self, PyObject *args)
{
	int gpioport = -1;
	int value = -1;
	int gpiocount = -1;
	int valuecount = -1;
	int i = 0;
	PyObject *gpiolist = NULL;
	PyObject *valuelist = NULL;
	PyObject *gpiotuple = NULL;
	PyObject *valuetuple = NULL;
	PyObject *tempobj = NULL;

	if (!PyArg_ParseTuple(args, "OO", &gpiolist, &valuelist))
		return NULL;

#if PY_MAJOR_VERSION >= 3
	if (PyLong_Check(gpiolist)) {
		gpioport = (int)PyLong_AsLong(gpiolist);
#else
	if (PyInt_Check(gpiolist)) {
		gpioport = (int)PyInt_AsLong(gpiolist);
#endif
		if (PyErr_Occurred())
			return NULL;
		gpiolist = NULL;
	} else if (PyList_Check(gpiolist)) {
	// do nothing
	} else if (PyTuple_Check(gpiolist)) {
		gpiotuple = gpiolist;
		gpiolist = NULL;
	} else {
		PyErr_SetString(PyExc_ValueError, "gpioport must be an integer or list/tuple of integers");
		return NULL;
	}

#if PY_MAJOR_VERSION >= 3
	if (PyLong_Check(valuelist)) {
		value = (int)PyLong_AsLong(valuelist);
#else
	if (PyInt_Check(valuelist)) {
		value = (int)PyInt_AsLong(valuelist);
#endif
		if (PyErr_Occurred())
			return NULL;
		valuelist = NULL;
	} else if (PyList_Check(valuelist)) {
	// do nothing
	} else if (PyTuple_Check(valuelist)) {
		valuetuple = valuelist;
		valuelist = NULL;
	} else {
		PyErr_SetString(PyExc_ValueError, "Value must be an integer/boolean or a list/tuple of integers/booleans");
		return NULL;
	}

	if (gpiolist)
		gpiocount = PyList_Size(gpiolist);
	if (gpiotuple)
		gpiocount = PyTuple_Size(gpiotuple);
	if (valuelist)
		valuecount = PyList_Size(valuelist);
	if (valuetuple)
		valuecount = PyTuple_Size(valuetuple);
	if ((gpiocount != -1 && gpiocount != valuecount && valuecount != -1) || (gpiocount == -1 && valuecount != -1)) {
		PyErr_SetString(PyExc_RuntimeError, "Number of gpioports != number of values");
		return NULL;
	}

	if (gpiocount == -1) {
		if (!output_py(gpioport, value))
			return NULL;
		Py_RETURN_NONE;
   }

	for (i=0; i<gpiocount; i++) {
		// get gpioport number
		if (gpiolist) {
			if ((tempobj = PyList_GetItem(gpiolist, i)) == NULL) {
				return NULL;
		 }
		} else { // assume gpiotuple
			if ((tempobj = PyTuple_GetItem(gpiotuple, i)) == NULL) {
				return NULL;
			}
		}

#if PY_MAJOR_VERSION >= 3
	if (PyLong_Check(tempobj)) {
		gpioport = (int)PyLong_AsLong(tempobj);
#else
	if (PyInt_Check(tempobj)) {
		gpioport = (int)PyInt_AsLong(tempobj);
#endif
	if (PyErr_Occurred())
		return NULL;
	} else {
		PyErr_SetString(PyExc_ValueError, "gpioport must be an integer");
		return NULL;
	}

	// get value
	if (valuecount > 0) {
			if (valuelist) {
				if ((tempobj = PyList_GetItem(valuelist, i)) == NULL) {
					return NULL;
			}
			} else { // assume valuetuple
				if ((tempobj = PyTuple_GetItem(valuetuple, i)) == NULL) {
					return NULL;
				}
			}
#if PY_MAJOR_VERSION >= 3
			if (PyLong_Check(tempobj)) {
				value = (int)PyLong_AsLong(tempobj);
#else
			if (PyInt_Check(tempobj)) {
				value = (int)PyInt_AsLong(tempobj);
#endif
				if (PyErr_Occurred())
					return NULL;
			} else {
				PyErr_SetString(PyExc_ValueError, "Value must be an integer or boolean");
				return NULL;
			}
		}
		if (!output_py(gpioport, value))
			return NULL;
	}

	Py_RETURN_NONE;
}

// python function value = input_py(gpioport)
static PyObject *py_input_gpio(PyObject *self, PyObject *args)
{
	int gpioport = -1;
	unsigned int gpiooffset = 0;
	PyObject *value;

	if (!PyArg_ParseTuple(args, "i", &gpioport))
		return NULL;

	if (get_gpio_offset(&gpioport, &gpiooffset))
		return NULL;

	// check gpioport is set up as an input or output
	if (gpio_direction[gpioport] != INPUT && gpio_direction[gpioport] != OUTPUT)
	{
		PyErr_SetString(PyExc_RuntimeError, "You must setup() the GPIO gpioport first");
		return NULL;
	}

	if (input_py(gpioport)) {
		value = Py_BuildValue("i", HIGH);
	} else {
		value = Py_BuildValue("i", LOW);
	}
	return value;
}

static const char moduledocstring[] = "Python GPIO module for VisionFive";

PyMethodDef sfv_gpio_methods[] = {
	{"setup", (PyCFunction)py_setup_gpioport, METH_VARARGS | METH_KEYWORDS, "Setup direction"},
	{"cleanup", (PyCFunction)py_cleanup, METH_VARARGS | METH_KEYWORDS, "set default."},
	{"output", py_output_gpio, METH_VARARGS, "Output to a GPIO gpioport or list of gpioports\ngpioport - either board pin number or BCM number depending on which mode is set.\nvalue   - 0/1 or False/True or LOW/HIGH"},
	{"input", py_input_gpio, METH_VARARGS, "Input from a GPIO gpioport.	Returns HIGH=1=True or LOW=0=False\ngpioport - either board pin number or BCM number depending on which mode is set."},
	{NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION > 2
static struct PyModuleDef sfvgpiomodule = {
	PyModuleDef_HEAD_INIT,
	"VisionFive._gpio",      // name of module
	moduledocstring,
	-1,
	sfv_gpio_methods
};
#endif

#if PY_MAJOR_VERSION > 2
PyMODINIT_FUNC PyInit__gpio(void)
#else
PyMODINIT_FUNC init_gpio(void)
#endif
{
	int i;
	PyObject *module = NULL;

#if PY_MAJOR_VERSION > 2
	if ((module = PyModule_Create(&sfvgpiomodule)) == NULL)
		return NULL;
#else
	if ((module = Py_InitModule3("VisionFive._gpio", sfv_gpio_methods, moduledocstring)) == NULL)
		return;
#endif

	define_py_constants(module);

	for (i=0; i<49; i++)
		gpio_direction[i] = -1;

	// detect board type
	if (get_vf_info(&VisonFiveinfo))
	{
		PyErr_SetString(PyExc_RuntimeError, "This module can only be run on a VisionFive board!");
#if PY_MAJOR_VERSION > 2
		return NULL;
#else
		return;
#endif
	}

	if (VisonFiveinfo.revision == 7100) {
		GPIO2line = &GPIO2line_VisionFive_v1;
	} else if (VisonFiveinfo.revision == 7110) {
		GPIO2line = &GPIO2line_VisionFive_v2;
	}

	// Add PWM class
	if (PWM_init_PWMType() == NULL)
#if PY_MAJOR_VERSION > 2
		return NULL;
#else
		return;
#endif
	Py_INCREF(&PWMType);
	PyModule_AddObject(module, "PWM", (PyObject*)&PWMType);

#if PY_MAJOR_VERSION < 3
	if (!PyEval_ThreadsInitialized())
		PyEval_InitThreads();
#endif

#if PY_MAJOR_VERSION > 2
	return module;
#else
	return;
#endif
}
