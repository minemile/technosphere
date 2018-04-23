all: bigint
	./bigint.o

bigint: bigint.cpp
	g++ bigint.cpp -o bigint.o --std=c++14

vector: vector.hpp
	g++ vector.hpp -o vector.o --std=c++14

clean:
	rm -rf *.o
