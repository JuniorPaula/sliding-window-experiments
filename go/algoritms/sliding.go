package algoritms

import "math"

func MinSubArrayLenSliding(arr []int, target int) int {
	n := len(arr)
	left := 0
	sum := 0
	minLen := math.MaxInt32

	for right := 0; right < n; right++ {
		sum += arr[right]

		for sum >= target {
			if right-left+1 < minLen {
				minLen = right - left + 1
			}
			sum -= arr[left]
			left++
		}
	}

	if minLen == math.MaxInt32 {
		return 0
	}
	return minLen
}
