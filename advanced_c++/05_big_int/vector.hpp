#include <algorithm>
#include <iostream>

// very simple vector implementation
class IntVector {
   public:
    //default
    IntVector() : data{new int[10]}, capacity(10), _size(0) {}

    IntVector(const int* _data, const size_t __size) {
        _size = __size;
        capacity = mult * _size;
        data = new int[capacity];
        for (size_t i = 0; i < _size; i++) {
            data[i] = _data[i];
        }
    }

    //copy
    IntVector (const IntVector& v)
    {
      capacity = v.capacity;
      _size = v._size;
      data = new int[capacity];
      std::copy(v.begin(), v.end(), data);
    }

    //move const
    IntVector(IntVector&& moved)
    {
      capacity = moved.capacity;
      data = moved.data;
      moved.data =  nullptr;
    }

    //move assigment
    IntVector& operator=(IntVector&& moved)
    {
        if (this == &moved)
            return *this;
        delete[] data;
        data = moved.data;
        capacity = moved.capacity;
        
        moved.data_ = nullptr;
        return *this;
    }

    IntVector& operator=(const IntVector& v)
    {
      delete [] data;
      capacity = v.capacity;
      _size = v._size;
      data = new int[capacity];
      std::copy(v.begin(), v.end(), data);
      return *this;
    }

    void resize() {
        int* tmp = new int[mult * _size];
        std::copy(data, data + _size, tmp);
        delete[] data;
        data = tmp;
    }

    size_t size() const { return _size; }

    void push_back(const int elem) {
        if (_size == capacity) resize();
        data[_size++] = elem;
    }

    int pop_back() { return data[_size--]; }

    int& operator[](size_t i) {
        if (i < _size) {
            return data[i];
        }
        throw std::out_of_range("indx is not correct");
    }

    int operator[](size_t i) const {
        if (i < _size) {
            return data[i];
        }
        throw std::out_of_range("indx is not correct");
    }

    int* begin() const { return data; }
    int* begin() { return data; }

    int* end() const { return data + _size; }
    int* end() { return data + _size; }

    ~IntVector() {
        std::cout << "DELETING VECTOR" << std::endl;
        delete[] data;
    }

   private:
    int* data;
    size_t capacity;
    size_t _size;
    const static int mult = 2;
};

void test() {
    int* numbers = new int[2];
    numbers[0] = 1;
    numbers[1] = 2;
    IntVector a(numbers, 2);
    std::cout << "Number: " << a[1] << std::endl;
    a.push_back(3);
    std::cout << "Number: " << a[2] << std::endl;
}
