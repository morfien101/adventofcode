from typing import Tuple, List

import os
import re

# 1: 26218

base_path = os.path.abspath(__file__)
input = os.path.join(os.path.dirname(base_path), "input.txt")
# input = os.path.join(os.path.dirname(base_path), "test.txt")


def digest_line(line: str) -> Tuple[int, List[int], List[int]]:
    read_pattern = r"(\d+):\s*(\d+(?:\s+\d+)*)\s\|\s*(\d+(?:\s+\d+)*)"
    match = re.search(read_pattern, line)

    if match:
        card_number = int(match.group(1))
        winning_numbers = [int(n) for n in match.group(2).split()]
        player_numbers = [int(n) for n in match.group(3).split()]
        return (card_number, winning_numbers, player_numbers)
    else:
        raise "Failed to find numbers!"


def read_card(winning_numbers: List[int], player_numbers: List[int]):

    matches = 0

    for x in player_numbers:
        if x in winning_numbers:
            matches += 1

    n = 1 if matches >= 1 else 0
    shift = matches - 1 if matches > 1 else 0
    return n << shift


def part1():
    points = []
    with open(input, "r") as file:
        for line in file.readlines():
            _, winning_numbers, player_numbers = digest_line(line)
            points.append(read_card(winning_numbers, player_numbers))

    print(f"total points: {sum(points)}")


part1()
