input_file = "./input.txt"
output_file = "./output2.txt"


def write_output(value):
    global output_file
    print(f"{value}")
    with open(output_file, "w") as output:
        output.write(f"{value}")


highest_calories = 0
current_calories = 0
elves = []

with open(input_file, "r") as input:
    for line in input:
        if line == "\n":
            elves.append(current_calories)
            current_calories = 0
            continue

        current_calories += int(line.strip())

elves.sort()
write_output(sum(elves[-3:]))
