import re
from typing import Dict, List
from collections import defaultdict
from math import prod

input = "input.txt"
# input = "test.txt"

game_test = {"red": 12, "green": 13, "blue": 14}


class Game:
    def __init__(self, line):
        self.line = line.strip()
        self.id = self.id(line)
        self.hands = self.hands(line)

    def __str__(self):
        return f"Game: {self.id} - {self.hands}"

    def id(self, line) -> int:
        return int(re.search(r" (\d+):", line).group(1))

    def hands(self, line) -> List[Dict[str, int]]:
        out = []
        current_hand = re.search("^.*: (.*)$", line).group(1)
        for hand in current_hand.split("; "):
            current_reveal = {}
            for dice in hand.split(", "):
                dice_components = dice.split(" ")
                current_reveal[dice_components[1]] = int(dice_components[0])

            out.append(current_reveal)

        return out

    def possible(self, game_test) -> int:
        for hand in self.hands:
            for color in hand:
                if hand[color] > game_test[color]:
                    return 0

        return self.id

    def minimum_required(self) -> Dict[str, int]:
        out = defaultdict(int)
        for hand in self.hands:
            for key in hand.keys():
                if hand[key] > out[key]:
                    out[key] = hand[key]
        return out

    def power_set(self) -> int:
        powers = []
        for v in self.minimum_required().values():
            powers.append(v)

        return prod(powers)


with open(input, "r") as file:
    games = []

    for line in file.readlines():
        games.append(Game(line))

    possibilities = []
    power_sets = []
    for game in games:
        possibilities.append(game.possible(game_test))
        power_sets.append(game.power_set())
        # print(game.power_set())

    possibilities = [x for x in possibilities if x != 0]
    # print(possibilities)
    print(sum(possibilities))
    print(sum(power_sets))
