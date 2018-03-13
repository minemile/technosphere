import numpy
from setuptools import setup, Extension

ext_modules = [Extension("cython_functions",
                         ["cython_functions.pyx"])
               ]

setup(
    ext_modules=ext_modules,
    include_dirs=[numpy.get_include()]
)
