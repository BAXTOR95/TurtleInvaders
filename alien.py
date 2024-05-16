from turtle import Turtle
from config import ALIEN_SPEED


class Alien(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("green")
        self.penup()
        self.direction = 1  # 1 for right, -1 for left

    def move(self):
        new_x = self.xcor() + self.direction * ALIEN_SPEED
        self.goto(new_x, self.ycor())
        if self.xcor() > 350 or self.xcor() < -350:
            self.direction *= -1
            self.goto(self.xcor(), self.ycor() - 40)
