input_file = "./input.txt"
output_file = "./output2.txt"


def count_chars(col: list, highest_occurrence: bool, tie_breaker: str):
    result = {"0": 0, "1": 0}

    for char in col:
        if f"{char}" == "0":
            result["0"] += 1
        else:
            result["1"] += 1

    if result["0"] == result["1"]:
        return tie_breaker
    elif result["0"] > result["1"]:
        return "0" if highest_occurrence else "1"
    else:
        return "1" if highest_occurrence else "0"


def reduce_grid(
    grid: list, current_idx: int, highest_occurrence: bool, tie_breaker: str
):
    working_col = [row[current_idx] for row in grid]
    key = count_chars(working_col, highest_occurrence, tie_breaker)

    new_grid = [row for row in grid if row[current_idx] == key]

    # print(
    #     f"key: {key}, current_index: {current_idx}, grid_size: {len(new_grid)}, old_grid: {len(grid)}"
    # )
    # for line in new_grid:
    #     print(line)

    if len(new_grid) == 1:
        return int("".join(new_grid[0]), 2)
    else:
        return reduce_grid(new_grid, current_idx + 1, highest_occurrence, tie_breaker)


def main():
    with open(input_file, "r") as input:
        grid = [list(line.strip()) for line in input]

    oxygen = reduce_grid(grid, 0, True, "1")
    co2 = reduce_grid(grid, 0, False, "0")

    print("Oxygen:", oxygen)
    print("CO2:", co2)
    print("Life support:", oxygen * co2)


if __name__ == "__main__":
    main()
