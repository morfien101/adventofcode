from __future__ import annotations
from typing import List, Union, Dict
import base64
from numpy.lib.stride_tricks import sliding_window_view
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from collections import defaultdict


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


output_file1 = "./output1.txt"
output_file2 = "./output2.txt"
verbose = False


def generate_cave(lines: List[List[str]]) -> Dict[str, List[int]]:
    cave_readings = defaultdict(list)

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

    return cave_readings


def draw(cave: Dict[str, List[int]], sand: Dict[str, List[int]]):
    _, cave_graph = plt.subplots(1)
    cave_graph.scatter(cave["x"], cave["y"], c="grey")
    cave_graph.scatter(sand["x"], sand["y"], c="khaki")
    cave_graph.invert_yaxis()
    # plt.rcParams["axes.axisbelow"] = True
    # plt.grid(which="minor", axis="y", zorder=-1.0)

    plt.show()


def convert_to_plotable(rows: Dict[int, List[int]]) -> Dict(str, List[int]):
    raw = []
    for y in rows.keys():
        for x in rows[y]:
            raw.append([x, y])

    return {"x": [point[0] for point in raw], "y": [point[1] for point in raw]}


def remove_walls(
    original_cave: Dict[int, List[int]], sand_filled_cave: Dict[int, List[int]]
) -> Dict[int, List[int]]:
    for y in original_cave:
        for x in original_cave[y]:
            try:
                sand_filled_cave[y].pop(sand_filled_cave[y].index(x))
            except:
                pass
    return sand_filled_cave


def pour_sand(
    cave: Dict[int, List[int]],
    starting_point: List[int],
    include_floor: bool = False,
    grains: int = -1,
) -> Union(Dict[int, List[int]], int):

    cave_lowest = max([y for y in cave.keys()])

    def pour() -> bool:
        falling = True
        at_rest = False

        current_position = {"x": starting_point[0], "y": starting_point[1]}
        if starting_point[0] in cave[starting_point[1]]:
            # There is something at rest in the starting point
            return False
        while falling:
            if include_floor:
                if current_position["y"] + 1 == cave_lowest + 2:
                    cave[current_position["y"]].append(current_position["x"])
                    at_rest = True
                    break
            else:
                if current_position["y"] > cave_lowest:
                    at_rest = False
                    break

            if current_position["x"] not in cave[current_position["y"] + 1]:
                current_position["y"] += 1
            elif current_position["x"] - 1 not in cave[current_position["y"] + 1]:
                current_position["x"] -= 1
                current_position["y"] += 1
            elif current_position["x"] + 1 not in cave[current_position["y"] + 1]:
                current_position["x"] += 1
                current_position["y"] += 1
            else:
                falling = False
                at_rest = True
                cave[current_position["y"]].append(current_position["x"])

        return at_rest

    can_fit_more = True
    current_grains = 0
    while can_fit_more:
        can_fit_more = pour()
        if grains != -1:
            if current_grains >= grains:
                break
        if can_fit_more:
            current_grains += 1
        # print(f"current grains: {current_grains}")

    return cave, current_grains


def main():
    # input_file = "./test_input.txt"
    input_file = "./input.txt"
    lines = []
    with open(input_file, "r") as input:
        for line in input:
            line = line.strip()
            line = line.split(" -> ")
            lines.append(line)

    original_cave = generate_cave(lines)

    # No floor
    sand_filled_cave, total_grains = pour_sand(
        deepcopy(original_cave), [500, 0], False, -1
    )
    write_output(output_file1, total_grains)

    # With floor
    sand_filled_cave, total_grains = pour_sand(
        deepcopy(original_cave), [500, 0], True, -1
    )
    write_output(output_file2, total_grains)

    # Draws a cave
    # sand_filled_cave = remove_walls(original_cave, sand_filled_cave)
    # draw(convert_to_plotable(original_cave), convert_to_plotable(sand_filled_cave))


if __name__ == "__main__":
    main()
