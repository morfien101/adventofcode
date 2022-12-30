package main

type Permutation struct {
	orig []int64
	perm []int64
}

func NewPermutation(orig []int64) *Permutation {
	self := Permutation{orig: orig, perm: make([]int64, len(orig))}
	return &self
}

func NewPermutationChan(orig []int64, limit int64, channelLimit int) chan []int64 {
	perm := NewPermutation(orig)
	ch := make(chan []int64, channelLimit)

	go func() {
		defer close(ch)
		var current int64 = 0
		for next := perm.Next(); next != nil; next = perm.Next() {
			ch <- next
			if limit != -1 {
				current++
				if current > limit {
					break
				}
			}
		}
	}()

	return ch
}

func NewPermutationBatchedChan(orig []int64, limit int64, channelLimit int, batching int) chan [][]int64 {
	perm := NewPermutation(orig)
	ch := make(chan [][]int64, channelLimit)

	go func() {
		defer close(ch)

		var current int64 = 0
		batch := [][]int64{}
		inBatch := 0

		for next := perm.Next(); next != nil; next = perm.Next() {
			// Fill batch
			batch = append(batch, next)
			inBatch++
			// Check if we need to ship it
			// reset everything
			if inBatch == batching {
				ch <- batch
				batch = [][]int64{}
				inBatch = 0
			}
			current++
			// Check if we have reached the limit.
			if limit != -1 {
				if current == limit {
					break
				}
			}
		}

		// Send the last of it if we need to.
		if len(batch) > 0 {
			ch <- batch
		}
	}()

	return ch
}

func (self *Permutation) nextPerm() {
	for i := int64(len(self.perm)) - 1; i >= 0; i-- {
		if i == 0 || self.perm[i] < int64(len(self.perm))-i-1 {
			self.perm[i]++
			return
		}
		self.perm[i] = 0
	}
}

func (self *Permutation) Next() []int64 {
	defer self.nextPerm()

	if int64(len(self.perm)) == 0 || self.perm[0] >= int64(len(self.perm)) {
		return nil
	}

	result := append([]int64{}, self.orig...)
	for i, v := range self.perm {
		result[i], result[i+int(v)] = result[i+int(v)], result[i]
	}
	return result
}
