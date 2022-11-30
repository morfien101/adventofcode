import os

input = open('./input.txt', 'r')

increases = 0
previous = 0

array = []
windowed_array = []

with open('./input.txt', 'r') as input:
    for line in input:
        array.append(int(line))


for index, _ in enumerate(array):
    if index + 3 > len(array):
        break

    windowed_array.append(
        sum([array[index], array[index + 1], array[index + 2]])
    )

for current in windowed_array:
    if current > previous:
        increases += 1

    previous = current

print(increases-1)

output = open('./output2.txt', 'w')
output.write(f"{increases-1}")
output.close()
