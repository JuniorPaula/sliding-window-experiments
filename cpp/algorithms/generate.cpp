#include "algorithms.hpp"
#include <cstdlib>

// Function to generate an array of given size with random integers
std::vector<int> MakeArray(int size) {
  std::vector<int> arr(size);
  for (int i = 0; i < size; ++i) {
      arr[i] = rand() % 100 + 1; // Random integers between 1 and 100
  }
  return arr;
}