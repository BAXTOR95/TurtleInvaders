from turtle import Turtle
from projectile import Projectile
from config import SCREEN_WIDTH, SHIP_SPEED, SHOOT_DELAY
import time


class Spaceship(Turtle):
    def __init__(self, frames, projectile_frames, sound_manager):
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
            projectile = Projectile(
                self.xcor(), self.ycor(), frames=self.projectile_frames
            )
            self.projectiles.append(projectile)
            self.sound_manager.play_sound("shoot")
            self.last_shot_time = current_time

    def update_animation(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.shape(self.frames[self.frame_index])
