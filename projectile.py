from turtle import Turtle
from config import PROJECTILE_SPEED


class Projectile(Turtle):
    def __init__(self, x, y, direction=1, frames=[]):
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
        self.forward(PROJECTILE_SPEED)

    def update_animation(self):
        if self.frames:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.shape(self.frames[self.frame_index])
