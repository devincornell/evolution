from distutils.core import setup
from Cython.Build import cythonize
import glob



setup(
    name='basics_cython', 
    ext_modules = cythonize(["*.pyx"], language_level = "3")
)
