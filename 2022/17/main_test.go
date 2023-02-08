package main

import (
	"strings"
	"sync"
	"testing"
)

func TestDecode(t *testing.T) {
	s, _ := readInput("./test_input.txt")

	so := decodeInput(s)

	t.Log(so)
}

func TestJetCycles(t *testing.T) {
	s, _ := readInput("./test_input.txt")
	so := decodeInput(s)
	c := jetCycles(so)

	cyclesCollected := []string{}
	for i := 0; i < 1000; i++ {
		cyclesCollected = append(cyclesCollected, <-c)
	}
	close(c)

	t.Log("Cycles collected:", len(cyclesCollected))
}

func drawRock(t *testing.T, r *rock) {
	lower := 3
	upper := 3
	for _, v := range r.pos {
		if v.y < lower {
			lower = v.y
		}
		if v.y > upper {
			upper = v.y
		}
	}
	grid := map[int][]string{}
	for y := lower - 3; y <= upper; y++ {
		grid[y] = []string{}
		for x := 0; x < 7; x++ {
			icon := "."
			for _, pos := range r.pos {
				if pos.x == x && pos.y == y {
					icon = "#"
				}
			}
			grid[y] = append(grid[y], icon)
		}
	}

	for line := upper; line >= 0; line-- {
		t.Logf("%01d: %v", line, grid[line])
	}
}

func TestRocks(t *testing.T) {
	currentHeight := 0
	rocksChan := generateRocks()

	for i := 0; i < 5; i++ {
		nextRock := <-rocksChan
		drawRock(t, nextRock(currentHeight))
		currentHeight++
	}
}

func TestMovement(t *testing.T) {
	theRock := newPlusRock(0)

	theRock.moveDown()
	drawRock(t, theRock)
	t.Log(" - - - - - - ")
	theRock.moveLeft()
	drawRock(t, theRock)
	t.Log(" - - - - - - ")
	theRock.moveRight()
	drawRock(t, theRock)
	t.Log(" - - - - - - ")
	theRock.moveUp()
	drawRock(t, theRock)
}

func TestCollision(t *testing.T) {
	theStack := newStack()
	firstRock := newPlusRock(-3)
	theStack.addRock(firstRock)

	secondRock := newVLineRock(theStack.highestPoint() - 2)
	theStack.addRock(secondRock)
	secondRock.moveRight()
	secondRock.moveRight()
	t.Log(theStack.collision(secondRock))
	secondRock.moveDown()
	secondRock.moveLeft()
	t.Log(theStack.collision(secondRock))
	theStack.addRock(secondRock)

	t.Log(theStack)
}

func matchSlice[T bool | int | string](x, y []T) bool {
	if len(x) != len(y) {
		return false
	}

	match := true
	for i := 0; i < len(x); i++ {
		if x[i] != y[i] {
			match = false
			break
		}
	}
	return match
}

func TestDrawStack(t *testing.T) {
	// There appears to be a bug when drawing the stack.
	// Each time you draw it adds 1 extra line.
	// Fix this.
}

func TestTrim(t *testing.T) {
	theStack := newStack()

	for i := 0; i < 10000; i++ {
		theStack.addBlankLine(i, true)
	}

	//t.Log(theStack)

	theStack.trim(5000)
	nKeys := 0
	for range theStack.pile {
		nKeys++
	}

	t.Logf("Number of keys: %d, current height: %d", nKeys, theStack.hight)

}

func TestMatchSlice(t *testing.T) {
	if !matchSlice([]bool{true, true}, []bool{true, true}) {
		t.Fail()
	}
	if matchSlice([]bool{true, false}, []bool{true, true}) {
		t.Fail()
	}
}

func TestSettle(t *testing.T) {
	theStack := newStack()
	rock1 := newPlusRock(-3)

	rock2 := newSquareRock(-1)
	rock2.moveRight()
	rock2.moveRight()
	// rock2.moveDown()
	// rock2.moveDown()

	rock3 := newVLineRock(0)

	rock4 := newVLineRock(-3)
	rock4.moveLeft()
	rock4.moveLeft()

	theStack.addRock(rock1)

	rockSettlements := []bool{
		theStack.settle(rock1),
		theStack.settle(rock2),
		theStack.settle(rock3),
		theStack.settle(rock4),
	}
	expectedRockSettlement := []bool{true, true, false, true}

	fail := false
	if !matchSlice(expectedRockSettlement, rockSettlements) {
		t.Logf("Rocks did not settle correctly. Expected: %v, Got: %v", expectedRockSettlement, rockSettlements)
		fail = true
	}

	theStack.addRock(rock2)
	theStack.addRock(rock3)
	theStack.addRock(rock4)
	t.Log(theStack)

	if fail {
		t.Fail()
	}
}

func TestHitWall(t *testing.T) {
	theStack := newStack()
	rock1 := newVLineRock(-3)
	rock2 := newVLineRock(-3)
	for i := 0; i < 10; i++ {
		rock1.moveLeft()
		rock2.moveRight()
	}

	t.Log("x", rock1.pos[1].x, "y", rock1.pos[1].y)
	t.Log("x", rock2.pos[1].x, "y", rock2.pos[1].y)
	theStack.addRock(rock1)
	theStack.addRock(rock2)
	t.Log(theStack)
}

func TestHitWall2(t *testing.T) {
	theStack := newStack()
	rock1 := newHLineRock(-3)
	rock2 := newPlusRock(-1)
	rock3 := newVLineRock(2)
	rock4 := newLRock(7)
	rock5 := newSquareRock(10)
	for i := 0; i < 10; i++ {
		rock1.moveLeft()
		rock2.moveRight()
		rock3.moveLeft()
		rock4.moveRight()
		rock5.moveLeft()
	}

	theStack.addRock(rock1)
	theStack.addRock(rock2)
	theStack.addRock(rock3)
	theStack.addRock(rock4)
	theStack.addRock(rock5)
	t.Log(theStack)

	theStack2 := newStack()
	rock1Stage2 := newHLineRock(-3)
	rock2Stage2 := newPlusRock(-1)
	rock3Stage2 := newVLineRock(2)
	rock4Stage2 := newLRock(7)
	rock5Stage2 := newSquareRock(10)
	for i := 0; i < 10; i++ {
		rock1Stage2.moveRight()
		rock2Stage2.moveLeft()
		rock3Stage2.moveRight()
		rock4Stage2.moveLeft()
		rock5Stage2.moveRight()
	}

	theStack2.addRock(rock1Stage2)
	theStack2.addRock(rock2Stage2)
	theStack2.addRock(rock3Stage2)
	theStack2.addRock(rock4Stage2)
	theStack2.addRock(rock5Stage2)
	t.Log(theStack2)
}

func TestFirstTwo(t *testing.T) {
	theStack := newStack()
	rock1 := newHLineRock(0)
	rock2 := newPlusRock(1)

	rock1.moveRight()
	rock1.moveDown()
	rock1.moveRight()
	rock1.moveDown()
	rock1.moveRight()
	rock1.moveDown()
	rock1.moveLeft()
	theStack.addRock(rock1)

	theStack.addRock(rock2)

	t.Log(theStack)
}

func TestDraw(t *testing.T) {
	theStack := newStack()
	rock1 := newHLineRock(4)
	theStack.addRock(rock1)
	t.Log(theStack.draw(true))
	t.Log(theStack.pile)
	t.Log(theStack.hight)
}

func TestFindPattern(t *testing.T) {
	nRocks := 1000000

	input, err := readInput("./input.txt")
	if err != nil {
		t.Log(err)
		t.FailNow()
	}
	jetsRaw := decodeInput(input)

	jets := jetCycles(jetsRaw)

	currentHight := 0
	theStack := newStack()
	rocks := generateRocks()

	for i := 1; i <= nRocks; i++ {
		nextRock := <-rocks
		currentRock := nextRock(currentHight)
		if i%100000 == 0 {
			t.Log("Dropping rock:", i)
		}
		moveLRRock := func(direction string) {
			if direction == left {
				currentRock.moveLeft()
				if theStack.collision(currentRock) {
					currentRock.moveRight()
				}
			} else if direction == right {
				currentRock.moveRight()
				if theStack.collision(currentRock) {
					currentRock.moveLeft()
				}
			}
		}

		for {
			moveLRRock(<-jets)

			currentRock.moveDown()
			if theStack.collision(currentRock) {
				currentRock.moveUp()
				theStack.addRock(currentRock)
				currentHight = theStack.highestPoint()
				break
			}
		}
	}

	t.Log("Done, going to drawing")
	theStackImage := theStack.draw(false)
	t.Log("Done, drawing")

	tester := func(limit int, found chan bool) {
		window1Limit := limit
		window2Limit := limit * 2

		window1 := []string{}
		window2 := []string{}

		for j := 1; j <= window1Limit; j++ {
			window1 = append(window1, theStackImage[j])
		}
		for k := window1Limit + 1; k <= window2Limit; k++ {
			window2 = append(window1, theStackImage[k])
		}

		if strings.Join(window1, "") == strings.Join(window2, "") {
			t.Logf("Found pattern at window limits 1: %d, 2: %d", window1Limit, window2Limit)
			found <- true
		}
	}

	workerWG := &sync.WaitGroup{}
	limitsChan := make(chan int)
	foundChan := make(chan bool, 8)

	for worker := 0; worker < 8; worker++ {
		workerWG.Add(1)
		go func() {
			for limit := range limitsChan {
				tester(limit, foundChan)
			}
			workerWG.Done()
		}()
	}

	for i := 100000; i < (len(theStackImage)-2)/2; i++ {
		if i%1000 == 0 {
			t.Log("Testing limit", i)
		}
		exit := false
		select {
		case limitsChan <- i:
		case <-foundChan:
			close(limitsChan)
			workerWG.Wait()
			close(foundChan)
			exit = true
		}
		if exit {
			break
		}
		limitsChan <- i
	}
}
