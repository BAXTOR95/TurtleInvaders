from turtle import Turtle


class Barrier(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("blue")
        self.penup()
        self.goto(position)
