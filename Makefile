
all: build docs

run: clean build
	python main_first.py

rebuild: clean build docs

build: 
	python setup.py build_ext --inplace

docs: 
	-mkdir docs
	-cython -a mase/position/*.pyx
	-mkdir mase/position/docs/
	-mv mase/position/*.html mase/position/docs/

clean: 
	-rm -r build
	-rm -r docs
	-rm mase/position/*.so
	-rm mase/position/*.c
	-rm mase/position/*.cpp
	
