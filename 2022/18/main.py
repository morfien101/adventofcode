from typing import List, Mapping, Union
import base64
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


output_file1 = "./output1.txt"
output_file2 = "./output2.txt"
input_file = "./test_input.txt"
# input_file = "./input.txt"

verbose = False


def digest_input(filename: str) -> List[List[int]]:
    lines = []
    with open(input_file, "r") as input:
        for line in input:
            line = line.strip()
            lines.append([int(i) for i in line.split(",")])
    return lines


def generate_grid(
    coords: List[List[int]],
) -> Mapping[int, Mapping[int, Mapping[int, bool]]]:
    grid = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: False)))
    for c in coords:
        grid[c[0]][c[1]][c[2]] = True

    return grid


def neighbors(coords: List[int]) -> List[tuple[int]]:
    # xyz difference
    return [
        (coords[0], coords[1], coords[2] - 1),  # front [0,0,-1]
        (coords[0], coords[1], coords[2] + 1),  # back  [0,0,1]
        (coords[0] - 1, coords[1], coords[2]),  # left  [-1,0,0]
        (coords[0] + 1, coords[1], coords[2]),  # right [1,0,0]
        (coords[0], coords[1] - 1, coords[2]),  # under [0,-1,0]
        (coords[0], coords[1] + 1, coords[2]),  # above [0,1,0]
    ]


def occupied(
    grid: Mapping[int, Mapping[int, Mapping[int, bool]]], x: int, y: int, z: int
) -> bool:
    """Returns true if the point is occupied in the shape"""
    return grid[x][y][z]


def exposedEdges(
    grid: Mapping[int, Mapping[int, Mapping[int, bool]]], xyz: List[int]
) -> int:
    exposedEdges = 0

    # grid contains the occupied space
    for x, y, z in neighbors(xyz):
        if not occupied(grid, x, y, z):
            exposedEdges += 1

    return exposedEdges


def part1(
    grid: Mapping[int, Mapping[int, Mapping[int, bool]]], coords: List[List[int]]
):
    count = 0
    for xyz in coords:
        count += exposedEdges(grid, xyz)

    write_output(output_file1, f"{count}")


# low: 1758
def part2(
    grid: Mapping[int, Mapping[int, Mapping[int, bool]]], coords: List[List[int]]
):

    combined_outside = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: False))
    )

    ax = plt.axes(projection="3d")
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))

    new_coords = []

    for x in grid.keys():
        for y in grid[x].keys():
            min_z = min(grid[x][y].keys())
            max_z = max(grid[x][y].keys())
            for z in [z for z in range(min_z, max_z + 1)]:
                combined_outside[x][y][z] = True
                ax.scatter(x, y, z, c="blue", linewidth=10)
                new_coords.append([x, y, z])

    for x in grid.keys():
        for y in grid[x].keys():
            for z in grid[x][y].keys():
                ax.scatter(x, y, z, c="red", linewidth=5)

    # count = 0
    # for c in new_coords:
    #     edges = exposedEdges(combined_outside, c)
    #     count += edges

    # write_output(output_file2, f"{count}")
    plt.show()


def main():
    coords = digest_input(input_file)
    grid = generate_grid(coords)

    # part1(grid, coords)
    part2(grid, coords)


if __name__ == "__main__":
    main()
