import base64


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


input_file = "./input.txt"
# input_file = "./test_input.txt"
output_file = "./output2.txt"


def elf_pairs(input_file):
    elf_pairs = []
    with open(input_file, "r") as input:
        for line in input:
            elves_pair = line.strip().split(",")
            x = []
            for elf in elves_pair:
                area = elf.split("-")
                x.append([int(area[0]), int(area[1])])

            elf_pairs.append(x)
    return elf_pairs


def expand(area: str) -> list:
    return [x for x in range(area[0], area[1] + 1)]


def overlapping(area1, area2):
    area2_range = expand(area2)
    for i in expand(area1):
        if i in area2_range:
            return True
    return False


useless_elves = 0
for elf_pair in elf_pairs(input_file):
    if overlapping(elf_pair[0], elf_pair[1]):
        useless_elves += 1

write_output(output_file, useless_elves)
