all: hw2

hw2: binary_search.o sieve.o hw2.cpp
	g++ hw2.cpp binary_search.o sieve.o -o hw2 --std=c++11

binary_search.o: binary_search.cpp
	g++ -c binary_search.cpp -o binary_search.o --std=c++11

sieve.o: sieve.cpp
	g++ -c sieve.cpp -o sieve.o --std=c++11

clean:
	rm -rf hw2 *.o
