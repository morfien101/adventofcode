package main

import (
	"fmt"
	"regexp"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"time"
)

type int64Set struct {
	mappings map[int64]bool
}

func newInt64Set() *int64Set {
	return &int64Set{
		mappings: map[int64]bool{},
	}
}

func (s *int64Set) add(i int64) {
	s.mappings[i] = true
}

func (s *int64Set) values() []int64 {
	size := len(s.mappings)
	out := make([]int64, size)
	idx := 0
	for key, _ := range s.mappings {
		out[idx] = key
		idx++
	}
	return out
}

type signal struct {
	sx       int
	sy       int
	bx       int
	by       int
	distance int
	coverage map[int][]int
}

func newSignal(sx, sy, bx, by int) *signal {
	s := &signal{
		sx:       sx,
		sy:       sy,
		bx:       bx,
		by:       by,
		coverage: map[int][]int{},
	}
	s.setDistance()
	return s
}

func (sig *signal) setDistance() {
	sig.distance = distance(sig.sx, sig.sy, sig.bx, sig.by)
}

func (sig *signal) generateCoverage() {
	coverRaw := map[int][]int{}
	current := map[string]int{"x": sig.sx, "y": sig.sy}

	coverRaw[current["y"]+sig.distance] = append(coverRaw[current["y"]+sig.distance], current["x"])
	coverRaw[current["y"]-sig.distance] = append(coverRaw[current["y"]-sig.distance], current["x"])
	coverRaw[current["y"]] = append(coverRaw[current["y"]], current["x"]-sig.distance)
	coverRaw[current["y"]] = append(coverRaw[current["y"]], current["x"]+sig.distance)

	for x_offset := sig.distance; x_offset > 0; x_offset-- {
		y_offset := sig.distance - x_offset

		coverRaw[current["y"]+y_offset] = append(coverRaw[current["y"]+y_offset], current["x"]+x_offset)
		coverRaw[current["y"]+y_offset] = append(coverRaw[current["y"]+y_offset], current["x"]-x_offset)
		coverRaw[current["y"]-y_offset] = append(coverRaw[current["y"]-y_offset], current["x"]+x_offset)
		coverRaw[current["y"]-y_offset] = append(coverRaw[current["y"]-y_offset], current["x"]-x_offset)
	}

	for key, value := range coverRaw {
		sig.coverage[key] = deDup(value)
	}
}

func positive(in int) int {
	if in < 0 {
		return in * -1
	}
	return in
}

func distance(sx, sy, rx, ry int) int {
	return positive(sx-rx) + positive(sy-ry)
}

func deDup[T string | int | int64](sliceList []T) []T {
	allKeys := make(map[T]bool)
	list := []T{}
	for _, item := range sliceList {
		if _, value := allKeys[item]; !value {
			allKeys[item] = true
			list = append(list, item)
		}
	}
	return list
}

func digest_input(input string) []*signal {
	output := make([]*signal, 0)

	matcher := regexp.MustCompile(`x=(?P<sensor_x>-?[0-9]+), y=(?P<sensor_y>-?[0-9]+): closest beacon is at x=(?P<beacon_x>-?[0-9]+), y=(?P<beacon_y>-?[0-9]+)`)
	for _, line := range strings.Split(input, "\n") {
		m := matcher.FindStringSubmatch(line)
		m1, _ := strconv.Atoi(m[1])
		m2, _ := strconv.Atoi(m[2])
		m3, _ := strconv.Atoi(m[3])
		m4, _ := strconv.Atoi(m[4])
		output = append(output, newSignal(m1, m2, m3, m4))
	}
	return output
}

type worker struct {
	yAxisQueue chan int
	output     chan []int
	f          func(int) ([][]int, bool)
	id         int
	wg         *sync.WaitGroup
}

func (w *worker) start() {
	for y := range w.yAxisQueue {
		coords, found := w.f(y)
		if found {
			for _, coord := range coords {
				w.output <- coord
			}
		}
	}
	w.wg.Done()
}

// Call this function
func findDeadZones(signals []*signal, limit int, testMode bool) [][]int {
	found := [][]int{}

	// Queues
	yAxisQueue := make(chan int, 100)
	zoneFoundQueue := make(chan []int, 1)

	// WaitGroups
	wgFeeder := sync.WaitGroup{}
	wgZoneProcessing := sync.WaitGroup{}
	wgWriter := sync.WaitGroup{}

	// Finder Functions
	finder := func(y int) ([][]int, bool) {
		fmt.Println("Checking y", y)
		output := [][]int{}
		for x := 0; x <= limit; x++ {
			withinZone := []bool{}
			for _, signal := range signals {
				currentDistance := distance(signal.sx, signal.sy, x, y)
				if testMode {
					if y == 11 && x == 14 || y == 11 && x == 13 {
						fmt.Println(x, y, "distances signal:", signal.distance, currentDistance, currentDistance <= signal.distance)
					}
				}
				withinZone = append(withinZone, currentDistance <= signal.distance)
			}
			found := true
			for _, covered := range withinZone {
				if covered {
					found = false
				}
			}
			if found {
				output = append(output, []int{x, y})
			}
		}
		return output, len(output) > 0
	}

	// Start filling the y queue for the workers
	wgFeeder.Add(1)
	go func(feeder chan int) {
		for y := 0; y <= limit; y++ {
			feeder <- y
		}
		wgFeeder.Done()
	}(yAxisQueue)

	// Start the workers to find the dead zones.
	for w := 0; w < runtime.NumCPU()-2; w++ {
		orc := &worker{
			yAxisQueue: yAxisQueue,
			output:     zoneFoundQueue,
			f:          finder,
			id:         w,
			wg:         &wgZoneProcessing,
		}
		wgZoneProcessing.Add(1)
		go orc.start()
	}

	wgWriter.Add(1)
	go func(foundQ chan []int) {
		for foundZone := range foundQ {
			found = append(found, foundZone)
		}
		wgWriter.Done()
	}(zoneFoundQueue)

	// Wait for the y axis generator to finish filling the queue
	wgFeeder.Wait()
	// Close it to signal to the zone finders that there is nothing more to do.
	close(yAxisQueue)
	// Wait for the zone processes to finish looking in all points
	wgZoneProcessing.Wait()
	// Close the queue for anything found to signal to the worker its finished.
	close(zoneFoundQueue)
	// wait for the found writer to finish
	wgWriter.Wait()

	return found
}

func mapReducer(signals []*signal, limit int) [][]int {
	wgFeeder := sync.WaitGroup{}
	wgLiner := sync.WaitGroup{}

	feederQ := make(chan int, 10)

	wgFeeder.Add(1)
	go func(feeder chan int) {
		for y := 0; y <= limit; y++ {
			feeder <- y
		}
		wgFeeder.Done()
	}(feederQ)

	for i := 0; i <= runtime.NumCPU()-2; i++ {
		wgLiner.Add(1)
		go func(y_axis chan int) {
			for y := range y_axis {
				if y == -1 {
					continue
				}
				line := map[int]bool{}
				for x := 0; x <= limit; x++ {
					line[x] = true
				}
			}
			wgLiner.Done()
		}(feederQ)
	}
	wgFeeder.Wait()
	close(feederQ)
	wgLiner.Wait()
	return [][]int{}
}

func sliceReducer(signals []*signal, limit int) [][]int {
	wgFeeder := sync.WaitGroup{}
	wgLiner := sync.WaitGroup{}

	feederQ := make(chan int, 10)

	wgFeeder.Add(1)
	go func(feeder chan int) {
		for y := 0; y <= limit; y++ {
			feeder <- y
		}
		wgFeeder.Done()
	}(feederQ)

	for i := 0; i <= runtime.NumCPU()-2; i++ {
		wgLiner.Add(1)
		go func(y_axis chan int) {
			for y := range y_axis {
				if y%10000 == 0 {
					fmt.Println("Y at", y)
				}
				line := make([]bool, limit+1)
				for x := 0; x <= limit; x++ {
					line[x] = true
				}
			}
			wgLiner.Done()
		}(feederQ)
	}
	wgFeeder.Wait()
	close(feederQ)
	wgLiner.Wait()
	return [][]int{}
}

func sorted(i, j int) (int, int) {
	if j >= i {
		return i, j
	}
	return j, i
}

func sliceReducerReal(signals []*signal, limit int) ([][]int, bool) {
	wgFeeder := sync.WaitGroup{}
	wgLiner := sync.WaitGroup{}
	wgWriter := sync.WaitGroup{}

	feederQ := make(chan int, 10)
	foundQ := make(chan []int, 1)

	found := [][]int{}

	wgFeeder.Add(1)
	go func(feeder chan int) {
		for y := 0; y <= limit; y++ {
			feeder <- y
		}
		wgFeeder.Done()
	}(feederQ)

	for i := 0; i <= runtime.NumCPU()-2; i++ {
		wgLiner.Add(1)
		go func(y_axis chan int, found chan []int) {
			for y := range y_axis {
				if y%10000 == 0 {
					fmt.Println("Y at", y)
				}
				line := make([]bool, limit+1)
				for _, s := range signals {
					// No co-ords in this line
					if len(s.coverage[y]) == 0 {
						continue
					}
					// Just a single cord in this line
					if len(s.coverage[y]) == 1 {
						line[s.coverage[y][0]] = true
						continue
					}
					// Get start stop of each coverage on the line
					min, max := sorted(s.coverage[y][0], s.coverage[y][1])
					if min < 0 {
						min = 0
					}
					if max > limit {
						max = limit
					}
					for x := min; x <= max; x++ {
						line[x] = true
					}
				}
				for x, covered := range line {
					if !covered {
						fmt.Println("Ding!", x, y)
						found <- []int{x, y}
					}
				}
			}
			wgLiner.Done()
		}(feederQ, foundQ)
	}

	wgWriter.Add(1)
	go func(foundQ chan []int) {
		for payload := range foundQ {
			found = append(found, payload)
		}
		wgWriter.Done()
	}(foundQ)

	wgFeeder.Wait()
	close(feederQ)
	wgLiner.Wait()
	close(foundQ)
	wgWriter.Wait()
	return found, len(found) > 0
}

func timeThis(f func()) {
	tStart := time.Now()
	f()
	fmt.Println(time.Since(tStart))
}

func main() {
	// signals := digest_input(test_input)
	signals := digest_input(input)
	generateCoverageQueue := make(chan *signal, runtime.NumCPU())
	wg := sync.WaitGroup{}

	wg.Add(1)
	go func(sigs chan *signal) {
		for s := range sigs {
			wg.Add(1)
			go func(s *signal) {
				s.generateCoverage()
				wg.Done()
			}(s)
		}
		wg.Done()
	}(generateCoverageQueue)

	for _, s := range signals {
		generateCoverageQueue <- s
	}
	close(generateCoverageQueue)
	wg.Wait()
	for id, s := range signals {
		fmt.Printf("-------- %d --------\n", id)
		fmt.Println("Distance:", s.distance)
		fmt.Printf("-------- %d --------\n", id)
	}

	// //deadZones := findDeadZones(signals, 20, true)
	// deadZones := findDeadZones(signals, 4000000, false)
	// fmt.Println(deadZones)
	// timeThis(
	// 	func() {
	// 		mapReducer(signals, 1000000)
	// 	},
	// )
	// timeThis(
	// 	func() {
	// 		sliceReducer(signals, 1000000)
	// 	},
	// )

	// coOrds, found := sliceReducerReal(signals, 20)
	coOrds, found := sliceReducerReal(signals, 4000000)
	if found {
		fmt.Println(coOrds)
	} else {
		fmt.Println("boo!")
	}
}
