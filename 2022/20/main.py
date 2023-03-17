from typing import Union, List, Mapping, Dict
import base64
from itertools import cycle


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


output_file1 = "./output1.txt"
output_file2 = "./output2.txt"
input_file = "./test_input.txt"
# input_file = "./input.txt"


class cycler:
    def __init__(self, numbers: List[int]):
        self.numbers = numbers
        self.idx = 0
        self.length = len(numbers)

    def seek(self, id: int):
        self.idx = self.numbers.index(id)

    def step(self, id: int, n: int):
        # if n is equal to zero, do nothing
        if n == 0:
            return

        # find the index of the id
        self.seek(id)
        # save the found index as we will need it after finding where to move to
        current_idx = self.current_idx()

        # determine how many steps to take
        # If the steps are in the negative direction, we need to account for zero
        # So we subtract one from the steps therefore adding an extra step
        steps = (self.idx + n) % self.length
        if n < 0:
            steps -= 1

        self.idx = steps

        # rebuild the list using self.index as the new index and current_index as the value to insert
        self._rebuild(current_idx)

    def current_idx(self):
        return self.idx

    def current_state(self):
        return self.numbers

    def _rebuild(self, current_index: int):
        current = self.numbers.pop(current_index)
        self.numbers = self.numbers[: self.idx] + [current] + self.numbers[self.idx :]

    def decrypt(self, start: id, steps: List[int]):
        cords = []

        for step in steps:
            self.step(start, step)
            cords.append(self.current_idx())

        print(f"found cords {cords}")

        return cords


def part1(numbers: List[int]):
    # make a new list containing the index ids of numbers

    idx_list = list(range(len(numbers)))

    # make a cycler
    c = cycler(idx_list.copy())

    for id in idx_list:
        c.step(id, numbers[id])

    print([numbers[x] for x in c.current_state()])

    decryption_ids_result = c.decrypt(numbers.index(0), [1000, 2000, 3000])

    decryption_result = [numbers[x] for x in decryption_ids_result]
    print(decryption_result)
    print(sum(decryption_result))

    # determine movement
    # move index through list
    # pop value at index
    # create a new list with values on left and right of the new index.


def main():
    with open(input_file, "r") as f:
        input = f.read().splitlines()
        numbers = [int(x) for x in input]

    part1(numbers.copy())


if __name__ == "__main__":
    main()
