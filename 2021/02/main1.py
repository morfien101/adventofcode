input_file = './input.txt'
output_file = './output1.txt'


def write_output(value):
    global output_file
    with open(output_file, 'w') as output:
        output.write(f'{value}')


horizontal = 0
depth = 0

with open(input_file, 'r') as input:
    for instruction in input:
        components = instruction.split(' ')

        if components[0] == 'forward':
            horizontal += int(components[1])
        if components[0] == 'down':
            depth += int(components[1])
        if components[0] == 'up':
            depth -= int(components[1])

result = horizontal * depth

print(result)
write_output(result)
