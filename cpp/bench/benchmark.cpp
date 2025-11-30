#include <iostream>
#include <vector>
#include <chrono>
#include <cstdlib>
#include <functional>

#include "../algorithms/algorithms.hpp"

using namespace std;
using namespace std::chrono;

long long measure(std::function<int()> func) {
 auto start = steady_clock::now();
 int result = func();
 auto end  = steady_clock::now();
 return duration_cast<nanoseconds>(end - start).count(); 
}

int main() {
  vector<int> sizes = {1000, 5000, 10000, 50000, 100000};

  cout << "n,algoritm,time_ns" << endl;

  for (int n : sizes) {
    auto arr = MakeArray(n);
    int target = n * 50;

    // Native algorithm benchmark - O(n^2)
    long long native_time = measure([&]() {
      return minSubArrayLenNative(arr, target);
    });
    cout << n << ",naive_cpp," << native_time << endl;

    // Sliding window algorithm benchmark - O(n)
    long long sliding_time = measure([&]() {
      return minSubArrayLenSliding(arr, target);
    });
    cout << n << ",sliding_cpp," << sliding_time << endl;
  }

  return 0;
}