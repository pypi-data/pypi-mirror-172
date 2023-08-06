#include <stdio.h>
#include <Python.h>

void c_print_fib(int n);

void c_print_fib(int n)
{
    // helper function
    int c_fib(int n)
    {
        if (n <= 1)
            return n;
        return c_fib(n - 1) + c_fib(n - 2);
    }

    // print sequence
    for (int i = 0; i < n; i++)
    {
        int cur_fib = c_fib(i);
        if (i == n - 1)
        {
            printf("%d\n", cur_fib);
        }
        else
        {
            printf("%d, ", cur_fib);
        }
    }
}


// wrap c-function into a python object
static PyObject *py_print_fib(PyObject *self, PyObject *args) {
    // declare pointer
    int *n = NULL;

    // Parse arguments - expects the integer to be mapped to n
    if (!PyArg_ParseTuple(args, "i", &n)) {
        return NULL;
    }
    c_print_fib(n);
    
    return PyLong_FromLong(0);
}


// specify the function name that we call in Python
static PyMethodDef SimpleFibMethods[] = {
    {
        "print_fib", // function name that we are calling from python
        py_print_fib, // refer to the functino wrapped above
        METH_VARARGS, // defines the signature: expect self and *args from python
        "Function for displaying Fibonacci sequence in c" // method description
    }, 
    {NULL, NULL, NULL, NULL}
};


// create module definition where we register module name, description and list of methods
static struct PyModuleDef simplefibmodule = {
    PyModuleDef_HEAD_INIT, // required for creating a PyModuleDef
    "simplefib", // name of module                             
    "C library for displaying Fibonacci sequence", // description of module
    -1, // memory needed, doesn’t support sub-interpreters                                 
    SimpleFibMethods // refers to the list of methods
};


// Initialization function that creates our module from the Module definition
PyMODINIT_FUNC PyInit_simplefib(void) {
    return PyModule_Create(&simplefibmodule);
};
