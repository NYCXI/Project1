#!/usr/bin/python
#python version: 2.7.3
#Filename: SetupTestOMP.py
 
# Run as:  
#    python setup.py build_ext --inplace  
   
import os
import numpy as np
from os.path import join as pjoin
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy as np

# ext_module = cythonize("TestOMP.pyx")
ext_module = Extension(
                        "cpu_nms",
            ["cpu_nms.pyx"],
            extra_compile_args={'gcc': ["-Wno-cpp", "-Wno-unused-function"]},
            #include_dirs=[numpy_include]
            )

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [ext_module],
    #注意这一句一定要有，不然只编译成C代码，无法编译成pyd文件
    include_dirs=[np.get_include()]
)
