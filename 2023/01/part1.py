# input = "test.txt"
input = "input.txt"

inputs = []

with open(input, 'r') as file:
    for line in file.readlines():
        line = line.strip()
        first = ""
        last = ""
        for c in range(0, len(line)):
            try:
                first = int(line[c])
                break
            except:
                continue
        for c in range(len(line)-1, -1,-1):
            try:
                last = int(line[c])
                break
            except:
                continue
        
        print(first, last)
        inputs.append(int(f"{first}{last}"))

print(sum(inputs))