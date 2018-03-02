#include <iostream>

bool* make_sieve(size_t n)
{
        bool* primes = new bool[n];
        primes[0] = primes[1] = false;
        for (size_t i = 2; i < n; i++) {
                primes[i] = true;
        }
        for (size_t i = 2; i * i < n; i++) {
                if (primes[i])
                {
                        for (size_t j = 2 * i; j < n; j += i) {
                                if (j % i == 0) primes[j] = false;
                        }
                }
        }
        return primes;
}
