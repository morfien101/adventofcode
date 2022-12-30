package main

import (
	"sync"
	"testing"
	"time"
)

func TestPather(t *testing.T) {
	input_file := "./input.txt"
	input, err := readInput(input_file)
	if err != nil {
		t.Fatal("Failed to read the test data.")
	}

	caves := decodeInput(input)
	caveDirectory := map[string]int64{}
	for label, cave := range caves {
		caveDirectory[label] = cave.Id
	}

	valves := cavesWithValves(caves)

	cn := newCaveNetwork(
		buildCaveNetwork(caves),
		valves,
	)

	path, steps := cn.travel(caveDirectory["AA"], caveDirectory["VX"])
	t.Logf("Path: %v, Steps: %d", path, steps)
}

var testSample = []int64{2, 7, 8, 14, 17, 26, 27, 45, 46, 47, 50, 51, 54, 56, 58}

func BenchmarkPermDirect(b *testing.B) {
	perm := NewPermutation(testSample)
	limit := 1000000
	current := 0
	start := time.Now()
	for next := perm.Next(); next != nil; next = perm.Next() {
		current++
		if current == limit {
			break
		}
	}
	b.Logf("Reads: %d, time: %s", current, time.Since(start))
}

func BenchmarkPermQ10000(b *testing.B) {
	c := NewPermutationChan(testSample, 1000000, 10000)
	var count int64 = 0
	start := time.Now()
	for p := range c {
		if len(p) == 1 {
			b.Error("Oh No!")
		}
		count++
	}
	b.Logf("Reads: %d, time: %s", count, time.Since(start))
}

func BenchmarkPermMix(b *testing.B) {
	start := time.Now()
	c := NewPermutationBatchedChan(testSample, 1000000, 100, 10000)
	var count int64 = 0
	for pp := range c {
		for _, p := range pp {
			if len(p) == 1 {
				b.Error("Oh No!")
			}
			count++
		}
	}
	b.Logf("Reads: %d, time: %s", count, time.Since(start))
}

func BenchmarkPerms1Worker(b *testing.B) {
	start := time.Now()
	c := NewPermutationChan(testSample, 1000000, 10000)
	var count int64 = 0
	for p := range c {
		if len(p) == 1 {
			b.Error("Oh No!")
		}
		count++
	}
	b.Logf("Reads: %d, time: %s", count, time.Since(start))
}

func BenchmarkPerms2Workers(b *testing.B) {
	start := time.Now()
	c := NewPermutationChan(testSample, 1000000, 10000)
	var total int64 = 0
	wgWorkers := &sync.WaitGroup{}
	wgReader := &sync.WaitGroup{}

	results := make(chan int64, 1)

	workerCount := 8

	for i := 0; i <= workerCount; i++ {
		wgWorkers.Add(1)
		go func() {
			var count int64 = 0
			for p := range c {
				if len(p) == 1 {
					b.Error("Oh No!")
				}
				count++
			}
			results <- count
			wgWorkers.Done()
		}()
	}

	wgReader.Add(1)
	go func() {
		for r := range results {
			total = total + r
		}
		wgReader.Done()
	}()

	wgWorkers.Wait()
	close(results)
	wgReader.Wait()

	b.Logf("Reads: %d, time: %s", total, time.Since(start))
}
