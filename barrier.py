from turtle import Turtle


class Barrier(Turtle):
    """
    A class to represent a barrier in the game.

    Attributes:
        frames (list): List of image frames for barrier animation.
        frame_index (int): Current index of the frame being displayed.

    Methods:
        update_animation(): Updates the barrier's animation frame.
    """

    def __init__(self, position, frames=[]):
        """
        Initializes the barrier with its position and animation frames.

        Args:
            position (tuple): The (x, y) position of the barrier.
            frames (list): List of image frames for barrier animation.
        """
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.shape(
            self.frames[self.frame_index] if self.frames else "assets/barrier.gif"
        )
        self.penup()
        self.goto(position)

    def update_animation(self):
        """
        Updates the barrier's animation frame.
        """
        if self.frames:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.shape(self.frames[self.frame_index])
