input_file = "./input.txt"
output_file = "./output2.txt"


def write_output(value):
    global output_file
    print(f"{value}")
    with open(output_file, "w") as output:
        output.write(f"{value}")


def shape_selector(outcome: str, shape: str) -> str:
    if outcome == "draw":
        return shape

    elif outcome == "win":
        if shape == "rock":
            return "paper"
        elif shape == "paper":
            return "scissors"
        elif shape == "scissors":
            return "rock"

    else:
        if shape == "rock":
            return "scissors"
        elif shape == "paper":
            return "rock"
        elif shape == "scissors":
            return "paper"


with open(input_file, "r") as input:
    games = [list(line.strip()) for line in input]


shapes = {"A": "rock", "B": "paper", "C": "scissors"}

outcome = {"X": "loose", "Y": "draw", "Z": "win"}

points = {"rock": 1, "paper": 2, "scissors": 3, "win": 6, "draw": 3, "loose": 0}

total_points = 0

for game in games:
    opponent = game[0]
    me = game[2]

    my_shape = shape_selector(outcome[me], shapes[opponent])

    if shapes[opponent] == my_shape:
        total_points += points["draw"] + points[my_shape]

    elif shapes[opponent] == "rock" and my_shape == "paper":
        total_points += points["win"] + points[my_shape]

    elif shapes[opponent] == "rock" and my_shape == "scissors":
        total_points += points["loose"] + points[my_shape]

    elif shapes[opponent] == "scissors" and my_shape == "paper":
        total_points += points["loose"] + points[my_shape]

    elif shapes[opponent] == "scissors" and my_shape == "rock":
        total_points += points["win"] + points[my_shape]

    elif shapes[opponent] == "paper" and my_shape == "rock":
        total_points += points["loose"] + points[my_shape]

    elif shapes[opponent] == "paper" and my_shape == "scissors":
        total_points += points["win"] + points[my_shape]


write_output(total_points)
