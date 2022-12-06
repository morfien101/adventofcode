import base64


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


input_file = "./input.txt"
# input_file = "./test_input.txt"
output_file = "./output1.txt"


priority_map = {}
# Upper case letters
for i in range(1, 27):
    priority_map[chr(64 + i)] = i + 26
# Lower case letters
for i in range(1, 27):
    priority_map[chr(96 + i)] = i


with open(input_file, "r") as input:
    packs = []
    for pack in input:
        pack = list(pack.strip())
        cut = int(len(pack) / 2)
        pocket1 = pack[:cut]
        pocket2 = pack[cut:]
        packs.append([pocket1, pocket2])


items = []
for pack in packs:
    for item in pack[0]:
        if item in pack[1]:
            items.append(priority_map[item])
            break

write_output(output_file, sum(items))
