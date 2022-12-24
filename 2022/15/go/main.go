package main

import (
	"fmt"
	"regexp"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/barkimedes/go-deepcopy"
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
	sx       int64
	sy       int64
	bx       int64
	by       int64
	distance int64
	coverage map[int64][]int64
}

func newSignal(sx, sy, bx, by int64) *signal {
	s := &signal{
		sx:       sx,
		sy:       sy,
		bx:       bx,
		by:       by,
		coverage: map[int64][]int64{},
	}
	s.setDistance()
	return s
}

func (sig *signal) setDistance() {
	sig.distance = distance(sig.sx, sig.sy, sig.bx, sig.by)
}

func (sig *signal) generateCoverage() {
	coverRaw := map[int64][]int64{}
	current := map[string]int64{"x": sig.sx, "y": sig.sy}

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

func positive(in int64) int64 {
	if in < 0 {
		return in * -1
	}
	return in
}

func distance(sx, sy, rx, ry int64) int64 {
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

func atoi64(in string) int64 {
	i, _ := strconv.ParseInt(in, 10, 64)
	return i
}

func digest_input(input string) []*signal {
	output := make([]*signal, 0)

	matcher := regexp.MustCompile(`x=(?P<sensor_x>-?[0-9]+), y=(?P<sensor_y>-?[0-9]+): closest beacon is at x=(?P<beacon_x>-?[0-9]+), y=(?P<beacon_y>-?[0-9]+)`)
	for _, line := range strings.Split(input, "\n") {
		// matches := make(map[string]string)
		m := matcher.FindStringSubmatch(line)
		m1 := atoi64(m[1])
		m2 := atoi64(m[2])
		m3 := atoi64(m[3])
		m4 := atoi64(m[4])
		output = append(output, newSignal(m1, m2, m3, m4))
	}
	return output
}

type mapWriter struct {
	id   int64
	data []string
}

func limitedGid(limit int64) map[int64][]string {
	output := map[int64][]string{}
	fmt.Println("Building template")

	slicer := func(limit int64) []string {
		templateSlice := make([]string, limit)
		var idx int64
		for idx = 0; idx < limit; idx++ {
			templateSlice[idx] = "x"
		}
		return templateSlice
	}

	fmt.Println("Setup queue")
	wg := sync.WaitGroup{}
	wgMapWriter := sync.WaitGroup{}

	keysChan := make(chan int64, runtime.NumCPU()-1)

	mapWriterQueue := make(chan *mapWriter, 1)

	wgMapWriter.Add(1)
	go func(in chan *mapWriter) {
		for payload := range in {
			output[payload.id] = payload.data
		}
		wgMapWriter.Done()
	}(mapWriterQueue)

	wg.Add(1)
	go func(in chan int64, out chan *mapWriter) {
		for id := range in {
			wg.Add(1)
			go func(id int64, out chan *mapWriter) {
				if id%1000 == 0 {
					println("Got ID:", id)
				}
				out <- &mapWriter{
					id:   id,
					data: slicer(limit),
				}
				wg.Done()
			}(id, out)
		}
		wg.Done()
	}(keysChan, mapWriterQueue)

	var idx int64
	for idx = 0; idx < limit; idx++ {
		keysChan <- idx
	}
	close(keysChan)
	fmt.Println("Waiting for grid.")
	wg.Wait()
	close(mapWriterQueue)
	wgMapWriter.Wait()
	return output
}

func testString(limit int64) {
	fmt.Println("Starting Generator")
	tStart := time.Now()
	templateSlice := make([]string, limit)
	var idx int64
	for idx = 0; idx < limit; idx++ {
		templateSlice[0] = "x"
	}
	tStop := time.Since(tStart)
	fmt.Println("time:", tStop)

	templateSlice[limit-100000] = "."

	fmt.Println("Starting finder")
	tStart = time.Now()
	for x, v := range templateSlice {
		if v == "." {
			fmt.Printf("Found at %d,%d\n", x, 1)
		}
	}
	tStop = time.Since(tStart)
	fmt.Println("time:", tStop)

	fmt.Println("Starting deepcopy")
	tStart = time.Now()
	DCtemplateSlice := deepcopy.MustAnything(templateSlice).([]string)

	tStop = time.Since(tStart)
	fmt.Println("time:", tStop)

	templateSlice[limit-100000] = "."

	fmt.Println("Starting finder")
	tStart = time.Now()
	for x, v := range DCtemplateSlice {
		if v == "." {
			fmt.Printf("Found at %d,%d\n", x, 1)
		}
	}
	tStop = time.Since(tStart)
	fmt.Println("time:", tStop)
}

type worker struct {
	yAxisQueue chan int64
	output     chan []int64
	f          func(int64) ([][]int64, bool)
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
func findDeadZones(signals []*signal, limit int64, testMode bool) [][]int64 {
	found := [][]int64{}

	// Queues
	yAxisQueue := make(chan int64, 100)
	zoneFoundQueue := make(chan []int64, 1)

	// WaitGroups
	wgFeeder := sync.WaitGroup{}
	wgZoneProcessing := sync.WaitGroup{}
	wgWriter := sync.WaitGroup{}

	// Finder Functions
	finder := func(y int64) ([][]int64, bool) {
		output := [][]int64{}
		var x int64
		for x = 0; x <= limit; x++ {
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
				output = append(output, []int64{x, y})
			}
		}
		return output, len(output) > 0
	}

	// Start filling the y queue for the workers
	wgFeeder.Add(1)
	go func(feeder chan int64) {
		var y int64
		for y = 0; y <= limit; y++ {
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
	go func(foundQ chan []int64) {
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

	//deadZones := findDeadZones(signals, 20, true)
	deadZones := findDeadZones(signals, 4000000, false)
	fmt.Println(deadZones)
}
