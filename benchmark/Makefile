
all: build docs


build: 
	python setup.py build_ext --inplace

docs: 
	-mkdir docs
	-cython -a *.pyx
	-mv *.html docs

clean: 
	-rm -r build
	-rm -r docs
	-rm *.so
	-rm *.c
	

