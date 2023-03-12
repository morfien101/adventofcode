from typing import List, Mapping, Dict
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
# input_file = "./test_input.txt"
input_file = "./input.txt"

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


def exposed_edges(
    grid: Mapping[int, Mapping[int, Mapping[int, bool]]], xyz: List[int]
) -> int:
    edges = 0

    # grid contains the occupied space
    for x, y, z in neighbors(xyz):
        if not occupied(grid, x, y, z):
            edges += 1

    return edges


def part1(
    grid: Mapping[int, Mapping[int, Mapping[int, bool]]], coords: List[List[int]]
):
    count = 0
    for xyz in coords:
        count += exposed_edges(grid, xyz)

    write_output(output_file1, f"{count}")


def axis_min_max(
    grid: Mapping[int, Mapping[int, Mapping[int, bool]]]
) -> Dict[str, List[int]]:
    max_x = 1
    min_x = 1
    max_y = 1
    min_y = 1
    max_z = 1
    min_z = 1

    for x in grid.keys():
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x

        for y in grid[x].keys():
            if y < min_y:
                min_y = y
            elif y > max_y:
                max_y = y

            for z in grid[x][y].keys():
                if z < min_z:
                    min_z = z
                elif z > max_z:
                    max_z = z
    return {
        "x": [min_x - 1, max_x + 1],
        "y": [min_y - 1, max_y + 1],
        "z": [min_z - 1, max_z + 1],
    }


# low: 1758
def part2(
    grid: Mapping[int, Mapping[int, Mapping[int, bool]]], coords: List[List[int]]
):
    # Max and min of the grid
    ax_mm = axis_min_max(grid)

    # Negative space represents the outside of the shape
    negative = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: True)))

    negative_spaces = [[0, 0, 0]]
    for space in negative_spaces:
        negative[space[0]][space[1]][space[2]] = False
        for n in neighbors(space):
            # Check that the neighbor is within the grid
            if n[0] < ax_mm["x"][0] or n[0] > ax_mm["x"][1]:
                continue
            elif n[1] < ax_mm["y"][0] or n[1] > ax_mm["y"][1]:
                continue
            elif n[2] < ax_mm["z"][0] or n[2] > ax_mm["z"][1]:
                continue
            # Check that the neighbor is not already in the negative space
            if n in negative_spaces:
                continue
            else:
                # Check if the neighbor is occupied in the shape
                if not occupied(grid, n[0], n[1], n[2]):
                    negative_spaces.append(n)

    count = 0
    for xyz in coords:
        count += exposed_edges(negative, xyz)
    write_output(output_file2, f"{count}")


def main():
    coords = digest_input(input_file)
    grid = generate_grid(coords)

    part1(grid, coords)
    part2(grid, coords)


if __name__ == "__main__":
    main()
