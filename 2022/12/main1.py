from __future__ import annotations
from typing import List, Union, Dict
import base64
import networkx


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


output_file1 = "./output1.txt"
output_file2 = "./output2.txt"


def s_to_i(s: str) -> int:
    return ord(s)


def can_step(f: str, t: str):
    f = s_to_i(f)
    t = s_to_i(t)

    if f + 1 == t:
        return True
    elif f >= t:
        return True


def make_label(x: int, y: int) -> str:
    return f"x:{x},y:{y}"


def generate_graph(grid: List[List[str]]) -> networkx.DiGraph:
    graph = networkx.DiGraph()

    for yi, row in enumerate(grid):
        for xi, _ in enumerate(row):
            current_node_label = make_label(xi, yi)
            # graph.add_node(current_node_label)

            def add_left():
                if can_step(row[xi], row[xi - 1]):
                    graph.add_edge(current_node_label, make_label(xi - 1, yi))

            def add_right():
                if can_step(row[xi], row[xi + 1]):
                    graph.add_edge(current_node_label, make_label(xi + 1, yi))

            def add_up():
                if can_step(row[xi], grid[yi - 1][xi]):
                    graph.add_edge(current_node_label, make_label(xi, yi - 1))

            def add_down():
                if can_step(row[xi], grid[yi + 1][xi]):
                    graph.add_edge(current_node_label, make_label(xi, yi + 1))

            # work out left right blocks
            if xi > 0 and xi < len(row) - 1:
                # I have left and right blocks
                # left
                add_left()
                # right
                add_right()
            elif xi == 0:
                # Right only
                add_right()
            elif xi == len(row) - 1:
                # left only
                add_left()

            # work out up down
            if yi > 0 and yi < len(grid) - 1:
                add_down()
                add_up()
            elif yi == 0:
                add_down()
            elif yi == len(grid) - 1:
                add_up()

    return graph


def part1(g: networkx.DiGraph, start: str, end: str):
    length = networkx.shortest_path_length(g, start, end)
    write_output(output_file1, length)


def part2(g: networkx.DiGraph, the_map: List[List[str]], end: str):
    starting_positions: List[str] = []
    path_lengths: List[int] = []

    # find a nodes
    for yi, _ in enumerate(the_map):
        for xi, _ in enumerate(the_map[yi]):
            if the_map[yi][xi] == "a":
                starting_positions.append(make_label(xi, yi))

    for start in starting_positions:
        try:
            l = networkx.shortest_path_length(g, start, end)
            path_lengths.append(l)
        except networkx.exception.NetworkXNoPath:
            continue

    write_output(output_file2, min(path_lengths))


def main():
    input_file = "./input.txt"
    # input_file = "./test_input.txt"
    the_map = []
    start_pos = []
    end_pos = []
    with open(input_file, "r") as input:
        for line in input:
            line = line.strip()
            the_map.append(list(line))

    found_start = False
    found_end = False

    for idx_y, row in enumerate(the_map):
        if "S" in the_map[idx_y]:
            found_start = True
            start_pos = [the_map[idx_y].index("S"), idx_y]
            the_map[start_pos[1]][start_pos[0]] = "a"

        if "E" in the_map[idx_y]:
            found_end = True
            end_pos = [the_map[idx_y].index("E"), idx_y]
            the_map[end_pos[1]][end_pos[0]] = "z"

        if found_start and found_end:
            break

    g = generate_graph(the_map)
    start_label = make_label(start_pos[0], start_pos[1])
    end_label = make_label(end_pos[0], end_pos[1])

    part1(g, start_label, end_label)
    part2(g, the_map, end_label)


if __name__ == "__main__":
    main()
