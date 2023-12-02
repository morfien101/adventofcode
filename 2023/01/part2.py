import re

# input="my_test.txt"
# input = "test2.txt"
input = "input.txt"

inputs = []

captures = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

forward_lookups = [s for s in list(captures.keys())]
reversed_lookups = [s[::-1] for s in forward_lookups]

with open(input, 'r') as file:
    for line in file.readlines():
        line = line.strip()
        r_line = line[::-1]

        first = ""
        last = ""
        found_first = False
        found_last = False

        for i in range(len(line)):
            try:
                first = int(line[i])
                found_first = True
            except:
                for lookup in forward_lookups:
                    if lookup in line[:i+1]:
                        first = captures[lookup]
                        found_first = True
                        break
            
            if found_first:
                break

        for i in range(len(r_line)):
            try:
                last = int(r_line[i])
                found_last = True
            except:
                for lookup in reversed_lookups:
                    if lookup in r_line[:i+1]:
                        last = captures[lookup[::-1]]
                        found_last = True
                        break

            if found_last:
                break
            
        inputs.append(int(f"{first}{last}"))

print(sum(inputs))