from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.initial_position = (0, 260)
        self.goto(self.initial_position)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score}", align="center", font=("Arial", 24, "normal"))

    def increase_score(self):
        self.score += 10
        self.update_scoreboard()

    def reset_score(self):
        self.score = 0
        self.update_scoreboard()

    def show_game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=("Arial", 36, "normal"))

    def reset_position(self):
        self.clear()
        self.goto(self.initial_position)
        self.update_scoreboard()
