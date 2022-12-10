from __future__ import annotations
from typing import List, Union, Dict
import base64

# incorrect = 4156 (Using any space)
# incorrect = 3218 (Using preferred route) (too high)
# incorrect = 2599 (using orth or diag rules)


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


input_file = "./input.txt"
# input_file = "./test_input.txt"
output_file1 = "./output1.txt"
output_file2 = "./output2.txt"


class Head:
    def __init__(self, starting_pos: List(int) = [0, 0]) -> None:
        self._pos_current = {"x": 0, "y": 0}
        self._around_me = []
        self._update_around_me()
        self._positions = []
        self._update_history()

    def link(self, obsession: Union[Head, Tail]):
        pass

    def _to_str(self, x: int, y: int) -> str:
        return f"{x},{y}"

    def _to_pos(self, coords: str) -> tuple[int, int]:
        coords = coords.split(",")
        return int(coords[0]), int(coords[1])

    def _coords(self):
        return self._to_str(self._pos_current["x"], self._pos_current["y"])

    def _update_history(self):
        self._positions.append(self._coords())

    def history(self, unique: bool = False) -> List[List[int]]:
        output = []
        for p in self._positions:
            x, y = self._to_pos(p)
            output.append([x, y])
        return set(output) if unique else output

    def _update_around_me(self):
        self._around_me = [
            self._to_str(self._pos_current["x"] - 1, self._pos_current["y"] + 1),
            self._to_str(self._pos_current["x"], self._pos_current["y"] + 1),
            self._to_str(self._pos_current["x"] + 1, self._pos_current["y"] + 1),
            self._to_str(self._pos_current["x"] - 1, self._pos_current["y"]),
            self._to_str(self._pos_current["x"] + 1, self._pos_current["y"]),
            self._to_str(self._pos_current["x"] - 1, self._pos_current["y"] - 1),
            self._to_str(self._pos_current["x"], self._pos_current["y"] - 1),
            self._to_str(self._pos_current["x"] + 1, self._pos_current["y"] - 1),
        ]

    def around(self) -> List(List(str)):
        return self._around_me

    def position(self) -> Dict[str, str]:
        return self._pos_current

    def _move_right(self):
        self._pos_current["x"] += 1

    def _move_left(self):
        self._pos_current["x"] -= 1

    def _move_up(self):
        self._pos_current["y"] += 1

    def _move_down(self):
        self._pos_current["y"] -= 1

    def move(self, direction: str) -> None:
        direction_func = {
            "L": self._move_left,
            "R": self._move_right,
            "U": self._move_up,
            "D": self._move_down,
        }
        direction_func[direction]()
        self._update_around_me()
        self._update_history()
        # print(f"moved head to {self._coords()}")


class Tail:
    def __init__(self, starting_pos: List(int) = [0, 0]) -> None:
        # Set initial tail position.
        self._pos_current: Dict[str, int] = {"x": starting_pos[0], "y": starting_pos[1]}
        self._around_me: List[str] = []
        self._positions: List[str] = []
        self._obsession: Union[Head, Tail, None] = None
        self._update_around_me()
        self._update_history()

    def _to_str(self, x: int, y: int) -> str:
        return f"{x},{y}"

    def _to_pos(self, coords: str) -> tuple[int, int]:
        coords = coords.split(",")
        return int(coords[0]), int(coords[1])

    def _coords(self):
        return self._to_str(self._pos_current["x"], self._pos_current["y"])

    def position(self) -> Dict[str, str]:
        return self._pos_current

    def _update_around_me(self):
        # 1 2 3
        # 8 x 4
        # 7 6 5
        self._around_me = [
            self._to_str(self._pos_current["x"] - 1, self._pos_current["y"] + 1),  # 1
            self._to_str(self._pos_current["x"], self._pos_current["y"] + 1),  # 2
            self._to_str(self._pos_current["x"] + 1, self._pos_current["y"] + 1),  # 3
            self._to_str(self._pos_current["x"] + 1, self._pos_current["y"]),  # 4
            self._to_str(self._pos_current["x"] + 1, self._pos_current["y"] - 1),  # 5
            self._to_str(self._pos_current["x"], self._pos_current["y"] - 1),  # 6
            self._to_str(self._pos_current["x"] - 1, self._pos_current["y"] - 1),  # 7
            self._to_str(self._pos_current["x"] - 1, self._pos_current["y"]),  # 8
        ]

    def _update_history(self):
        self._positions.append(self._coords())

    def history(self, unique: bool = False) -> List[List[int]]:
        output = []
        for p in self._positions:
            x, y = self._to_pos(p)
            output.append([x, y])
        return set(output) if unique else output

    def history_count(self, unique: bool = False) -> int:
        return len(set(self._positions)) if unique else len(self._positions)

    def link(self, obsession: Union[Head, Tail]):
        self._obsession = obsession

    def _obsession_str_position(self) -> str:
        obsession_position = self._obsession.position()
        return self._to_str(obsession_position["x"], obsession_position["y"])

    def _under_obsession(self):
        if self._obsession_str_position() == self._coords():
            return True
        else:
            return False

    def _is_obsession_close(self) -> bool:
        if self._under_obsession():
            return True
        elif self._obsession_str_position() in self._around_me:
            return True
        else:
            return False

    # def _obsession_allowed_coords(self) -> Dict[str, List[str]]:
    #     # a 2 b
    #     # 1 H 3
    #     # c 4 d
    #     return {
    #         "orthogonal": [
    #             self._to_str(
    #                 self._obsession.position()["x"] - 1, self._obsession.position()["y"]
    #             ),  # 1
    #             self._to_str(
    #                 self._obsession.position()["x"], self._obsession.position()["y"] + 1
    #             ),  # 2
    #             self._to_str(
    #                 self._obsession.position()["x"] + 1, self._obsession.position()["y"]
    #             ),  # 3
    #             self._to_str(
    #                 self._obsession.position()["x"], self._obsession.position()["y"] - 1
    #             ),  # 4
    #         ],
    #         "diagonal": [
    #             self._to_str(
    #                 self._obsession.position()["x"] - 1,
    #                 self._obsession.position()["y"] + 1,
    #             ),  # a
    #             self._to_str(
    #                 self._obsession.position()["x"] + 1,
    #                 self._obsession.position()["y"] + 1,
    #             ),  # b
    #             self._to_str(
    #                 self._obsession.position()["x"] - 1,
    #                 self._obsession.position()["y"] - 1,
    #             ),  # c
    #             self._to_str(
    #                 self._obsession.position()["x"] + 1,
    #                 self._obsession.position()["y"] - 1,
    #             ),  # d
    #         ],
    #     }

    def _move_to_obsession(self):
        moved = False
        if (
            self._obsession.position()["x"] == self._pos_current["x"]
            or self._obsession.position()["y"] == self._pos_current["y"]
        ):
            move = []
            # move towards the obsession on the same plane
            if self._obsession.position()["x"] == self._pos_current["x"]:
                # move on y axis
                if self._obsession.position()["y"] > self._pos_current["y"]:
                    # Move up
                    # O
                    # *
                    # T
                    move = ["y", 1]
                else:
                    # Move down
                    # T
                    # *
                    # O
                    move = ["y", -1]

            if self._obsession.position()["y"] == self._pos_current["y"]:
                # move on x axis
                if self._obsession.position()["x"] > self._pos_current["x"]:
                    # Move Right
                    # T * O
                    move = ["x", 1]
                else:
                    # Move Left
                    # O * T
                    move = ["x", -1]
            self._pos_current[move[0]] += move[1]
            moved = True
        else:
            # move towards obsession diagonally
            # Obsession can only be in one of numbered spaces.
            # move into a,b,c or d towards it.
            # 1 2 * 0 1
            # 0 a * b 2
            # * * T * *
            # 0 c * d 0
            # 1 2 * 2 1
            ob_pos_str = self._obsession_str_position()
            a = [
                self._to_str(self._pos_current["x"] - 2, self._pos_current["y"] + 1),
                self._to_str(self._pos_current["x"] - 2, self._pos_current["y"] + 2),
                self._to_str(self._pos_current["x"] - 1, self._pos_current["y"] + 2),
            ]
            b = [
                self._to_str(self._pos_current["x"] + 1, self._pos_current["y"] + 2),
                self._to_str(self._pos_current["x"] + 2, self._pos_current["y"] + 2),
                self._to_str(self._pos_current["x"] + 2, self._pos_current["y"] + 1),
            ]
            c = [
                self._to_str(self._pos_current["x"] - 2, self._pos_current["y"] - 1),
                self._to_str(self._pos_current["x"] - 2, self._pos_current["y"] - 2),
                self._to_str(self._pos_current["x"] - 1, self._pos_current["y"] - 2),
            ]
            d = [
                self._to_str(self._pos_current["x"] + 2, self._pos_current["y"] - 1),
                self._to_str(self._pos_current["x"] + 2, self._pos_current["y"] - 2),
                self._to_str(self._pos_current["x"] + 1, self._pos_current["y"] - 2),
            ]
            # print(f"ob_pos_str: {ob_pos_str}. Possibles: {a} {b} {c} {d}")
            if ob_pos_str in a:
                self._pos_current["x"] = self._pos_current["x"] - 1
                self._pos_current["y"] = self._pos_current["y"] + 1
                moved = True
            elif ob_pos_str in b:
                self._pos_current["x"] = self._pos_current["x"] + 1
                self._pos_current["y"] = self._pos_current["y"] + 1
                moved = True
            elif ob_pos_str in c:
                self._pos_current["x"] = self._pos_current["x"] - 1
                self._pos_current["y"] = self._pos_current["y"] - 1
                moved = True
            elif ob_pos_str in d:
                self._pos_current["x"] = self._pos_current["x"] + 1
                self._pos_current["y"] = self._pos_current["y"] - 1
                moved = True

        if moved:
            self._update_around_me()
            self._update_history()
            return

        # If we couldn't make a move, there is an error
        raise (
            Exception(
                f"Rope knot could not find a space near obsession. Me: {self._pos_current} | Obsession: {self._obsession._pos_current}"
            )
        )

    def follow_obsession(self):
        # Do I need to move
        #   Am I under my obsession
        #   Am I near my obsession
        if self._is_obsession_close():
            # print(f"tail stays in {self._coords()}")
            pass
        else:
            self._move_to_obsession()
            # print(f"moved tail to {self._coords()}")


class Rope:
    def __init__(self, joints: int, starting_pos: List[int] = [0, 0]) -> None:
        self._head = Head(starting_pos)
        self._tails = [Tail(starting_pos) for _ in range(0, joints - 1)]
        self._tails[0].link(self._head)
        for i, t in enumerate(self._tails[1:], 1):
            t.link(self._tails[i - 1])

    def move(self, direction: str, steps: int):
        for _ in range(0, steps):
            self._head.move(direction)
            for tail in self._tails:
                tail.follow_obsession()

    def tail_history_count(self, unique: bool = False):
        return self._tails[-1].history_count(unique)


def main():
    rope = Rope(10)

    with open(input_file, "r") as input:
        for line in input:
            line = line.strip()
            instruction = line.split(" ")
            rope.move(instruction[0], int(instruction[1]))

    write_output(output_file2, rope.tail_history_count(unique=True))


if __name__ == "__main__":
    main()
