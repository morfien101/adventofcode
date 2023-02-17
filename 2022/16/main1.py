from typing import List, Mapping, Union
import base64
import re
import networkx as nx

# p1: wrong 4294

# input_file = "./input.txt"
input_file = "./test_input.txt"
output_file1 = "./output1.txt"
output_file2 = "./output2.txt"


def convert_input(file: str):
    lines = []
    with open(file, "r") as input:
        for line in input:
            line.strip()
            lines.append(line)
    return lines


def write_output(file: str, value: str):
    print(f"{value}")
    with open(file, "wb") as output:
        out = base64.b64encode(f"{value}".encode("utf8"))
        output.write(out)


def digest_input(line: str) -> map:
    regex_matcher = r"Valve (?P<room>[A-Z]{2}).*rate=(?P<rate>[0-9]+);.*valves? (?P<connections>.*)$"
    matches = re.findall(regex_matcher, line)
    return {
        "room": matches[0][0],
        "rate": int(matches[0][1]),
        "connections": matches[0][2].split(", "),
    }


def walk(
    caves: nx.DiGraph,
    time_left: int,
    current_room: str,
    valves_left: List[str],
    valve_running_time: Mapping[str, int],
    travel_path: List[str],
    paths: Mapping[str, int],
) -> Union[List[str], int]:
    # What rooms can I get to within the time left.
    print(f"valve_running_time: {valve_running_time}")
    for next_valve in valves_left:
        travel_time = nx.shortest_path_length(caves, current_room, next_valve)
        # travel time  + 1 min opening + at least 1 min release.
        if travel_time + 2 <= time_left:
            run_time = time_left - (travel_time + 1)
            # print(f"run_time: {run_time} on {next_valve}")
            valve_running_time[next_valve] = run_time
            my_path = travel_path.copy()
            my_path.append(next_valve)
            walk(
                caves,
                run_time,
                next_valve,
                [x for x in valves_left if x != next_valve],
                valve_running_time.copy(),
                my_path,
                paths,
            )
            continue
        else:
            print(f"time_left: {time_left}")
            break

    pressure = 0
    path = []
    travel_path_str = ",".join(travel_path)
    if travel_path_str == "BB":
        print(valve_running_time)
    for valve in valve_running_time.keys():
        pressure += caves.nodes[valve]["rate"] * valve_running_time[valve]
        path.append(valve)
    paths[travel_path_str] = pressure


def part1(caves: nx.DiGraph, valves: List[str]):
    possible_options = {}
    walk(caves, 30, "AA", valves.copy(), {}, [], possible_options)

    current_highest = ["AA", 0]
    for path in possible_options.keys():
        if current_highest[1] < possible_options[path]:
            current_highest = [path, possible_options[path]]
            print(f"New High: {current_highest}")


def main():
    valves = []
    caves = nx.DiGraph()
    for line in convert_input(input_file):
        ld = digest_input(line)

        if ld["rate"] > 0:
            valves.append(ld["room"])

        caves.add_node(ld["room"], rate=ld["rate"])
        for connection in ld["connections"]:
            caves.add_edge(ld["room"], connection)

    part1(caves, valves.copy())


if __name__ == "__main__":
    main()
