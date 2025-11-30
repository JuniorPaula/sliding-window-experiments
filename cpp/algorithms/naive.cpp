#include "algorithms.hpp"
#include <climits>

using namespace std;

// Native implementation to find the minimal length of a contiguous subarray
// of which the sum is at least target. Returns 0 if no such subarray exists.
// Time Complexity: O(n^2)
int minSubArrayLenNative(const vector<int>& arr, int target) {
  int n = arr.size();
  int minLength = INT_MAX;

  for (int start = 0; start < n; ++start) {
      long long sum = 0;
      for (int end = start; end < n; ++end) {
          sum += arr[end];
          if (sum >= target) {
              minLength = min(minLength, end - start + 1);
              break; // No need to check further for this start
          }
      }
  }

  return (minLength == INT_MAX) ? 0 : minLength;
}