package algoritms

import "math"

func MinSubArrayLenNative(arr []int, target int) int {
	n := len(arr)
	minLen := math.MaxInt32

	for i := 0; i < n; i++ {
		sum := 0
		for j := i; j < n; j++ {
			sum += arr[j]
			if sum > target {
				if j-i+1 < minLen {
					minLen = j - i + 1
				}
				break
			}
		}
	}

	if minLen == math.MaxInt32 {
		return 0
	}

	return minLen
}
