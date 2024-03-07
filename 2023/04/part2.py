from typing import Tuple, List

import os
import re
from collections import defaultdict

# 2: 9997537

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
    return matches


cards = defaultdict(lambda: {"matches": 0, "copies": 1})

with open(input, "r") as file:
    for line in file.readlines():
        current_card, winning_numbers, player_numbers = digest_line(line)
        matches = read_card(winning_numbers, player_numbers)
        cards[current_card]["matches"] = matches
        # print(f"current_card: {current_card} | matches {matches}")

for k in cards.keys():
    if cards[k]["matches"] > 0:
        for _ in range(cards[k]["copies"]):
            for i in range(1, cards[k]["matches"] + 1):
                cards[k + i]["copies"] += 1

# for k, v in cards.items():
#     print(f"card: {k}: {v}")

print(f"copies: {sum([v['copies'] for v in cards.values()])}")
