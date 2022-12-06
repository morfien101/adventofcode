from typing import Dict, List
import re
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


def split_input(input_file):
    lines = [[], []]
    index = 0
    with open(input_file, "r") as input:
        for line in input:
            line = line.rstrip()
            if line == "":
                index += 1
                continue
            lines[index].append(line)
    return lines[0], lines[1]


def convert_stack(stack_lines: List[str]) -> Dict[int, str]:
    stacks_indexes: List[str] = []
    stacks: Dict[int, List[str]] = {}

    # Work out the indexes that have the values that we need.
    # This will be the where the containers are.
    # The container stack ID is on the first line when reversed.
    for stack_index, value in enumerate(list(reversed(stack_lines))[0]):
        if value != " ":
            stacks_indexes.append(stack_index)
            stacks[int(value)] = []

    # Then get the container values from the indexes.
    # However lines may end before the last index when you start
    # getting to the peaks.
    # Remember to remove the container stack ids
    for line in reversed(stack_lines[0 : len(stack_lines) - 1]):
        line = list(line)
        for idx, loc in enumerate(stacks_indexes):
            try:
                if line[loc] == " ":
                    continue
                stacks[idx + 1].append(line[loc])
            except IndexError:
                continue

    # Bring the stacks back to the correct order
    for key in stacks:
        stacks[key].reverse()

    return stacks


def convert_instructions(lines: List[str]) -> List[Dict[str, int]]:
    instructions: List[Dict[str, int]] = []
    instructions_regex = r"move (\d+) from (\d+) to (\d+)"
    for line in lines:
        capture = re.search(instructions_regex, line)
        values = capture.groups()
        instructions.append(
            {"move": int(values[0]), "from": int(values[1]), "to": int(values[2])}
        )
    return instructions


def shuffle_stack(
    instructions: List[Dict[str, int]], stack: Dict[int, str], multi_pickup: bool
) -> Dict[int, str]:
    for i in instructions:
        crane_holding: List[str] = []
        for _ in range(0, i["move"]):
            crane_holding.append(stack[i["from"]].pop(0))

        if multi_pickup:
            crane_holding.reverse()

        for item in crane_holding:
            stack[i["to"]] = [item] + stack[i["to"]]

    return stack


def print_stack(stack: Dict[int, str]):
    for key in stack:
        print(f"{key}:{stack[key]}")


def whats_on_top(stack: Dict[int, str]) -> str:
    output = ""
    for key in stack:
        try:
            output += stack[key][0]
        except IndexError:
            continue

    return output


def main():
    cargo_stack, instructions_raw = split_input(input_file)

    instructions = convert_instructions(instructions_raw)

    # Part 1
    # Single crate crane
    print(" Part 1 ".center(50, "#"))
    stack = convert_stack(cargo_stack)

    print_stack(stack)
    print(" Original stack ".center(50, "#"))

    stack = shuffle_stack(instructions, stack, False)

    print_stack(stack)
    print(" Single crate movement stack ".center(50, "#"))
    write_output(output_file1, whats_on_top(stack))
    print("")

    # Part2
    # multi stack crane
    print(" Part 2 ".center(50, "#"))

    stack = convert_stack(cargo_stack)
    print_stack(stack)
    print(" Original stack ".center(50, "#"))
    stack = shuffle_stack(instructions, stack, True)

    print_stack(stack)
    print(" Single crate movement stack ".center(50, "#"))
    write_output(output_file2, whats_on_top(stack))


if __name__ == "__main__":
    main()
