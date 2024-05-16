from turtle import Screen
from spaceship import Spaceship
from alien import Alien
from barrier import Barrier
from scoreboard import Scoreboard
from projectile import Projectile
import time
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ALIEN_ROWS,
    ALIEN_COLUMNS,
    BARRIER_POSITION,
    ALIEN_MOVE_INTERVAL,
)


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.spaceship = Spaceship()
        self.aliens = self.create_aliens()
        self.barriers = self.create_barriers()
        self.projectiles = []
        self.alien_projectiles = []
        self.scoreboard = Scoreboard()
        self.is_game_over = False

    def create_aliens(self):
        aliens = []
        for row in range(ALIEN_ROWS):
            for col in range(ALIEN_COLUMNS):
                alien = Alien()
                alien.goto(col * 50 - 250, row * 30 + 150)
                aliens.append(alien)
        return aliens

    def create_barriers(self):
        barriers = [Barrier(pos) for pos in BARRIER_POSITION]
        return barriers

    def run(self):
        while not self.is_game_over:
            self.screen.update()
            time.sleep(0.02)  # Update the screen every 20ms
            self.move_aliens()
            self.move_projectiles()
            self.check_collisions()
            self.alien_shoot()

    def move_aliens(self):
        for alien in self.aliens:
            alien.move()

    def move_projectiles(self):
        for projectile in self.spaceship.projectiles:
            projectile.move()
            if projectile.ycor() > SCREEN_HEIGHT / 2:
                projectile.hideturtle()
                self.spaceship.projectiles.remove(projectile)

        for projectile in self.alien_projectiles:
            projectile.move()
            if projectile.ycor() < -SCREEN_HEIGHT / 2:
                projectile.hideturtle()
                self.alien_projectiles.remove(projectile)

    def check_collisions(self):
        for projectile in self.spaceship.projectiles:
            for alien in self.aliens:
                if projectile.distance(alien) < 20:
                    alien.hideturtle()
                    self.aliens.remove(alien)
                    projectile.hideturtle()
                    self.spaceship.projectiles.remove(projectile)
                    self.scoreboard.increase_score()
                    break

            for barrier in self.barriers:
                if projectile.distance(barrier) < 20:
                    projectile.hideturtle()
                    self.spaceship.projectiles.remove(projectile)
                    break

        for projectile in self.alien_projectiles:
            if projectile.distance(self.spaceship) < 20:
                self.is_game_over = True
                self.game_over()
                return

            for barrier in self.barriers:
                if projectile.distance(barrier) < 20:
                    projectile.hideturtle()
                    self.alien_projectiles.remove(projectile)
                    break

            for player_projectile in self.spaceship.projectiles:
                if projectile.distance(player_projectile) < 20:
                    projectile.hideturtle()
                    self.alien_projectiles.remove(projectile)
                    player_projectile.hideturtle()
                    self.spaceship.projectiles.remove(player_projectile)
                    break

        for alien in self.aliens:
            if alien.ycor() <= self.spaceship.ycor() + 20:
                self.is_game_over = True
                self.game_over()

    def alien_shoot(self):
        from random import choice, randint

        if (
            self.aliens and randint(1, 100) <= 5
        ):  # 5% chance per frame for any alien to shoot
            shooter = choice(self.aliens)
            projectile = Projectile(shooter.xcor(), shooter.ycor(), direction=-1)
            self.alien_projectiles.append(projectile)

    def game_over(self):
        self.scoreboard.goto(0, 0)
        self.scoreboard.write("GAME OVER", align="center", font=("Arial", 36, "normal"))
