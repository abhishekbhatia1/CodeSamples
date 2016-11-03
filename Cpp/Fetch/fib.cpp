#include <iostream>

int main()
{
    // Don't be afraid to make changes!!
    int num_elements;
    std::cin >> num_elements;
    int* arr = new int[num_elements];

    // Input
    for (int i = 0; i < num_elements; i++)
    {
        std::cin >> arr[i];
    }

    //TODO remove hard coded example and solve the problem
    int arr_fb[60];
    arr_fb[0] = 0;
    arr_fb[1] = 1;

    for (int i = 2; i< 60; i++)
    {
        arr_fb[i] = arr_fb[i - 1] + arr_fb[i - 2];
    }

    // Output
    int j;
    for (int i = 0; i < num_elements; i++)
    {
        if (arr[i] == 0)
        {
            std::cout << 1 << std::endl;
            continue;
        }
        for (int j = 2; j < 59; j++)
        {
                if (arr_fb[j] == arr[i])
                {
                    std::cout << arr_fb[j + 1] << std::endl;
                    break;
                }
                else if (arr_fb[j] > arr[i])
                {
                    std::cout << arr_fb[j] << std::endl;
                    break;
                }
                
        }
    }

    delete[] arr;
    return 0;
}
