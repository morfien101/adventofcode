from typing import List
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


def convert_input(file: str):
    with open(file, "r") as input:
        return list(input.readline().strip())


def find_start(input: List[str], size: int) -> int:
    offset = size
    while offset < len(input):
        current_window = input[offset - size : offset]
        if len(set(current_window)) == size:
            return offset
        offset += 1


def main():
    input = convert_input(input_file)
    start_of_packet = find_start(input, 4)
    start_of_message = find_start(input, 14)
    write_output(output_file1, start_of_packet)
    write_output(output_file2, start_of_message)


if __name__ == "__main__":
    main()
