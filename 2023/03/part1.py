from typing import List, Tuple, Dict

input = "input.txt"
# input = "test.txt"

# 1: 560670
# 2: 91622824


def print_gid(grid: Dict[int, List[int]]):
    for y in range(0, len(grid)):
        for x in range(0, len(grid[y])):
            print(f"x: {x}, y: {y}, value: {grid[y][x]}")


def is_symbol(char: str) -> bool:
    if char.isdigit():
        return False
    elif char == ".":
        return False
    else:
        return True


def number_crawler(
    grid: Dict[int, List[int]], x: int, y: int
) -> Tuple[List[List[int]], int]:
    # from start move left and right to find the ends of the number.
    # then read the number from left to right. return the number and the coordinates of the number.
    start = ""
    end = ""
    current_x = x
    visited = []
    grid_max_x = len(grid[0]) - 1

    # print(f"starting point: {grid[y][x]}")

    # move left
    while grid[y][current_x].isdigit():
        # print(f"moving left: {grid[y][current_x]}")
        current_x -= 1
        if current_x == -1:
            break

    start = current_x + 1

    # move right
    current_x = x
    while grid[y][current_x].isdigit():
        # print(f"Moving right: {grid[y][current_x]}")
        current_x += 1
        if current_x > grid_max_x:
            break
    end = current_x - 1

    number = ""
    # print(f"start: {start}, end: {end}")
    for x in range(start, end + 1):
        visited.append([x, y])
        number += grid[y][x]

    return visited, int(number)


def neighbors(grid: Dict[int, List[int]], x: int, y: int) -> List[List[int]]:
    # y+1 x-1 x x+1
    # y   x-1 * x+1
    # y-1 x-1 x x+1
    possibles = [
        [x - 1, y + 1],
        [x, y + 1],
        [x + 1, y + 1],
        [x - 1, y],
        [x + 1, y],
        [x - 1, y - 1],
        [x, y - 1],
        [x + 1, y - 1],
    ]
    grid_min = 0
    grid_max_y = len(grid.keys()) - 1
    grid_max_x = len(grid[0]) - 1
    confirmed_neighbors = []
    for neighbor in possibles:
        if neighbor[0] < grid_min or neighbor[0] > grid_max_x:
            continue
        if neighbor[1] < grid_min or neighbor[1] > grid_max_y:
            continue
        confirmed_neighbors.append(neighbor)

    return confirmed_neighbors


def is_symbol(c: str) -> bool:
    if c.isdigit() or c == ".":
        return False
    return True


def check_numbers(grid: Dict[int, List[int]], x: int, y: int) -> List[int]:
    visited = []
    numbers = []
    my_neighbors = neighbors(grid, x, y)
    for n in my_neighbors:
        cell_id = f"{n[0]},{n[1]}"
        if cell_id in visited:
            continue
        cell_content = grid[n[1]][n[0]]
        if cell_content.isdigit():
            checked_cells, number = number_crawler(grid, n[0], n[1])
            numbers.append(number)
            for cell in checked_cells:
                visited.append(f"{cell[0]},{cell[1]}")
    return numbers


def grid_walker(grid: Dict[int, List[int]]) -> Dict[str, List[int]]:
    results = {}
    for y in range(0, len(grid)):
        for x in range(0, len(grid[y])):
            if is_symbol(grid[y][x]):
                numbers = check_numbers(the_grid, x, y)
                if len(numbers) > 0:
                    results[f"{x},{y}"] = numbers

    return results


the_grid = {}
max_x = 0
max_y = 0


with open(input, "r") as file:
    y_index = 0
    for line in file.readlines():
        line = line.strip()
        the_grid[y_index] = list(line)
        y_index += 1
    max_y = y_index - 1
    max_x = len(line) - 1


# print(number_crawler(the_grid, 8, 2))
# print(neighbors(the_grid, 1, 0))
# print(is_symbol(the_grid[1][3]))
# print(is_symbol(the_grid[1][2]))
# print(check_numbers(the_grid, 5, 8))

resulting_numbers = grid_walker(the_grid)
all_numbers = []
all_gears = []
for k, v in resulting_numbers.items():
    xy = k.split(",")
    print(f"{k} '{the_grid[int(xy[1])][int(xy[0])]}': {v}")
    for n in v:
        all_numbers.append(n)

    if the_grid[int(xy[1])][int(xy[0])] == "*" and len(v) == 2:
        all_gears.append(v[0] * v[1])

print(f"sum: {sum(all_numbers)}")
print(f"sum: {sum(all_gears)}")
