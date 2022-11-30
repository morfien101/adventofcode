input_file = './input.txt'
output_file = './output1.txt'


def write_output(value):
    global output_file
    with open(output_file, 'w') as output:
        output.write(f'{value}')


grid = []

with open(input_file, 'r') as input:
    for line in input:
        grid.append([int(s) for s in list(line.strip())])

grid_half = len(grid)/2
grid_column_counts = []

for index in range(0, len(grid[0])):
    grid_column_counts.append(0)

for line in grid:
    for index, value in enumerate(line):
        grid_column_counts[index] += value

gamma = []
epsilon = []

for value in grid_column_counts:
    if value > grid_half:
        gamma.append('1')
        epsilon.append('0')
    else:
        gamma.append('0')
        epsilon.append('1')

gamma_int = int(''.join(gamma), 2)
epsilon_int = int(''.join(epsilon), 2)

result = gamma_int * epsilon_int
print(result)
write_output(result)
