from turtle import Turtle
from config import PROJECTILE_SPEED


class Projectile(Turtle):
    def __init__(self, x, y, direction=1):
        super().__init__()
        self.shape("circle")
        self.color("red" if direction == 1 else "yellow")
        self.penup()
        self.goto(x, y)
        self.setheading(90 if direction == 1 else 270)
        self.direction = direction

    def move(self):
        self.forward(PROJECTILE_SPEED)
