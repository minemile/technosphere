#include <iostream>
#include "hw2.hpp"
#include "numbers.dat"

int main(int argc, char* argv[])
{
        if (argc % 2 == 0 || argc == 1) return -1;
        const size_t sieve_n = 100000;
        const bool* sieve = make_sieve(sieve_n);
        for (int i = 1; i < argc; i+=2) {
                int prime_count = 0;
                int start_index = binary_search(Data, std::atoi(argv[i]), Size, true);
                int end_index = binary_search(Data, std::atoi(argv[i+1]), Size, false);
                std::cout << "Start index: " << start_index << " End index: " << end_index << std::endl;
                if (start_index == -1 || end_index == -1)
                {
                        return -1;
                }
                for (int i = start_index; i <= end_index; i++) {
                        if (sieve[Data[i]])
                                prime_count += 1;
                }
                std::cout << prime_count << std::endl;
        }
}
