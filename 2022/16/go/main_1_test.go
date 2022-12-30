package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"
	"sync"
	"testing"
	"time"
)

func setup(testMode bool) (*CaveNetwork, map[string]int64) {
	input_file := "./input.txt"
	if testMode {
		input_file = "./test_input.txt"
	}
	input, err := readInput(input_file)
	if err != nil {
		log.Fatal("Failed to read the test data.")
	}

	caves := decodeInput(input)
	caveDirectory := map[string]int64{}
	for label, cave := range caves {
		caveDirectory[label] = cave.Id
	}

	valves := cavesWithValves(caves)

	return newCaveNetwork(
		buildCaveNetwork(caves),
		valves,
	), caveDirectory
}

func BenchmarkWalking(b *testing.B) {
	cn, caveDirectory := setup(false)

	start := time.Now()
	var steps int
	for i := 0; i < 1000000; i++ {
		_, steps = cn.travel(caveDirectory["AA"], caveDirectory["VX"])
	}
	b.Logf("Time taken: %v", time.Since(start))
	if steps == -1 {
		b.Fail()
	}
}

func BenchmarkMappingMap(b *testing.B) {
	cn, caveDirectory := setup(false)

	theMap := map[string]map[string]int{}

	for room := range caveDirectory {
		for otherRoom := range caveDirectory {
			if room == otherRoom {
				continue
			}
			_, steps := cn.travel(caveDirectory[room], caveDirectory[otherRoom])
			inner := map[string]int{otherRoom: steps}
			theMap[room] = inner
		}
	}

	start := time.Now()
	var steps int
	for i := 0; i < 1000000; i++ {
		steps = theMap["AA"]["XV"]
	}
	b.Logf("Time taken: %v", time.Since(start))
	if steps == -1 {
		b.Fail()
	}
}

func BenchmarkMappingString(b *testing.B) {
	cn, caveDirectory := setup(false)

	theMap := map[string]int{}

	for room := range caveDirectory {
		for otherRoom := range caveDirectory {
			if room == otherRoom {
				continue
			}
			_, steps := cn.travel(caveDirectory[room], caveDirectory[otherRoom])
			theMap[fmt.Sprintf("%s,%s", room, otherRoom)] = steps
		}
	}

	start := time.Now()
	var steps int
	for i := 0; i < 1000000; i++ {
		steps = theMap["AA,VX"]
	}
	b.Logf("Time taken: %v", time.Since(start))
	if steps == -1 {
		b.Fail()
	}
}

// func TestCompletes(t *testing.T) {
// 	cn, caveDirectory := setup(false)

// 	theMap := map[string]int{}

// 	for room := range caveDirectory {
// 		for otherRoom := range caveDirectory {
// 			if room == otherRoom {
// 				continue
// 			}
// 			_, steps := cn.travel(caveDirectory[room], caveDirectory[otherRoom])
// 			theMap[fmt.Sprintf("%s,%s", room, otherRoom)] = steps
// 		}
// 	}

// 	totalSteps := 0
// 	for _, id := range testSample {
// 		totalSteps = totalSteps + theMap[caveDirectory[]]
// 	}
// }

func TestTheMapListings(t *testing.T) {
	cn, caveDirectory := setup(false)

	theMap := map[string]int{}

	for room := range caveDirectory {
		for otherRoom := range caveDirectory {
			if room == otherRoom {
				continue
			}
			_, steps := cn.travel(caveDirectory[room], caveDirectory[otherRoom])
			theMap[fmt.Sprintf("%d,%d", caveDirectory[room], caveDirectory[otherRoom])] = steps
		}
	}

	totalSteps := 0
	for idx, _ := range testSample {
		if idx+1 == len(testSample) {
			break
		}
		totalSteps = totalSteps + theMap[fmt.Sprintf("%d,%d", testSample[idx], testSample[idx+1])]
	}

	t.Logf("Total Steps: %d\n", totalSteps)
}

// func TestWalker(t *testing.T) {
// 	cn, caveDirectory := setup(false)

// 	theMap := map[string][]int{}

// 	for room := range caveDirectory {
// 		for otherRoom := range caveDirectory {
// 			if room == otherRoom {
// 				continue
// 			}
// 			_, steps := cn.travel(caveDirectory[room], caveDirectory[otherRoom])
// 			valuePressure := cn.nodeFlowRate(caveDirectory[otherRoom])
// 			theMap[mapName(caveDirectory[room], caveDirectory[otherRoom])] = []int{steps, valuePressure}
// 		}
// 	}

// 	dataChan := make(chan []int64, 1)
// 	wgReader := &sync.WaitGroup{}
// 	paths := [][]int64{}

// 	wgReader.Add(1)
// 	go func() {
// 		for path := range dataChan {
// 			paths = append(paths, path)
// 		}
// 		wgReader.Done()
// 	}()

// 	walkerWithPressure(
// 		dataChan,
// 		theMap,
// 		caveDirectory["AA"],
// 		testSample,
// 		30,
// 		[]int64{},
// 		0,
// 	)
// 	close(dataChan)
// 	wgReader.Wait()

// 	possiblePaths := map[string][]int64{}
// 	for _, p := range paths {
// 		possiblePaths[compactor(p)] = p
// 	}

// 	possibleCount := 0
// 	for k, v := range possiblePaths {
// 		t.Log(k, "->", v)
// 		possibleCount++
// 	}

// 	t.Log("AA=", caveDirectory["AA"])
// 	t.Log("PossibleCount: ", possibleCount)

// }

func TestPressureWalker(t *testing.T) {
	cn, caveDirectory := setup(true)

	theMap := map[string][]int{}

	for room := range caveDirectory {
		for otherRoom := range caveDirectory {
			if room == otherRoom {
				continue
			}
			_, travelTime := cn.travel(caveDirectory[room], caveDirectory[otherRoom])
			valuePressure := cn.nodeFlowRate(caveDirectory[otherRoom])
			theMap[mapName(caveDirectory[room], caveDirectory[otherRoom])] = []int{travelTime, valuePressure}
		}
	}

	dataChan := make(chan walkedPath, 1)
	wgReader := &sync.WaitGroup{}
	paths := []walkedPath{}

	wgReader.Add(1)
	go func() {
		for path := range dataChan {
			paths = append(paths, path)
		}
		wgReader.Done()
	}()

	walkerWithPressure(
		dataChan,
		theMap,
		cn,
		caveDirectory["AA"],
		cn.roomsWithWorkingValves,
		30,
		[]int64{caveDirectory["AA"]},
		0,
	)
	close(dataChan)
	wgReader.Wait()

	possiblePaths := map[string]int{}
	for _, wp := range paths {
		possiblePaths[compactor(wp.path)] = wp.pressure
	}

	possibleCount := 0
	highestPressure := 0
	highestPath := ""
	for k, v := range possiblePaths {
		if v > highestPressure {
			highestPath = k
			highestPressure = v
		}
		possibleCount++
	}

	realPath := ""
	for _, v := range strings.Split(highestPath, ",") {
		n, _ := strconv.Atoi(v)
		realPath = realPath + " < " + cn.nodeLabel(int64(n))
	}

	t.Log("AA=", caveDirectory["AA"])
	t.Log("PossibleCount: ", possibleCount)
	t.Log("HighestPath:", highestPath, realPath)
	t.Log("HighestPressure:", highestPressure)

}
