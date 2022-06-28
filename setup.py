from distutils.core import setup
from Cython.Build import cythonize
import glob



setup(
    name='first_model', 
    ext_modules = cythonize(["first/*.pyx", "first/*.pyx"], language_level = "3", language="c++")
)
