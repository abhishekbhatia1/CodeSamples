#include <iostream>
#include <stdlib.h>
#include <string>
#include <vector>

// Main method, most your code should go here
int main()
{
  // Load in the grid and initialize the output
  int size, tmp, out = 0;
  std::cin >> size;
  int arr[size][size];
  for (int i = 0; i < size; i++)
      for (int j = 0; j < size; j++)
          std::cin >> arr[i][j];
  
  for (int i = 0; i < size; i++)
  {
      for (int j = 0; j < size; j++)
      {
          out = 0;
          if (i-1 >= 0)
          {
              out = out + arr[i-1][j];
              if (j-1 >= 0 )
                  out = out + arr[i-1][j-1];
              if (j+1 < size)
                  out = out + arr[i-1][j+1];
          }
          if (i+1 < size)
          {
              out = out + arr[i+1][j];
              if (j-1 >= 0 )
                  out = out + arr[i+1][j-1];
              if (j+1 < size)
                  out = out + arr[i+1][j+1];
          }
          if (j-1 >= 0)
              out = out + arr[i][j-1];
          if (j+1 < size)
              out = out + arr[i][j+1];
          std::cout << out << " ";
      }
      std::cout << std::endl;
  }

  return 0;
}
