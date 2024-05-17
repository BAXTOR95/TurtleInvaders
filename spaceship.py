from turtle import Turtle
from projectile import Projectile
from config import SCREEN_WIDTH, SHIP_SPEED, SHOOT_DELAY
import time


class Spaceship(Turtle):
    """
    A class to represent the player's spaceship.

    Attributes:
        frames (list): List of image frames for spaceship animation.
        projectile_frames (list): List of image frames for projectile animation.
        sound_manager (SoundManager): Manages the game's sound effects.
        frame_index (int): Current index of the frame being displayed.
        projectiles (list): List of active projectiles shot by the spaceship.
        last_shot_time (float): Time when the last projectile was shot.

    Methods:
        move_left(): Moves the spaceship to the left.
        move_right(): Moves the spaceship to the right.
        shoot(): Shoots a projectile if the shoot delay has passed.
        update_animation(): Updates the spaceship's animation frame.
    """

    def __init__(self, frames, projectile_frames, sound_manager):
        """
        Initializes the spaceship with its animation frames, projectile frames, and sound manager.

        Args:
            frames (list): List of image frames for spaceship animation.
            projectile_frames (list): List of image frames for projectile animation.
            sound_manager (SoundManager): Manages the game's sound effects.
        """
        super().__init__()
        self.frames = frames
        self.projectile_frames = projectile_frames
        self.sound_manager = sound_manager
        self.frame_index = 0
        self.shape(self.frames[self.frame_index])
        self.penup()
        self.goto(0, -250)
        self.setheading(90)
        self.projectiles = []
        self.last_shot_time = 0

    def move_left(self):
        """
        Moves the spaceship to the left if it is within the screen bounds.
        """
        new_x = self.xcor() - SHIP_SPEED
        if new_x > -SCREEN_WIDTH / 2:
            self.goto(new_x, self.ycor())

    def move_right(self):
        """
        Moves the spaceship to the right if it is within the screen bounds.
        """
        new_x = self.xcor() + SHIP_SPEED
        if new_x < SCREEN_WIDTH / 2:
            self.goto(new_x, self.ycor())

    def shoot(self):
        """
        Shoots a projectile if the delay since the last shot has passed.
        """
        current_time = time.time()
        if current_time - self.last_shot_time >= SHOOT_DELAY:
            projectile = Projectile(
                self.xcor(), self.ycor(), frames=self.projectile_frames
            )
            self.projectiles.append(projectile)
            self.sound_manager.play_sound("shoot")
            self.last_shot_time = current_time

    def update_animation(self):
        """
        Updates the spaceship's animation frame.
        """
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.shape(self.frames[self.frame_index])
