package algoritms

import (
	"math/rand"
	"testing"
)

func makeArray(n int) []int {
	arr := make([]int, n)
	for i := range arr {
		arr[i] = rand.Intn(100) + 1
	}
	return arr
}

func BenchmarkNative_1e4(b *testing.B) {
	arr := makeArray(10000)
	target := 20000

	for b.Loop() {
		MinSubArrayLenNative(arr, target)
	}
}

func BenchmarkSliding_1e4(b *testing.B) {
	arr := makeArray(10000)
	target := 20000

	for b.Loop() {
		MinSubArrayLenSliding(arr, target)
	}
}
