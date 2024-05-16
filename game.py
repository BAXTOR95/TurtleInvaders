from turtle import Screen
from spaceship import Spaceship
from alien import Alien
from barrier import Barrier
from scoreboard import Scoreboard
from projectile import Projectile
import time
from config import (
    SCREEN_HEIGHT,
    ALIEN_ROWS,
    ALIEN_COLUMNS,
    BARRIER_POSITION,
    ALIEN_MOVE_INTERVAL,
    INITIAL_ALIEN_SPEED,
    INITIAL_PROJECTILE_SPEED,
)


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.alien_speed = INITIAL_ALIEN_SPEED
        self.projectile_speed = INITIAL_PROJECTILE_SPEED
        self.scoreboard = Scoreboard()  # Initialize scoreboard once
        self.last_alien_move_time = time.time()
        self.reset_game()

    def reset_game(self):
        self.is_game_over = False
        self.scoreboard.reset_position()
        self.spaceship = Spaceship()
        self.aliens = self.create_aliens()
        self.barriers = self.create_barriers()
        self.spaceship.projectiles = []
        self.alien_projectiles = []
        self.scoreboard.reset_score()  # Reset the score

        self.screen.listen()
        self.screen.onkey(self.spaceship.move_left, "Left")
        self.screen.onkey(self.spaceship.move_right, "Right")
        self.screen.onkey(self.spaceship.shoot, "space")

    def create_aliens(self):
        aliens = []
        for row in range(ALIEN_ROWS):
            for col in range(ALIEN_COLUMNS):
                alien = Alien(self.alien_speed)
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
            current_time = time.time()
            if current_time - self.last_alien_move_time >= ALIEN_MOVE_INTERVAL:
                self.move_aliens()
                self.last_alien_move_time = current_time
            self.move_projectiles()
            self.check_collisions()
            self.alien_shoot()
            if not self.aliens:
                self.is_game_over = True
                self.game_over()

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
        self.scoreboard.show_game_over()
        self.screen.onkey(self.restart, "r")
        self.screen.listen()

    def restart(self):
        self.hide_objects()
        self.alien_speed *= 1.2
        self.projectile_speed *= 1.2
        self.reset_game()
        self.run()

    def hide_objects(self):
        self.spaceship.hideturtle()
        for alien in self.aliens:
            alien.hideturtle()
        for barrier in self.barriers:
            barrier.hideturtle()
        for projectile in self.spaceship.projectiles:
            projectile.hideturtle()
        for projectile in self.alien_projectiles:
            projectile.hideturtle()
        self.spaceship.projectiles.clear()
        self.alien_projectiles.clear()
