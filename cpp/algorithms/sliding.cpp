#include "algorithms.hpp"
#include <climits>

using namespace std;

// Sliding window implementation to find the minimal length of a contiguous subarray
// of which the sum is at least target. Returns 0 if no such subarray exists.
// Time Complexity: O(n)
int minSubArrayLenSliding(const vector<int>& nums, int target) {
  int n = nums.size();
  int left = 0, sum = 0, minLength = INT_MAX;

  for (int right = 0; right < n; ++right) {
      sum += nums[right];

      while (sum >= target) {
          minLength = min(minLength, right - left + 1);
          sum -= nums[left];
          ++left;
      }
  }

  return (minLength == INT_MAX) ? 0 : minLength;
}