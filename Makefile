
all: build docs

run: clean build
	python main_first.py

rebuild: clean build docs

build: 
	python setup.py build_ext --inplace

docs: 
	-mkdir docs
	-cython -a mase/*.pyx
	-mv mase/*.html docs

clean: 
	-rm -r build
	-rm -r docs
	-rm mase/*.so
	-rm mase/*.c
	-rm mase/*.cpp
	
