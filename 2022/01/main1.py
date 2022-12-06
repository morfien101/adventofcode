import base64

input_file = "./input.txt"
output_file = "./output1.txt"


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


highest_calories = 0
current_calories = 0
elves = []

with open(input_file, "r") as input:
    for line in input:
        if line == "\n":
            if current_calories > highest_calories:
                highest_calories = current_calories

            current_calories = 0
            continue

        current_calories += int(line.strip())

write_output(output_file, highest_calories)
