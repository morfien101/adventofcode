import base64


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


input_file = "./input.txt"
# input_file = "./test_input.txt"
output_file = "./output1.txt"


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


def overlapping(area1, area2):
    # Assume that the partner is fully covered.
    area2_range = [x for x in range(area2[0], area2[1] + 1)]
    for i in range(area1[0], area1[1] + 1):
        if i not in area2_range:
            return False
    return True


useless_elves = 0
for elf_pair in elf_pairs(input_file):
    # print(f"elf_pair: {elf_pair}")
    for check in [elf_pair, [x for x in elf_pair.__reversed__()]]:
        if overlapping(check[0], check[1]):
            useless_elves += 1
            break

write_output(output_file, useless_elves)
