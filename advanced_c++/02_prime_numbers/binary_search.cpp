#include <iostream>

int binary_search(const int* array, int number, int size, bool find_first_index)
{
        int left_bound = 0, mid = 0, right_bound = size - 1, result = -1;
        while(left_bound <= right_bound)
        {
                mid = (left_bound + right_bound) / 2;
                int cur_number = array[mid];
                if (cur_number == number)
                {
                        result = mid;
                        if (find_first_index) right_bound = mid - 1;
                        else left_bound = mid + 1;
                }
                else if (number > cur_number)
                        left_bound = mid + 1;
                else if (number < cur_number)
                        right_bound = mid - 1;
        }
        return result;
}
