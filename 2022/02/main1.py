input_file = "./input.txt"
output_file = "./output1.txt"


def write_output(value):
    global output_file
    print(f"{value}")
    with open(output_file, "w") as output:
        output.write(f"{value}")


with open(input_file, "r") as input:
    games = [list(line.strip()) for line in input]


shapes = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}

points = {"rock": 1, "paper": 2, "scissors": 3, "win": 6, "draw": 3, "loose": 0}

total_points = 0

for game in games:
    opponent = game[0]
    me = game[2]

    if shapes[opponent] == shapes[me]:
        total_points += points["draw"] + points[shapes[me]]

    elif shapes[opponent] == "rock" and shapes[me] == "paper":
        total_points += points["win"] + points[shapes[me]]

    elif shapes[opponent] == "rock" and shapes[me] == "scissors":
        total_points += points["loose"] + points[shapes[me]]

    elif shapes[opponent] == "scissors" and shapes[me] == "paper":
        total_points += points["loose"] + points[shapes[me]]

    elif shapes[opponent] == "scissors" and shapes[me] == "rock":
        total_points += points["win"] + points[shapes[me]]

    elif shapes[opponent] == "paper" and shapes[me] == "rock":
        total_points += points["loose"] + points[shapes[me]]

    elif shapes[opponent] == "paper" and shapes[me] == "scissors":
        total_points += points["win"] + points[shapes[me]]


write_output(total_points)
