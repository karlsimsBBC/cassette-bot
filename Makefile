
build:
	python3 -m unittest
	pip3 install .

build_with_examples:
	./test
	pip3 install .