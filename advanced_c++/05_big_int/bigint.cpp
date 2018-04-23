#include <algorithm>
#include <cmath>
#include <iostream>
#include "vector.hpp"

class BigInt {
   public:
    BigInt() : sign{true} {}

    // from string
    BigInt(std::string str) {
        if (std::stoi(str) < 0) {
            sign = negative;
            str = str.substr(1);
        }
        for (size_t i = 0; i < str.size(); i++) {
            number.push_back(str[i] - '0');
        }
        std::reverse(number.begin(), number.end());
    }
    // copy cons
    BigInt(const BigInt& other) : number{other.number}, sign{other.sign} {}

    BigInt(const IntVector& v, const bool _sign) : number{v}, sign{_sign} {}

    BigInt operator+(const BigInt& rhs) const {
        IntVector tmp_num;
        const int r_size = rhs.number.size();
        const int l_size = number.size();
        int k = 0;
        for (int j = 0; j < std::max(r_size, l_size); j++) {
            int l_num = j < l_size ? number[j] : 0;
            int r_num = j < r_size ? rhs.number[j] : 0;
            tmp_num.push_back((l_num + r_num + k) % base);
            k = floor((l_num + r_num) / base);
        }
        tmp_num.push_back(k);
        BigInt tmp(tmp_num, rhs.sign);
        tmp.clean_leading_zeros();
        return tmp;
    }

    BigInt operator-(const BigInt& rhs) const {
        IntVector tmp_num;
        const int r_size = rhs.number.size();
        const int l_size = number.size();
        int k = 0;
        IntVector left = number;
        IntVector right = rhs.number;
        if (*this < rhs) {
            std::swap(left, right);
        }
        for (int j = 0; j < std::max(r_size, l_size); j++) {
            int l_num = j < l_size ? left[j] : 0;
            int r_num = j < r_size ? right[j] : 0;
            tmp_num.push_back((base + ((l_num - r_num + k) % base)) % base);
            k = floor(((float)l_num - r_num + k) / base);
        }
        BigInt tmp(tmp_num, positive);
        tmp.clean_leading_zeros();
        return tmp;
    }

    bool operator<(const BigInt& rhs) const {
        if (sign == positive && rhs.sign == negative) return false;
        if (sign == negative && rhs.sign == positive) return true;
        const int r_size = rhs.number.size();
        const int l_size = number.size();

        if (l_size > r_size)
            return false;
        else if (l_size < r_size)
            return true;

        for (int i = r_size - 1; i >= 0; i--) {
            if (number[i] > rhs.number[i])
                return false;
            else if (number[i] < rhs.number[i])
                return true;
        }
        return false;
    }

    bool operator==(const BigInt& rhs) const {
        const size_t r_size = rhs.number.size();
        const size_t l_size = number.size();
        if (r_size != l_size || sign != rhs.sign) return false;
        if (&rhs == this) return true;
        for (size_t i = 0; i < r_size; i++) {
            if (number[i] != rhs.number[i]) return false;
        }
        return true;
    }

    bool operator>(const BigInt& rhs) const { return !(*this < rhs); }

    bool operator<=(const BigInt& rhs) const {
        return (*this == rhs) && (*this < rhs);
    }

    bool operator>=(const BigInt& rhs) const { return !(*this <= rhs); }

    void print() {
        // std::reverse(number.begin(), number.end());
        for (size_t i = 0; i < number.size(); i++) {
            std::cout << number[i];
        }
        std::cout << std::endl;
    }

   private:
    void clean_leading_zeros() {
        for (size_t i = number.size() - 1; number[i] == 0 && i != 0; i--) {
            std::cout << number[i];
            number.pop_back();
        }
    }

    IntVector number;  // invariant - should be always reversed
    bool sign;
    const static int base = 10;

    enum { positive = true, negative = false };
};

int main() {
    BigInt num1("12");
    BigInt num2("30");
    std::cout << "NUM1 < NUM2: " << (num1 < num2) << std::endl;
    BigInt num3 = num1 + num2;
    std::cout << "NUM1 + NUM2" << std::endl;
    num3.print();
    BigInt num4 = num1 - num2;
    std::cout << "NUM1 - NUM2" << std::endl;
    num4.print();
}
