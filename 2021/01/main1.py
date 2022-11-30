import os

input = open('./input.txt', 'r')

increases = 0
previous = 0

with open('./input.txt', 'r') as input:
    for line in input:
        current = int(line)
        if current > previous:
            increases += 1

        previous = current

print(increases-1)

output = open('./output.txt', 'w')
output.write(f"{increases-1}")
output.close()
