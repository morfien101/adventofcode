input_file = "./input.txt"
output_file = "./output2.txt"


def write_output(value):
    global output_file
    with open(output_file, "w") as output:
        output.write(f"{value}")


aim = 0
horizontal = 0
depth = 0

with open(input_file, "r") as input:
    for line in input:
        command = line.strip().split(" ")
        instruction = command[0]
        unit = int(command[1])

        if instruction == "forward":
            horizontal += unit
            depth += aim * unit
        if instruction == "down":
            aim += unit
        if instruction == "up":
            aim -= unit

result = horizontal * depth
print(result)

write_output(result)
