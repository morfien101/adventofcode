package main

import (
	"encoding/base64"
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
	"runtime"
	"sort"
	"strconv"
	"strings"
	"sync"

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/path"
	"gonum.org/v1/gonum/graph/simple"
)

var (
	flagFile    = flag.String("f", "./input.txt", "Data file to read.")
	flagHelp    = flag.Bool("h", false, "Help menu.")
	flagVerbose = flag.Bool("V", false, "Verbose debug printing.")
)

func writeOutput(fileName string, data interface{}) error {
	fmt.Println(data)

	outputFile, err := os.OpenFile(fileName, os.O_RDWR+os.O_CREATE, 0660)
	if err != nil {
		return err
	}

	b64Enc := base64.NewEncoder(base64.RawStdEncoding, outputFile)
	_, err = b64Enc.Write([]byte(fmt.Sprint(data)))
	if err != nil {
		return err
	}

	return nil
}

func readInput(fileName string) (string, error) {
	input, err := os.ReadFile(fileName)
	if err != nil {
		return "", fmt.Errorf("error reading data. Error: %s", err)
	}
	return string(input), nil
}

func mustInt(i string) int {
	j, err := strconv.Atoi(i)
	if err != nil {
		panic(err)
	}
	return j
}

// This is too slow and consumes way to much memory in this problem.
// func permutation(xs []int64) (out [][]int64) {
// 	// Create a definition here because its used in recursion
// 	var rc func([]int64, int)
// 	rc = func(a []int64, k int) {
// 		if k == len(a) {
// 			out = append(out, append([]int64{}, a...))
// 		} else {
// 			for i := k; i < len(xs); i++ {
// 				a[k], a[i] = a[i], a[k]
// 				rc(a, k+1)
// 				a[k], a[i] = a[i], a[k]
// 			}
// 		}
// 	}
// 	rc(xs, 0)

// 	return out
// }

type Cave struct {
	Id            int64
	Label         string
	ValveFlowRate int
	TimeActivated int
	Connections   []string
}

func (c *Cave) ID() int64 {
	return c.Id
}

func buildCaveNetwork(caves map[string]*Cave) *simple.UndirectedGraph {
	network := simple.NewUndirectedGraph()

	for _, cave := range caves {
		for _, nextCave := range cave.Connections {
			if *flagVerbose {
				fmt.Printf("Link %s [%d] to %s [%d]\n", cave.Label, cave.Id, caves[nextCave].Label, caves[nextCave].Id)
			}
			network.SetEdge(network.NewEdge(cave, caves[nextCave]))
		}
	}

	return network
}

func cavesWithValves(caves map[string]*Cave) []int64 {
	out := []int{}
	for _, cave := range caves {
		if cave.ValveFlowRate > 0 {
			out = append(out, int(cave.ID()))
		}
	}
	sort.Ints(out)
	output := []int64{}
	for _, o := range out {
		output = append(output, int64(o))
	}
	return output
}

func decodeInput(input string) map[string]*Cave {
	caves := map[string]*Cave{}
	regexPattern := regexp.MustCompile(`Valve (?P<id>[A-Z]+).*=(?P<rate>[0-9]+);.*valve[s]? (?P<neighbors>.*)$`)
	for id, line := range strings.Split(input, "\n") {
		digestedLine := regexPattern.FindStringSubmatch(line)
		caves[digestedLine[1]] = &Cave{
			Id:            int64(id),
			Label:         digestedLine[1],
			ValveFlowRate: mustInt(digestedLine[2]),
			Connections:   strings.Split(digestedLine[len(digestedLine)-1], ", "),
		}
	}
	return caves
}

type CaveNetwork struct {
	network                *simple.UndirectedGraph
	roomsWithWorkingValves []int64
	routes                 path.AllShortest
}

func newCaveNetwork(
	network *simple.UndirectedGraph,
	roomsWithValves []int64,
) *CaveNetwork {
	return &CaveNetwork{
		network:                network,
		routes:                 path.DijkstraAllPaths(network),
		roomsWithWorkingValves: roomsWithValves,
	}
}

func (cn *CaveNetwork) nodeFlowRate(id int64) int {
	return cn.network.Node(id).(*Cave).ValveFlowRate
}

func (cn *CaveNetwork) travel(from int64, to int64) ([]graph.Node, int) {
	path, _, _ := cn.routes.Between(from, to)
	return path, len(path) - 1
}

func (cn *CaveNetwork) nodeLabel(id int64) string {
	return cn.network.Node(id).(*Cave).Label
}

func (cn *CaveNetwork) pathTester(roomMap map[string]int64, valveOrder chan []int64, outputChan chan int, wg *sync.WaitGroup) {
	var timeLeft int
	var currentSteamOutput int
	var currentRoom int64

	reset := func() {
		timeLeft = 30
		currentSteamOutput = 0
		currentRoom = roomMap["AA"]
	}

	for path := range valveOrder {
		if *flagVerbose {
			fmt.Println("Checking: ", path)
		}
		reset()
		for _, nextRoom := range path {
			_, steps := cn.travel(int64(currentRoom), nextRoom)
			timeLeft = timeLeft - steps
			if timeLeft <= 0 {
				break
			}
			currentSteamOutput = currentSteamOutput + (cn.network.Node(nextRoom).(*Cave).ValveFlowRate * timeLeft)
			currentRoom = nextRoom
		}
		if currentSteamOutput > 0 {
			outputChan <- currentSteamOutput
		}
	}
	wg.Done()
}

func rev(x []int64) {
	for i, j := 0, len(x)-1; i < j; i, j = i+1, j-1 {
		x[i], x[j] = x[j], x[i]
	}
}

func main() {
	flag.Parse()

	if *flagHelp {
		flag.PrintDefaults()
		os.Exit(1)
	}
	input, err := readInput(*flagFile)
	if err != nil {
		log.Fatal("Failed to read file.")
	}
	caves := decodeInput(input)
	caveDirectory := map[string]int64{}
	for label, cave := range caves {
		caveDirectory[label] = cave.Id
	}

	valves := cavesWithValves(caves)

	fmt.Println(valves)

	cn := newCaveNetwork(
		buildCaveNetwork(caves),
		valves,
	)

	pathsToTest := NewPermutationChan(valves, -1, 1)
	pathsTested := make(chan int, 1)
	wgWorkers := &sync.WaitGroup{}
	wgReader := &sync.WaitGroup{}

	for i := 0; i < (runtime.NumCPU()*3)-2; i++ {
		wgWorkers.Add(1)
		go cn.pathTester(caveDirectory, pathsToTest, pathsTested, wgWorkers)
	}

	wgReader.Add(1)
	var highestValue int
	go func(valuesChan chan int) {
		for payload := range valuesChan {
			if payload > highestValue {
				highestValue = payload
			}
		}
		wgReader.Done()
	}(pathsTested)

	wgWorkers.Wait()
	close(pathsTested)
	wgReader.Wait()

	writeOutput("output1.txt", fmt.Sprint(highestValue))

	// Create a go routine to work over each permutation in a worker pool.
	// Walk the path turning on the valves until either the time limit is reached
	// or all the values are open.
	// Calculate the units of pressure that you can disperse.
	// Get the max value and the path walked.
}

type walkedPath struct {
	path     []int64
	pressure int
}

func mapName(i, j int64) string {
	return fmt.Sprintf("%d,%d", i, j)
}

func popAt(i int, xs []int64) (int64, []int64) {
	y := xs[i]
	ys := append(xs[:i], xs[i+1:]...)
	return y, ys
}

func compactor(in []int64) string {
	s := []string{}
	for _, i := range in {
		s = append(s, strconv.Itoa(int(i)))
	}
	return strings.Join(s, ",")
}

func walker(theMap map[string][]int, current int64, valvesLeft []int64, stepsTaken int, path []int64, dataChan chan []int64) {
	newPath := append([]int64{current}, path...)
	for idx := range valvesLeft {
		nextValve, leftAfter := popAt(idx, valvesLeft)
		// Steps taken so far, +1 to open this valve, plus steps to get to the next room
		fmt.Println(theMap[mapName(current, nextValve)], mapName(current, nextValve))
		if nextValve == current {
			continue
		}
		stepsToNext := theMap[mapName(current, nextValve)][0] + stepsTaken + 1
		//fmt.Println(stepsToNext, path)
		// We need no more than 29 as we need at least 1 min to open the valve
		if stepsToNext < 29 {
			walker(theMap, nextValve, append([]int64{}, leftAfter...), stepsToNext, newPath, dataChan)
		} else {
			dataChan <- path
			return
		}
	}
}

func walkerWithPressure(
	dataChan chan walkedPath,
	theMap map[string][]int,
	cn *CaveNetwork,
	current int64,
	closedValves []int64,
	timeLeft int,
	path []int64,
	pressureReleased int,
) {
	//fmt.Println("Current valve:", current, "Closed valves", closedValves)
	for idx := range closedValves {
		// Reset the closed valves on each loop
		myClosedValves := append([]int64{}, closedValves...)
		// Reset the pressure on each loop
		myPressure := pressureReleased
		// Get the valve that we will no go to.
		nextValve, closedValvesToCheck := popAt(idx, myClosedValves)
		//fmt.Println("Next valve to get to:", nextValve, cn.nodeLabel(nextValve), "Still left to check:", closedValvesToCheck)

		// This is here to catch my stupid bugs.
		if nextValve == current {
			fmt.Println("Continue")
			continue
		}
		//fmt.Println(theMap[mapName(current, nextValve)], mapName(current, nextValve))

		travelTime := theMap[mapName(current, nextValve)][0]
		nextValvePressure := theMap[mapName(current, nextValve)][1]

		// Travel time plus a minute to open the valve
		checkTimeLeft := timeLeft - travelTime
		// Grab our own copy of the path followed.
		traveledPath := append([]int64{}, path...)

		if checkTimeLeft > 1 {
			// Add a minute to open the valve
			checkTimeLeft = checkTimeLeft - 1
			// How much pressure will this valve release.
			thisValvePressureReleased := checkTimeLeft * nextValvePressure
			// Add the next valve to the path followed.
			traveledPath = append(traveledPath, nextValve)
			//fmt.Println("Travel time:", travelTime, "time used with travel:", checkTimeLeft, "Walked Path:", traveledPath)
			//fmt.Println("Pressure before:", myPressure)
			myPressure = myPressure + thisValvePressureReleased
			//fmt.Println("Pressure After:", myPressure)
			//fmt.Println("Pressure released:", thisValvePressureReleased, "|", nextValvePressure, "over", checkTimeLeft)
		}

		// If we have no valves left to check
		// or
		// we have no time left. Stop traveling this path.
		if len(closedValvesToCheck) == 0 || checkTimeLeft <= 0 {
			wp := walkedPath{traveledPath, myPressure}
			dataChan <- wp
			//fmt.Println("Ship:", wp)
			return
		}

		// We still have time and valves.
		// Move on.
		walkerWithPressure(
			dataChan,
			theMap,
			cn,
			nextValve,
			// Use append to create a new slice to stop ref values
			append([]int64{}, closedValvesToCheck...),
			checkTimeLeft,
			traveledPath,
			myPressure,
		)
	}
}
