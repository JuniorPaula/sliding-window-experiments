package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"swe/algoritms"
	"time"
)

type Result struct {
	N      int
	Algo   string
	TimeNs int64
}

func measure(fn func() int) int64 {
	start := time.Now()
	_ = fn()
	return time.Since(start).Nanoseconds()
}

func main() {
	sizes := []int{1000, 5000, 10000, 50000, 100000}
	var results []Result

	for _, n := range sizes {
		arr := algoritms.MakeArray(n)
		target := n * 50

		// Measure Native - O(n^2)
		nativeTime := measure(func() int {
			return algoritms.MinSubArrayLenNaive(arr, target)
		})
		results = append(results, Result{N: n, Algo: "naive_go", TimeNs: nativeTime})

		// Measure Sliding Window - O(n)
		slidingTime := measure(func() int {
			return algoritms.MinSubArrayLenSliding(arr, target)
		})
		results = append(results, Result{N: n, Algo: "sliding_go", TimeNs: slidingTime})
	}

	// Create data directory if not exists
	_ = os.MkdirAll("../../data", os.ModePerm)

	file, err := os.Create("../../data/go_results.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	w := csv.NewWriter(file)
	defer w.Flush()

	// Write header
	_ = w.Write([]string{"n", "algorithm", "time_ns"})

	// Write results
	for _, r := range results {
		_ = w.Write([]string{
			fmt.Sprintf("%d", r.N),
			r.Algo,
			fmt.Sprintf("%d", r.TimeNs),
		})
	}

	fmt.Println("Results written to ../../data/go_results.csv")
}
