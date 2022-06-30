from distutils.core import setup
from Cython.Build import cythonize
import glob



setup(
    name='mase', 
    ext_modules = cythonize(["mase/*.pyx"], language_level = "3", language="c++")
)
