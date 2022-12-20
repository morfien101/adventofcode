from __future__ import annotations
from typing import List, Union
import base64
from numpy.lib.stride_tricks import sliding_window_view
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


output_file1 = "./output1.txt"
output_file2 = "./output2.txt"
verbose = False


def generate_cave(lines: List[List[str]]) -> Union(List[List[int]], int):
    cave_readings = {}

    for line in lines:
        window = sliding_window_view(np.array(line, dtype=object), window_shape=2)
        for slice in window:
            s1 = [int(i) for i in slice[0].split(",")]
            s2 = [int(i) for i in slice[1].split(",")]
            y_min = min([s1[1], s2[1]])
            y_max = max([s1[1], s2[1]])
            x_min = min([s1[0], s2[0]])
            x_max = max([s1[0], s2[0]])
            for y in range(y_min, y_max + 1):
                for x in range(x_min, x_max + 1):
                    if y not in cave_readings.keys():
                        cave_readings[y] = []
                    cave_readings[y].append(x)
    cave_coords = []
    for y in cave_readings.keys():
        for x in cave_readings[y]:
            cave_coords.append([x, y])
    floor = max([co[1] for co in cave_coords])
    return cave_coords, floor


def draw(cave: List[List[int]], sand=List[List[int]]):
    # plt.scatter(h_x, h_y, c="green")
    cave_x = [reading[0] for reading in cave]
    cave_y = [reading[1] for reading in cave]
    sand_x = [reading[0] for reading in sand]
    sand_y = [reading[1] for reading in sand]
    graph, cave_graph = plt.subplots(1)
    cave_graph.scatter(cave_x, cave_y, c="grey")
    cave_graph.scatter(sand_x, sand_y, c="khaki")
    cave_graph.invert_yaxis()
    plt.show()


def pour_sand(
    cave: List[List[int]],
    starting_point: List[int],
    max_y: int,
    until_grain: int = -1,
) -> Union(List[List[int]], int):
    def pour() -> bool:
        # down 1
        # if rest on something,
        # move left down 1
        # else move right down 1
        # if can't do either, stop
        #
        # if a gran falls past max_y
        # we are done
        falling = True
        at_rest = False
        current_position = {"x": starting_point[0], "y": starting_point[1]}
        while falling:
            if current_position["y"] + 1 > max_y:
                falling = False
                at_rest = False
            else:
                # can it go down
                if [current_position["x"], current_position["y"] + 1] not in cave:
                    current_position["y"] += 1
                    if verbose:
                        print(
                            f'move DOWN to x:{current_position["x"]}, y:{current_position["y"]}'
                        )
                # can it go left
                elif [current_position["x"] - 1, current_position["y"] + 1] not in cave:
                    current_position["x"] -= 1
                    current_position["y"] += 1
                    if verbose:
                        print(
                            f'move LEFT to x:{current_position["x"]}, y:{current_position["y"]}'
                        )
                # can it go right
                elif [current_position["x"] + 1, current_position["y"] + 1] not in cave:
                    if verbose:
                        print(
                            f'move RIGHT to x:{current_position["x"]}, y:{current_position["y"]}'
                        )
                    current_position["x"] += 1
                    current_position["y"] += 1
                else:
                    cave.append([current_position["x"], current_position["y"]])
                    falling = False
                    at_rest = True

        return at_rest

    more_can_fit = True
    grains = 0
    while more_can_fit:
        more_can_fit = pour()
        if more_can_fit:
            grains += 1
        if until_grain != -1:
            if grains >= until_grain:
                break
        if verbose:
            print(f"current grains: {grains}")

    return cave, grains


def main():
    input_file = "./test_input.txt"
    input_file = "./input.txt"
    lines = []
    with open(input_file, "r") as input:
        for line in input:
            line = line.strip()
            line = line.split(" -> ")
            lines.append(line)

    original_cave, floor = generate_cave(lines)
    sand_filled_cave, total_grains = pour_sand(
        deepcopy(original_cave), [500, 0], floor, -1
    )
    write_output(output_file1, total_grains)

    just_sand = [x for x in sand_filled_cave if x not in original_cave]
    # print(f"floor: {floor}")

    draw(original_cave, just_sand)


if __name__ == "__main__":
    main()
