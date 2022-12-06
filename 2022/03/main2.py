import base64


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


input_file = "./input.txt"
# input_file = "./test_input.txt"
output_file = "./output2.txt"


priority_map = {}
# Upper case letters
for i in range(1, 27):
    priority_map[chr(64 + i)] = i + 26
# Lower case letters
for i in range(1, 27):
    priority_map[chr(96 + i)] = i


def every_3(input: list) -> list:
    output = [[]]
    output_index = 0
    for index, item in enumerate(input):
        output[output_index].append(item)
        if (index + 1) % 3 == 0:
            output_index += 1
            output.append([])

    return [group for group in output if len(group) == 3]


def determine_badge(bags: list) -> str:
    for item in bags[0]:
        if item in bags[1] and item in bags[2]:
            return item


with open(input_file, "r") as input:
    bags = [list(line.strip()) for line in input]

groups = every_3(bags)

badges = [priority_map[determine_badge(group)] for group in groups]

write_output(output_file, sum(badges))
