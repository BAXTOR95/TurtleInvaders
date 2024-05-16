from turtle import Turtle
from projectile import Projectile
from config import SCREEN_WIDTH, SHIP_SPEED, SHOOT_DELAY
import time


class Spaceship(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("triangle")
        self.color("white")
        self.penup()
        self.goto(0, -250)
        self.setheading(90)
        self.projectiles = []
        self.last_shot_time = 0

    def move_left(self):
        new_x = self.xcor() - SHIP_SPEED
        if new_x > -SCREEN_WIDTH / 2:
            self.goto(new_x, self.ycor())

    def move_right(self):
        new_x = self.xcor() + SHIP_SPEED
        if new_x < SCREEN_WIDTH / 2:
            self.goto(new_x, self.ycor())

    def shoot(self):
        current_time = time.time()
        if current_time - self.last_shot_time >= SHOOT_DELAY:
            projectile = Projectile(self.xcor(), self.ycor())
            self.projectiles.append(projectile)
            self.last_shot_time = current_time
