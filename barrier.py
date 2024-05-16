from turtle import Turtle


class Barrier(Turtle):
    def __init__(self, position, frames=[]):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.shape(
            self.frames[self.frame_index] if self.frames else "assets/barrier.gif"
        )
        self.penup()
        self.goto(position)

    def update_animation(self):
        if self.frames:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.shape(self.frames[self.frame_index])
