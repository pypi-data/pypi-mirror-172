from ctypes import *
import os
import sys

def print_fib(n):
    ext_lib.print_fib(n)

def fib(n):
    ext_lib.fib(n)

if sys.platform == 'darwin':  # mac
    SHEXT = 'dylib'
else:
    SHEXT = 'so'

ext_lib_path = "fib." + SHEXT
ext_lib = cdll.LoadLibrary(os.path.abspath(ext_lib_path))
print_fib(5)
