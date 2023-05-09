from distutils.core import setup
from Cython.Build import cythonize
import glob



setup(
    name='mase', 
    ext_modules = cythonize(["mase/position/*.pyx"], language="c++", compiler_directives={'language_level' : "3"})
)
