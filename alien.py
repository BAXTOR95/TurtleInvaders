from turtle import Turtle


class Alien(Turtle):
    """
    A class to represent an alien in the game.

    Attributes:
        frames (list): List of image frames for alien animation.
        frame_index (int): Current index of the frame being displayed.
        direction (int): Current direction of movement (1 for right, -1 for left).
        speed (float): Speed of the alien's movement.

    Methods:
        move(): Moves the alien and changes direction at screen edges.
        update_animation(): Updates the alien's animation frame.
    """

    def __init__(self, speed, frames):
        """
        Initializes the alien with its animation frames and movement speed.

        Args:
            speed (float): Speed of the alien's movement.
            frames (list): List of image frames for alien animation.
        """
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.shape(self.frames[self.frame_index])
        self.penup()
        self.direction = 1  # 1 for right, -1 for left
        self.speed = speed

    def move(self):
        """
        Moves the alien in the current direction and changes direction at screen edges.
        """
        new_x = self.xcor() + self.direction * self.speed
        self.goto(new_x, self.ycor())
        if self.xcor() > 350 or self.xcor() < -350:
            self.direction *= -1
            self.goto(self.xcor(), self.ycor() - 40)

    def update_animation(self):
        """
        Updates the alien's animation frame.
        """
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.shape(self.frames[self.frame_index])
