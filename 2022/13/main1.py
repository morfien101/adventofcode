from __future__ import annotations
from typing import List, Union
import base64
import functools

# incorrect 70
# incorrect 5459


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


output_file1 = "./output1.txt"
output_file2 = "./output2.txt"


def compare(left, right):
    out, _ = process(1, left, right)
    return out


def process(index, left, right) -> Union(int, bool):
    index += 1
    out = 0
    _continue = None
    if isinstance(left, int) and isinstance(right, int):
        if left > right:
            out, _continue = -1, False
        elif left == right:
            out, _continue = 0, True
        else:
            out, _continue = 1, False

    # int vs list
    if isinstance(left, int) and isinstance(right, list):
        out, _continue = process(index, [left], right)

    # list vs int
    if isinstance(left, list) and isinstance(right, int):
        out, _continue = process(index, left, [right])

    # list vs list
    if isinstance(left, list) and isinstance(right, list):
        # Set _continue to true, so we can go through the loop until
        # we get a false. If we keep getting continues and the left
        # runs out of checks, the left is smaller and we return True
        _continue = True
        # Stop if we get an empty list.
        if len(left) > 0 and len(right) == 0:
            # If the left has items but right doesn't it's
            # Left is too big and its false.
            print(f"{index} Right has no items - {left} vs {right}")
            out, _continue = -1, False
        elif len(left) == 0 and len(right) > 0:
            # If left is empty and right still has items,
            # left is smaller than right and its correct.
            print(f"{index} Left has no items - {left} vs {right}")
            out, _continue = 1, False
        elif len(left) == 0 and len(right) == 0:
            out, _continue = 0, True
        # Else continue to look at items in the list
        else:
            for li, l in enumerate(left):
                if li > len(right) - 1:
                    out, _continue = -1, False
                    print(f"{index} Left too big - {left} vs {right}")
                    break
                out, _continue = process(index, l, right[li])
                if _continue == False:
                    break
                if li == len(left) - 1 and len(right) - 1 > li:
                    out, _continue = 1, False

    print(
        f"{index} - process: {left} vs {right} | {type(left)} {type(right)} -> _continue: {_continue}, out: {out}"
    )
    return out, _continue


def main():
    input_file = "./input.txt"
    # input_file = "./test_input.txt"

    messages: List[List:any] = []
    current_lines: List[str] = []
    with open(input_file, "r") as input:

        for line in input:
            line = line.strip()
            if line == "":
                messages.append([eval(current_lines[0]), eval(current_lines[1])])
                current_lines = []
            else:
                current_lines.append(line)
        # There are 2 lines at the bottom that have no new line at the end.
        messages.append([eval(current_lines[0]), eval(current_lines[1])])
        current_lines = []

    message_correct = []
    for i, mp in enumerate(messages, 1):
        print(f"-------------- {i} ----------------")
        correct, _ = process(0, mp[0], mp[1])
        print("---------------------------------")
        if correct == 1:
            message_correct.append(i)
    write_output(output_file1, sum(message_correct))

    corrected_messages = []
    for idx, msgs in enumerate(messages):
        if idx in message_correct:
            corrected_messages.append(msgs[0])
            corrected_messages.append(msgs[1])
        else:
            corrected_messages.append(msgs[1])
            corrected_messages.append(msgs[0])

    mark1 = [[2]]
    mark2 = [[6]]
    corrected_messages.append(mark1)
    corrected_messages.append(mark2)

    # print(corrected_messages)

    p2 = sorted(corrected_messages, key=functools.cmp_to_key(compare), reverse=True)
    # for i in p2:
    #    print(i)
    write_output(output_file2, (p2.index(mark1) + 1) * (p2.index(mark2) + 1))


if __name__ == "__main__":
    main()
