from turtle import Turtle
from config import PROJECTILE_SPEED


class Projectile(Turtle):
    """
    A class to represent a projectile in the game.

    Attributes:
        frames (list): List of image frames for projectile animation.
        frame_index (int): Current index of the frame being displayed.
        direction (int): Direction of the projectile's movement (1 for up, -1 for down).

    Methods:
        move(): Moves the projectile in the current direction.
        update_animation(): Updates the projectile's animation frame.
    """

    def __init__(self, x, y, direction=1, frames=[]):
        """
        Initializes the projectile with its initial position, direction, and animation frames.

        Args:
            x (float): Initial x-coordinate of the projectile.
            y (float): Initial y-coordinate of the projectile.
            direction (int): Direction of the projectile's movement (1 for up, -1 for down).
            frames (list): List of image frames for projectile animation.
        """
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.shape(
            self.frames[self.frame_index] if self.frames else "assets/projectile.gif"
        )
        self.penup()
        self.goto(x, y)
        self.setheading(90 if direction == 1 else 270)
        self.direction = direction

    def move(self):
        """
        Moves the projectile forward in the current direction.
        """
        self.forward(PROJECTILE_SPEED)

    def update_animation(self):
        """
        Updates the projectile's animation frame.
        """
        if self.frames:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.shape(self.frames[self.frame_index])
