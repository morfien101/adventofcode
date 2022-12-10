from typing import List
import base64
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# incorrect = 6417


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


input_file = "./input.txt"
# input_file = "./test_input.txt"
output_file1 = "./output1.txt"
output_file2 = "./output2.txt"


class Rope:
    def __init__(self) -> None:
        # Plane of movement.
        #
        #   [x, y]
        #   |
        # y |
        #   |
        #   + - - - -
        #       x

        # Set initial head position.
        self._head_current = {"x": 0, "y": 0}
        self._around_head = []
        self._update_around_head()

        # Set initial tail position.
        self._tail_current = {"x": 0, "y": 0}
        self._around_tail = []
        self._update_around_tail()

        # Where have they been, unique spaces.
        self._head_positions = []
        self._tail_positions = []
        self._update_head_history()
        self._update_tail_history()

    def _to_str(self, x: int, y: int) -> str:
        return f"{x},{y}"

    def _to_pos(self, coords: str) -> tuple[int, int]:
        coords = coords.split(",")
        return int(coords[0]), int(coords[1])

    def _head_coords(self):
        return self._to_str(self._head_current["x"], self._head_current["y"])

    def _tail_coords(self):
        return self._to_str(self._tail_current["x"], self._tail_current["y"])

    def _update_head_history(self):
        self._head_positions.append(self._head_coords())
        # print(f"Head: {self._head_coords()}")

    def _update_tail_history(self):
        self._tail_positions.append(self._tail_coords())
        # print(f"Tail: {self._tail_coords()}")

    def tail_history(self, unique: bool = False) -> List[List[int]]:
        output = []
        for p in self._tail_positions:
            x, y = self._to_pos(p)
            output.append([x, y])
        return set(output) if unique else output

    def head_history(self, unique: bool = False) -> List[List[int]]:
        output = []
        for p in self._head_positions:
            x, y = self._to_pos(p)
            output.append([x, y])
        return set(output) if unique else output

    def tail_history_count(self, unique: bool = False) -> int:
        return len(set(self._tail_positions)) if unique else len(self._tail_positions)

    def head_history_count(self, unique: bool = False) -> int:
        return len(set(self._head_positions)) if unique else len(self._head_positions)

    def _update_around_head(self):
        self._around_head = [
            self._to_str(self._head_current["x"] - 1, self._head_current["y"] + 1),
            self._to_str(self._head_current["x"], self._head_current["y"] + 1),
            self._to_str(self._head_current["x"] + 1, self._head_current["y"] + 1),
            self._to_str(self._head_current["x"] - 1, self._head_current["y"]),
            self._to_str(self._head_current["x"] + 1, self._head_current["y"]),
            self._to_str(self._head_current["x"] - 1, self._head_current["y"] - 1),
            self._to_str(self._head_current["x"], self._head_current["y"] - 1),
            self._to_str(self._head_current["x"] + 1, self._head_current["y"] - 1),
        ]

    def _tail_allowed_spaces(self) -> List[str]:
        # * 2 *
        # 1 H 3
        # * 4 *
        return [
            self._to_str(self._head_current["x"] - 1, self._head_current["y"]),  # 1
            self._to_str(self._head_current["x"], self._head_current["y"] + 1),  # 2
            self._to_str(self._head_current["x"] + 1, self._head_current["y"]),  # 3
            self._to_str(self._head_current["x"], self._head_current["y"] - 1),  # 4
        ]

    def _update_around_tail(self):
        self._around_tail = [
            self._to_str(self._tail_current["x"] - 1, self._tail_current["y"] + 1),
            self._to_str(self._tail_current["x"], self._tail_current["y"] + 1),
            self._to_str(self._tail_current["x"] + 1, self._tail_current["y"] + 1),
            self._to_str(self._tail_current["x"] - 1, self._tail_current["y"]),
            self._to_str(self._tail_current["x"] + 1, self._tail_current["y"]),
            self._to_str(self._tail_current["x"] - 1, self._tail_current["y"] - 1),
            self._to_str(self._tail_current["x"], self._tail_current["y"] - 1),
            self._to_str(self._tail_current["x"] + 1, self._tail_current["y"] - 1),
        ]

    def _is_tail_under_head(self):
        if self._head_coords() == self._tail_coords():
            return True
        else:
            return False

    def _move_right(self):
        self._head_current["x"] += 1

    def _move_left(self):
        self._head_current["x"] -= 1

    def _move_up(self):
        self._head_current["y"] += 1

    def _move_down(self):
        self._head_current["y"] -= 1

    def _is_tail_near_head(self) -> bool:
        # print(f"Around head: {self._around_head}. Tail: {self._tail_coords()}")
        if self._tail_coords() in self._around_head:
            return True

        return False

    def _move_tail(self):
        for allowed_space in self._tail_allowed_spaces():
            if allowed_space in self._around_tail:
                x, y = self._to_pos(allowed_space)
                self._tail_current["x"] = x
                self._tail_current["y"] = y
                self._update_around_tail()
                self._update_tail_history()
                return
        raise (
            Exception(
                f"Rope tail could not find a space near head. head: {self._head_current} | tail: {self._tail_current}"
            )
        )

    def move_head(self, direction: str, steps: int) -> None:
        direction_func = {
            "L": self._move_left,
            "R": self._move_right,
            "U": self._move_up,
            "D": self._move_down,
        }
        for _ in range(0, steps):
            # move head
            direction_func[direction]()
            self._update_around_head()
            self._update_head_history()
            if not self._is_tail_under_head():
                # is tail touching or under
                if self._is_tail_near_head():
                    # print(
                    #     f"Tail near head. head: {self._head_coords()}, tail: {self._tail_coords()}"
                    # )
                    continue
                else:
                    self._move_tail()


def draw_graphs(rope: Rope):
    tail_history = rope.tail_history()
    head_history = rope.head_history()

    t_x = [pos[0] for pos in tail_history]
    t_y = [pos[1] for pos in tail_history]

    h_x = [pos[0] for pos in head_history]
    h_y = [pos[1] for pos in head_history]

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.1, bottom=0.35)

    tail = plt.scatter(t_x, t_y)
    tail.set_label("tail")
    head = plt.scatter(h_x, h_y, c="green")
    head.set_label("head")
    plt.legend("top left")

    axSlider1 = plt.axes([0.1, 0.2, 0.8, 0.05])
    slider1 = Slider(axSlider1, "Steps", valmin=0, valmax=len(t_x), valinit=len(t_x))

    def update(val):
        steps = int(slider1.val)
        # scatter(t_x[0:steps], t_y[0:steps])
        tail.axes.clear()
        head.axes.clear()
        tail.axes.scatter(t_x[0:steps], t_y[0:steps])
        head.axes.scatter(h_x[0:steps], h_y[0:steps], c="green", marker="x")
        plt.draw()

    slider1.on_changed(update)

    plt.show()


def main():
    rope = Rope()
    with open(input_file, "r") as input:
        for line in input:
            line = line.strip()
            instruction = line.split(" ")
            rope.move_head(instruction[0], int(instruction[1]))

    write_output(output_file1, rope.tail_history_count(unique=True))
    # draw_graphs(rope)


if __name__ == "__main__":
    main()
