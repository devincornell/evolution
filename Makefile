
all: build docs


build: 
	python setup.py build_ext --inplace

docs: 
	-mkdir docs
	-cython -a first/*.pyx
	-mv first/*.html docs

clean: 
	-rm -r build
	-rm -r docs
	-rm first/*.so
	-rm first/*.c
	-rm first/*.cpp
	

