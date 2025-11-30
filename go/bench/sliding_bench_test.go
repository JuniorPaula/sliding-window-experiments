package main

import (
	"swe/algoritms"
	"testing"
)

func BenchmarkNative_1e4(b *testing.B) {
	arr := algoritms.MakeArray(10000)
	target := 20000

	for b.Loop() {
		algoritms.MinSubArrayLenNaive(arr, target)
	}
}

func BenchmarkSliding_1e4(b *testing.B) {
	arr := algoritms.MakeArray(10000)
	target := 20000

	for b.Loop() {
		algoritms.MinSubArrayLenSliding(arr, target)
	}
}
