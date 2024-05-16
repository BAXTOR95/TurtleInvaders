from turtle import Turtle
from projectile import Projectile
from config import SCREEN_WIDTH, SHIP_SPEED


class Spaceship(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("triangle")
        self.color("white")
        self.penup()
        self.goto(0, -250)
        self.setheading(90)
        self.projectiles = []

    def move_left(self):
        new_x = self.xcor() - SHIP_SPEED
        if new_x > -SCREEN_WIDTH / 2:
            self.goto(new_x, self.ycor())

    def move_right(self):
        new_x = self.xcor() + SHIP_SPEED
        if new_x < SCREEN_WIDTH / 2:
            self.goto(new_x, self.ycor())

    def shoot(self):
        projectile = Projectile(self.xcor(), self.ycor())
        self.projectiles.append(projectile)
