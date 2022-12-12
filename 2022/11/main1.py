from __future__ import annotations
from typing import List, Union, Callable, Dict
import base64
import re
import math
from copy import deepcopy

# incorrect p2: 18956452272


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


output_file1 = "./output1.txt"
output_file2 = "./output2.txt"
test_output_file = "./test_output.txt"


class Monkey:
    def __init__(
        self,
        starting_items: List[int],
        friend_ids: List[int],
        worry_func: Callable[[int], int],
        friend_test: int,
    ) -> None:
        # Setup now
        self._friend_ids: List[int] = friend_ids
        self._worry_func: Callable[[int], int] = worry_func
        self._friend_test: int = friend_test

        # Set by functions
        self._friends: Dict[bool, Monkey] = {}
        self._items: List[int] = starting_items
        self._handled_count: int = 0
        self._reducer = lambda input: input

    def find_friends(self, friends: List[Monkey]):
        self._friends[True] = friends[self._friend_ids[0]]
        self._friends[False] = friends[self._friend_ids[1]]

    def play(self):
        while len(self._items) > 0:
            self._handled_count += 1
            item = self._worry_func(self._items.pop(0))
            item = self._reducer(item)
            mod_bool = item % self._friend_test == 0
            self._friends[mod_bool].catch(item)

    def catch(self, item: int):
        self._items.append(item)

    def items_handled(self):
        return self._handled_count

    def set_reducer(self, f: Callable[[int], int]):
        self._reducer = f


def operation_factory(symbol: str, raiser: str):
    if symbol == "+":
        if raiser == "old":
            return lambda worry: worry + worry
        else:
            return lambda worry: worry + int(raiser)
    elif symbol == "*":
        if raiser == "old":
            return lambda worry: worry**2
        else:
            return lambda worry: worry * int(raiser)


def create_monkey(description: List[str]) -> Union(Monkey, int):
    for line in description:
        if line.startswith("Starting items:"):
            items = re.findall(r"(\d+)", line)
            items = [int(i) for i in items]
        elif line.startswith("Operation:"):
            op = re.search(r"(?P<symbol>[\*\+]) (?P<raiser>\d+|old)$", line)
            worry_func = operation_factory(op.group("symbol"), op.group("raiser"))
        elif line.startswith("Test:"):
            friend_test = int(re.search(r"(?P<num>\d+)", line).group("num"))
        elif line.startswith("If true:"):
            true_friend = int(re.search(r"(?P<friend>\d+)", line).group("friend"))
        elif line.startswith("If false:"):
            false_friend = int(re.search(r"(?P<friend>\d+)", line).group("friend"))

    return (
        Monkey(items, [true_friend, false_friend], worry_func, friend_test),
        friend_test,
    )


def generate_monkeys(input_file: str) -> List[Monkey]:
    current_monkey_lines = []
    monkeys: List[Monkey] = []
    reducers: List[int] = []
    with open(input_file, "r") as input:
        for line in input:
            line = line.strip()
            current_monkey_lines.append(line)
            if line == "":
                new_monkey, reducer_value = create_monkey(current_monkey_lines)
                monkeys.append(new_monkey)
                reducers.append(reducer_value)
                current_monkey_lines = []
        # Create the last monkey. This is because there is no new line after the last monkey.
        new_monkey, reducer_value = create_monkey(current_monkey_lines)
        monkeys.append(new_monkey)
        reducers.append(reducer_value)
        current_monkey_lines = []

    for monkey in monkeys:
        monkey.find_friends(monkeys)

    reducer_prod = math.prod(reducers)
    print(f"Reducers: {reducers} = {reducer_prod}")
    return monkeys, reducer_prod


def run(
    monkeys: List[Monkey],
    rounds: int,
    output_file: str,
    reducer_func: Callable[[int], int],
    test_mode: bool = False,
):
    for monkey in monkeys:
        monkey.set_reducer(reducer_func)

    for i in range(0, rounds):
        print(f"Round: {i+1}")
        for monkey in monkeys:
            monkey.play()

    counts = [monkey.items_handled() for monkey in monkeys]
    counts.sort(reverse=True)
    if test_mode:
        print(counts)
    write_output(output_file, math.prod(counts[0:2]))


def main():

    # Testing
    # monkeys = generate_monkeys("./test_input.txt")
    # run(monkeys, 1, 10000, test_output_file, True)

    # Proper
    monkeys, reducer_value = generate_monkeys("./input.txt")
    run(deepcopy(monkeys), 20, output_file1, lambda x: x // 3)
    run(deepcopy(monkeys), 10000, output_file2, lambda x: x % reducer_value)


if __name__ == "__main__":
    main()
