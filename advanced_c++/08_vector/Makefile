all: test
	./check

vector: vector.cpp
	g++ -pedantic -Wall vector.cpp -o vector --std=c++14

test: check.cpp
	g++ check.cpp -o check --std=c++14
