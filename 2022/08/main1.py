from typing import List
import base64
import math


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


input_file = "./input.txt"
# input_file = "./test_input.txt"
output_file1 = "./output1.txt"
output_file2 = "./output2.txt"

grid = []

with open(input_file, "r") as input:
    for line in input:
        grid.append(list(line.strip()))


cols = len(grid[0])
rows = len(grid)
outside_trees = (cols * 2) + ((rows * 2) - 4)
visible_internal_trees = 0

max_row = rows
max_col = cols

# Go through each row from index 1 to len(grid_rows) -1 (second last row)
for row_index, row in enumerate(grid[1 : max_row - 1], 1):
    # print(f"row_index = {row_index}")
    # Go through trees 1 to len(row) - 1
    for tree_index, current_tree in enumerate(row[1 : max_col - 1], 1):
        # print(f"tree_index = {tree_index}")

        # check row
        left_side = range(0, tree_index)
        right_side = range(tree_index + 1, cols)

        # check col
        top = range(0, row_index)
        bottom = range(row_index + 1, rows)

        seen_from_left = True
        seen_from_right = True
        seen_from_top = True
        seen_from_bottom = True

        for tree in left_side:
            # print(
            #     f"left - index {tree} -> current tree index = {tree_index} | {grid[row_index][tree]} > {current_tree}"
            # )
            if grid[row_index][tree] >= current_tree:
                seen_from_left = False
                break

        for tree in right_side:
            # print(
            #     f"right - index {tree} -> current tree index = {tree_index} | {grid[row_index][tree]} > {current_tree}"
            # )
            if grid[row_index][tree] >= current_tree:
                seen_from_right = False
                break

        for testing_row_index in top:
            # print(
            #     f"top - row index {row_index} testing row {testing_row_index} | {grid[testing_row_index][tree_index]} > {current_tree}"
            # )
            if grid[testing_row_index][tree_index] >= current_tree:
                seen_from_top = False
                break

        for testing_row_index in bottom:
            # print(
            #     f"bottom - row index {row_index} testing row {testing_row_index} | {grid[testing_row_index][tree_index]} > {current_tree}"
            # )
            if grid[testing_row_index][tree_index] >= current_tree:
                seen_from_bottom = False
                break

        if True in [seen_from_top, seen_from_bottom, seen_from_left, seen_from_right]:
            visible_internal_trees += 1

write_output(output_file1, visible_internal_trees + outside_trees)


scenic_scores = []
for current_row_index, current_row in enumerate(grid):
    for current_tree_index, current_tree in enumerate(current_row):
        current_trees_seen = []

        # trees left of me
        if current_tree_index != 0:
            tree_count = 0
            for i in range(current_tree_index - 1, -1, -1):
                tree_count += 1
                if current_row[i] >= current_tree:
                    break
            current_trees_seen.append(tree_count)
        else:
            current_trees_seen.append(0)
            # print(
            #     f"current tree - x: {current_row_index+1} y: {current_tree_index} | skip left"
            # )

        # trees right of me
        if current_tree_index != len(current_row) - 1:
            tree_count = 0
            for t in current_row[current_tree_index + 1 :]:
                tree_count += 1
                if t >= current_tree:
                    break
            current_trees_seen.append(tree_count)
        else:
            current_trees_seen.append(0)
            # print(
            #     f"current tree - x: {current_row_index+1} y: {current_tree_index} | skip right"
            # )

        # trees above me
        if current_row_index != 0:
            tree_count = 0
            for i in range(current_row_index - 1, -1, -1):
                tree_count += 1
                if grid[i][current_tree_index] >= current_tree:
                    break
            current_trees_seen.append(tree_count)
        else:
            current_trees_seen.append(0)
            # print(
            #     f"current tree - x: {current_row_index+1} y: {current_tree_index} | skip top"
            # )

        # trees below me
        if current_row_index != len(grid) - 1:
            tree_count = 0
            for i in range(current_row_index + 1, len(grid)):
                tree_count += 1
                if grid[i][current_tree_index] >= current_tree:
                    break
            current_trees_seen.append(tree_count)
        else:
            current_trees_seen.append(0)
            # print(
            #     f"current tree - x: {current_row_index+1} y: {current_tree_index} | skip bottom"
            # )

        scenic_scores.append(math.prod(current_trees_seen))
        # print(
        #     f"current tree - x: {current_row_index+1} y: {current_tree_index} | scores {current_trees_seen} | product {math.prod(current_trees_seen)}"
        # )

write_output(output_file2, max(scenic_scores))
