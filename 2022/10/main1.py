from typing import List, Union, Callable
import base64


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


input_file = "./input.txt"
# input_file = "./test_input.txt"
output_file1 = "./output1.txt"
output_file2 = "./output2.txt"


class CPU:
    def __init__(self):
        self._X: int = 1
        self._current_clock_number: int = 0
        self._readings: List[List[Union[int, Callable[[int], None]]]] = []
        self._crt = [["." for _ in range(0, 40)] for _ in range(0, 6)]
        self._crt_index = 0
        self._crt_row = 0

    def process_instructions(self, input: List[str]):
        for i in input:
            i = i.split(" ")
            if i[0] == "noop":
                self._noop()
            elif i[0] == "addx":
                self._addX(int(i[1]))

    def readings(self, at: int, f: Callable[[int], None]):
        self._readings.append([at, f])

    def _addX(self, value: int):
        self._current_clock_number += 2
        if len(self._readings) > 0:
            self._take_reading()
        self._draw()
        self._draw()
        self._X += value

    def _noop(self):
        self._current_clock_number += 1
        if len(self._readings) > 0:
            self._take_reading()
        self._draw()

    def _take_reading(self):
        if self._current_clock_number >= self._readings[0][0]:
            self._readings[0][1](self._X * self._readings[0][0])
            self._readings.pop(0)

    def _draw(self):
        if self._crt_index in [self._X - 1, self._X, self._X + 1]:
            self._crt[self._crt_row][self._crt_index] = "#"
        else:
            self._crt[self._crt_row][self._crt_index] = "."

        # screen rows runs from 0 - 5
        # screen col runs from 0 - 39
        if self._crt_index == 39:
            self._crt_index = 0
            if self._crt_row == 5:
                self._crt_row = 0
            else:
                self._crt_row += 1
        else:
            self._crt_index += 1

    def render(self) -> str:
        output = ""
        for row in self._crt:
            line = "".join(row)
            line += "\n"
            output += line
        return output


def main():
    instructions = []
    with open(input_file, "r") as input:
        for line in input:
            line = line.strip()
            instructions.append(line)

    readings = []

    def take_reading(value: int):
        readings.append(value)

    cpu = CPU()
    for i in [20, 60, 100, 140, 180, 220]:
        cpu.readings(at=i, f=take_reading)

    cpu.process_instructions(instructions)
    write_output(output_file1, sum(readings))
    write_output(output_file2, cpu.render())


if __name__ == "__main__":
    main()
