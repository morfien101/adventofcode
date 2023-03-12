from typing import Union, List, Mapping, Dict
import base64
import re


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


output_file1 = "./output1.txt"
output_file2 = "./output2.txt"
input_file = "./test_input.txt"
# input_file = "./input.txt"


class robot:
    def __init__(self, type: str, cost: Dict[str, int]):
        self.type = type
        self.cost = cost

    def __str__(self) -> str:
        return f"type: {self.type}, cost: {self.cost}"


class Blueprint:
    def __init__(self, line: str):
        self.id, self.robots = self.digest_line(line)

    def digest_line(self, line: str) -> Union[int, Dict[str, robot]]:
        s1 = line.split(":")
        id = s1[0][-1]
        robots = s1[1].split(".")
        ore_robot_line = robots[0]
        clay_robot_line = robots[1]
        obsidian_robot_line = robots[2]
        geode_robot_line = robots[3]

        # ore_robot
        m = re.search(r"(\d+) ore$", ore_robot_line)
        ore_robot = robot("ore", {"ore": int(m.groups()[0])})

        # clay_robot
        m = re.search(r"(\d+) ore$", clay_robot_line)
        clay_robot = robot("clay", {"ore": int(m.groups()[0])})

        # obsidian_robot
        m = re.search(r"(\d+) ore and (\d+) clay$", obsidian_robot_line)
        obsidian_robot = robot(
            "obsidian", {"ore": int(m.groups()[0]), "clay": int(m.groups()[1])}
        )

        # geode_robot
        m = re.search(r"(\d+) ore and (\d+) obsidian$", geode_robot_line)
        geode_robot = robot(
            "geode", {"ore": int(m.groups()[1]), "obsidian": int(m.groups()[1])}
        )

        return id, {
            "ore": ore_robot,
            "clay": clay_robot,
            "obsidian": obsidian_robot,
            "geode": geode_robot,
        }

    def __str__(self) -> str:
        robots = {
            "ore": f"{self.robots['ore']}",
            "clay": f"{self.robots['clay']}",
            "obsidian": f"{self.robots['obsidian']}",
            "geode": f"{self.robots['geode']}",
        }
        return f"id: {self.id}, robots: {robots}"


def main():
    blueprints = []
    for line in open(input_file):
        blueprints.append(Blueprint(line))

    for blueprint in blueprints:
        print(blueprint)


if __name__ == "__main__":
    main()
