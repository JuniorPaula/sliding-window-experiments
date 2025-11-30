package algoritms

import "math/rand"

func MakeArray(n int) []int {
	arr := make([]int, n)
	for i := range arr {
		arr[i] = rand.Intn(100) + 1
	}
	return arr
}
