from turtle import Turtle
import os


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = self.load_high_score()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.initial_position = (0, 260)
        self.goto(self.initial_position)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(
            f"Score: {self.score}  High Score: {self.high_score}",
            align="center",
            font=("Arial", 24, "normal"),
        )

    def increase_score(self):
        self.score += 10
        self.update_scoreboard()

    def reset_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.score = 0
        self.update_scoreboard()

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def load_high_score(self):
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as file:
                return int(file.read())
        return 0

    def show_game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=("Arial", 36, "normal"))
        self.goto(0, -40)
        self.write(
            "Press 'R' to Restart or 'Q' to Quit",
            align="center",
            font=("Arial", 24, "normal"),
        )

    def reset_position(self):
        self.clear()
        self.goto(self.initial_position)
        self.update_scoreboard()
