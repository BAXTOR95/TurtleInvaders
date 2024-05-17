from turtle import Turtle
import os


class Scoreboard(Turtle):
    """
    A class to represent the scoreboard in the game.

    Attributes:
        score (int): The current score of the player.
        high_score (int): The highest score achieved by the player.
        initial_position (tuple): The initial position of the scoreboard on the screen.

    Methods:
        update_scoreboard(): Updates the scoreboard display with the current score and high score.
        increase_score(): Increases the current score by a fixed amount.
        reset_score(): Resets the current score and updates the high score if needed.
        save_high_score(): Saves the high score to a file.
        load_high_score(): Loads the high score from a file.
        show_game_over(): Displays the game over message.
        reset_position(): Resets the scoreboard to its initial position.
    """

    def __init__(self):
        """
        Initializes the scoreboard with default values and loads the high score.
        """
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
        """
        Updates the scoreboard display with the current score and high score.
        """
        self.clear()
        self.write(
            f"Score: {self.score}  High Score: {self.high_score}",
            align="center",
            font=("Arial", 24, "normal"),
        )

    def increase_score(self):
        """
        Increases the current score by a fixed amount and updates the scoreboard.
        """
        self.score += 10
        self.update_scoreboard()

    def reset_score(self):
        """
        Resets the current score and updates the high score if the current score is higher.
        """
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.score = 0
        self.update_scoreboard()

    def save_high_score(self):
        """
        Saves the high score to a file if the current score is higher.
        """
        if self.score > self.high_score:
            self.high_score = self.score
            with open("high_score.txt", "w") as file:
                file.write(str(self.high_score))

    def load_high_score(self):
        """
        Loads the high score from a file.

        Returns:
            int: The high score loaded from the file, or 0 if the file does not exist.
        """
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as file:
                return int(file.read())
        return 0

    def show_game_over(self):
        """
        Displays the game over message on the screen.
        """
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=("Arial", 36, "normal"))
        self.goto(0, -40)
        self.write(
            "Press 'R' to Restart or 'Q' to Quit",
            align="center",
            font=("Arial", 24, "normal"),
        )

    def reset_position(self):
        """
        Resets the scoreboard to its initial position and updates the display.
        """
        self.clear()
        self.goto(self.initial_position)
        self.update_scoreboard()
