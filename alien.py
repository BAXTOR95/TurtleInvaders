from turtle import Turtle


class Alien(Turtle):
    def __init__(self, speed, frames):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.shape(self.frames[self.frame_index])
        self.penup()
        self.direction = 1  # 1 for right, -1 for left
        self.speed = speed

    def move(self):
        new_x = self.xcor() + self.direction * self.speed
        self.goto(new_x, self.ycor())
        if self.xcor() > 350 or self.xcor() < -350:
            self.direction *= -1
            self.goto(self.xcor(), self.ycor() - 40)

    def update_animation(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.shape(self.frames[self.frame_index])
