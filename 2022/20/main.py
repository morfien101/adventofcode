from typing import Union, List, Mapping, Dict
import base64


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


output_file1 = "./output1.txt"
output_file2 = "./output2.txt"
input_file = "./test_input.txt"
# input_file = "./input.txt"


class mixer:
    def __init__(self, numbers: List[int]):
        self.numbers = numbers
        self.idx = 0
        self.length = len(numbers)

    def seek(self, id: int):
        self.idx = self.numbers.index(id)

    def mix(self, id: int, n: int):
        # if n is equal to zero, do nothing
        if n == 0:
            return

        new_index = self._step(id, n)
        # rebuild the list using self.index as the new index and current_index as the value to insert
        self._move_current_to(new_index)

    def _step(self, id: int, n: int):
        # step will always be a number more or less than 0.
        # step forward = (i + v) % len
        # step backwards = (-1(((len - (i + v)) % len) + len) % len

        # set the current index to the index of the id
        self.seek(id)

        if n > 0:
            new_index = (self.idx + n) % self.length
        else:
            new_index = (
                -1 * ((self.length - (self.idx + n)) % self.length) + self.length
            ) % self.length
        return new_index

    def _index_value(self, index: int):
        return self.numbers[index]

    def _move_current_to(self, new_index: int):
        current_value = self.numbers.pop(self.idx)
        print(f"moving {current_value} to {new_index}")
        if new_index == 0:
            self.numbers = [current_value] + self.numbers
        elif new_index == self.length - 1:
            self.numbers = self.numbers + [current_value]
        else:
            new_index -= 1
            self.numbers = (
                self.numbers[:new_index] + [current_value] + self.numbers[new_index:]
            )

    def current_state(self):
        return self.numbers

    def decrypt(self, start: id, steps: List[int]):
        cords = []

        for step in steps:
            collect_from = self._step(start, step)
            cords.append(self._index_value(collect_from))

        return cords


def part1(numbers: List[int]):
    # make a new list containing the index ids of numbers

    idx_list = list(range(len(numbers)))

    # make a mixer
    c = mixer(list(range(len(numbers))))

    print([numbers[x] for x in c.current_state()])
    for id in idx_list:
        print(f"mixing {numbers[id]} as id {id}")
        c.mix(id, numbers[id])
        print([numbers[x] for x in c.current_state()])
        print("---")

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
