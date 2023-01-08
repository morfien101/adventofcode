package main

import (
	"encoding/base64"
	"flag"
	"fmt"
	"os"
	"sort"
)

// Falling hole is 7 units wide
// Rocks start 2 units from left edge (x: 2).
// 0, 1, x
// Falls from 3 units above the highest rock in the room.
// push, fall, push, fall
// If any movement would cause any part of the rock to move into the walls, floor, or a stopped rock, the movement instead does not occur.
//
//	A rock can not be pushed THROUGH anything else when being pushed by a jet.
//
// A rock will be pushed once more before stopping.
var (
	flagFile    = flag.String("f", "./input.txt", "Data file to read.")
	flagHelp    = flag.Bool("h", false, "Help menu.")
	flagVerbose = flag.Bool("V", false, "Verbose debug printing.")
)

const (
	left  = "l"
	right = "r"
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

func decodeInput(input string) []string {
	out := []string{}
	for _, i := range []byte(input) {
		if i == '<' {
			out = append(out, left)
		} else {
			out = append(out, right)
		}
	}

	return out
}

func jetCycles(cycle []string) chan string {
	out := make(chan string)
	go func() {
		defer func() {
			recover()
		}()

		for {
			for _, d := range cycle {
				out <- d
			}
		}
	}()

	return out
}

type position struct {
	x int
	y int
}

func newPosition(x, y int) *position {
	return &position{
		x: x,
		y: y,
	}
}

type rock struct {
	pos []*position
}

func (r *rock) addPart(x, y int) {
	r.pos = append(r.pos, newPosition(x, y))
}

func (r *rock) move(xDirection int, yDirection int) {
	// Make sure the rocks never pass beyond the walls.
	// Testing if they hit other rocks or the floor needs
	// to be done elsewhere.
	for _, p := range r.pos {
		currentXCheck := p.x + xDirection
		if currentXCheck < 0 || currentXCheck > 6 {
			return
		}
	}

	for _, p := range r.pos {
		newX := p.x + xDirection
		if newX >= 0 && newX < 7 {
			p.x = newX
		}
		p.y = p.y + yDirection
	}
}

func (r *rock) moveLeft() {
	r.move(-1, 0)
}

func (r *rock) moveRight() {
	r.move(1, 0)
}

func (r *rock) moveDown() {
	r.move(0, -1)
}

func (r *rock) moveUp() {
	r.move(0, 1)
}

func newRock() *rock {
	return &rock{
		pos: []*position{},
	}
}

func newHLineRock(yLower int) *rock {
	xStart := 2
	yStart := yLower + 4
	theRock := newRock()
	for i := 0; i < 4; i++ {
		theRock.addPart(xStart+i, yStart)
	}
	return theRock
}

func newVLineRock(yLower int) *rock {
	xStart := 2
	yStart := yLower + 4
	theRock := newRock()
	for i := 0; i < 4; i++ {
		theRock.addPart(xStart, yStart+i)
	}
	return theRock
}

func newLRock(yLower int) *rock {
	xStart := 2
	yStart := yLower + 4
	theRock := newRock()
	for i := 0; i < 3; i++ {
		theRock.addPart(xStart+i, yStart)
	}
	for i := 0; i < 2; i++ {
		theRock.addPart(xStart+2, yStart+1+i)
	}
	return theRock
}

func newPlusRock(yLower int) *rock {
	xStart := 2
	yStart := yLower + 4
	theRock := newRock()
	for i := 0; i < 3; i++ {
		theRock.addPart(xStart+i, yStart+1)
	}
	theRock.addPart(xStart+1, yStart)
	theRock.addPart(xStart+1, yStart+2)
	return theRock
}

func newSquareRock(yLower int) *rock {
	xStart := 2
	yStart := yLower + 4
	theRock := newRock()
	for y := 0; y < 2; y++ {
		for x := 0; x < 2; x++ {
			theRock.addPart(xStart+x, yStart+y)
		}
	}
	return theRock
}

func generateRocks() chan func(int) *rock {
	c := make(chan func(int) *rock)
	rocksOrder := []func(int) *rock{
		newHLineRock,
		newPlusRock,
		newLRock,
		newVLineRock,
		newSquareRock,
	}

	go func(c chan func(int) *rock) {
		for {
			for _, rock := range rocksOrder {
				c <- rock
			}
		}
	}(c)

	return c
}

type stack struct {
	pile   map[int][]string
	keys   []int
	empty  string
	filled string
}

func newStack() *stack {
	return &stack{pile: map[int][]string{}, keys: []int{}, empty: ".", filled: "x"}
}

func (s *stack) updateKeys() {
	keys := []int{}
	for k := range s.pile {
		keys = append(keys, k)
	}
	sort.Ints(keys)
	s.keys = keys
}

func (s *stack) highestPoint() int {
	return s.keys[len(s.keys)-1]
}

func (s *stack) String() string {
	if len(s.keys) == 0 {
		return fmt.Sprintln("001: [. . . . . . .]")
	}
	maxLines := s.keys[len(s.keys)-1]
	output := "\n"

	for i := maxLines; i >= 1; i-- {
		if len(s.pile[i]) == 0 {
			s.addBlankLine(i)
		}
		output += fmt.Sprintf("%03d: %v\n", i, s.pile[i])
	}

	return output
}

func (s *stack) addBlankLine(y int) {
	line := make([]string, 7)
	for i := 0; i < 7; i++ {
		line[i] = s.empty
	}
	s.pile[y] = line
	s.updateKeys()
}

func (s *stack) addRock(r *rock) {
	for _, p := range r.pos {
		if len(s.pile[p.y]) == 0 {
			s.addBlankLine(p.y)
		}
		s.pile[p.y][p.x] = s.filled
	}
	s.updateKeys()
}

// collision tests to see if there is a left or right movement
// collision. The rock must already be in the position that you
// want to test with. A bool is returned to state if there is a
// collision.
func (s *stack) collision(r *rock) bool {
	for _, p := range r.pos {
		// We have gone through the floor
		if p.y == 0 {
			return true
		}
		// If there is no line, there can't be a collision.
		if len(s.pile[p.y]) == 0 {
			continue
		}
		if s.pile[p.y][p.x] == s.filled {
			return true
		}
	}
	return false
}

// settle tests to see if the rock would settle where it is.
// The rock should be tested for settling before moving down.
func (s *stack) settle(r *rock) bool {
	for _, p := range r.pos {
		// We are at the floor
		if p.y-1 == 0 {
			return true
		}
		// If there is no line under it then it can't settle.
		if len(s.pile[p.y-1]) == 0 {
			return false
		}
		if s.pile[p.y-1][p.x] == s.filled {
			return true
		}
	}
	// We should never be able to get here.
	return false
}

func part1(jetsRaw []string, nRocks int) {
	jets := jetCycles(jetsRaw)

	currentHight := 0
	theStack := newStack()
	rocks := generateRocks()

	for i := 1; i <= nRocks; i++ {
		//fmt.Println("Dropping rock:", i)
		nextRock := <-rocks
		currentRock := nextRock(currentHight)

		moveLRRock := func(direction string) {
			if direction == left {
				currentRock.moveLeft()
				//fmt.Println("Move left")
				if theStack.collision(currentRock) {
					//fmt.Println("Collision: Move right")
					currentRock.moveRight()
				}
			} else if direction == right {
				currentRock.moveRight()
				//fmt.Println("Move right")
				if theStack.collision(currentRock) {
					//fmt.Println("Collision: Move left")
					currentRock.moveLeft()
				}
			}
		}

		for {
			moveLRRock(<-jets)

			currentRock.moveDown()
			//fmt.Println("Move down")
			if theStack.collision(currentRock) {
				//fmt.Println("Moved down into something")
				currentRock.moveUp()
				//fmt.Println("Move up")
				theStack.addRock(currentRock)
				//fmt.Println("Set hight to:", theStack.highestPoint())
				currentHight = theStack.highestPoint()
				break
			}
		}
	}
	//fmt.Println(theStack)

	writeOutput("./output1.txt", theStack.highestPoint())
}

func part2(jetsRaw []string, nRocks int) {
	jets := jetCycles(jetsRaw)

	currentHight := 0
	theStack := newStack()
	rocks := generateRocks()

	for i := 1; i <= nRocks; i++ {
		if i%100000 == 0 {
			fmt.Println("Dropping rock", i)
		}
		//fmt.Println("Dropping rock:", i)
		nextRock := <-rocks
		currentRock := nextRock(currentHight)

		moveLRRock := func(direction string) {
			if direction == left {
				currentRock.moveLeft()
				//fmt.Println("Move left")
				if theStack.collision(currentRock) {
					//fmt.Println("Collision: Move right")
					currentRock.moveRight()
				}
			} else if direction == right {
				currentRock.moveRight()
				//fmt.Println("Move right")
				if theStack.collision(currentRock) {
					//fmt.Println("Collision: Move left")
					currentRock.moveLeft()
				}
			}
		}

		for {
			moveLRRock(<-jets)

			currentRock.moveDown()
			//fmt.Println("Move down")
			if theStack.collision(currentRock) {
				//fmt.Println("Moved down into something")
				currentRock.moveUp()
				//fmt.Println("Move up")
				theStack.addRock(currentRock)
				//fmt.Println("Set hight to:", theStack.highestPoint())
				currentHight = theStack.highestPoint()
				break
			}
		}
	}
	//fmt.Println(theStack)

	writeOutput("./output1.txt", theStack.highestPoint())
}

func main() {
	flag.Parse()

	input, err := readInput(*flagFile)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	jetsRaw := decodeInput(input)

	// Drop 2022 rocks
	part1(jetsRaw, 2022)
	part2(jetsRaw, 1000000000000)
}
