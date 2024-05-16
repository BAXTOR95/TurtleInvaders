from spaceship import Spaceship
from alien import Alien
from barrier import Barrier
from scoreboard import Scoreboard
from projectile import Projectile
from sound_manager import SoundManager
from PIL import Image
import time
import os
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
        self.sound_manager = SoundManager()
        self.alien_speed = INITIAL_ALIEN_SPEED
        self.projectile_speed = INITIAL_PROJECTILE_SPEED
        self.scoreboard = Scoreboard()  # Initialize scoreboard once
        self.last_alien_move_time = time.time()
        self.load_assets()
        self.reset_game()
        self.load_sounds()
        self.play_background_music()

    def load_assets(self):
        self.spaceship_frames = self.extract_frames("assets/spaceship.gif", "spaceship")
        self.alien_frames = self.extract_frames("assets/alien.gif", "alien")
        self.projectile_frames = self.extract_frames(
            "assets/projectile.gif", "projectile"
        )
        self.barrier_frames = self.extract_frames("assets/barrier.gif", "barrier")
        self.background_frames = self.extract_frames(
            "assets/background.gif", "background"
        )

        for frame in self.spaceship_frames:
            self.screen.register_shape(frame)
        for frame in self.alien_frames:
            self.screen.register_shape(frame)
        for frame in self.projectile_frames:
            self.screen.register_shape(frame)
        for frame in self.barrier_frames:
            self.screen.register_shape(frame)
        for frame in self.background_frames:
            self.screen.register_shape(frame)

        # Set the initial background frame
        self.screen.bgpic(self.background_frames[0])

    def extract_frames(self, gif_path, name_prefix):
        frames_dir = os.path.join("assets", "frames")
        os.makedirs(frames_dir, exist_ok=True)
        frames = []
        with Image.open(gif_path) as img:
            for frame in range(img.n_frames):
                img.seek(frame)
                frame_image = img.copy().convert("RGBA")
                frame_path = os.path.join(
                    frames_dir, f"{name_prefix}_frame_{frame}.gif"
                )
                frame_image.save(frame_path)
                frames.append(frame_path)
        return frames

    def load_sounds(self):
        self.sound_manager.load_sound("shoot", "assets/sounds/shoot.wav")
        self.sound_manager.load_sound("alien_hit", "assets/sounds/alien_hit.wav")
        self.sound_manager.load_sound("barrier_hit", "assets/sounds/barrier_hit.wav")
        self.sound_manager.load_sound("alien_shoot", "assets/sounds/alien_shoot.wav")
        self.sound_manager.load_sound("game_over", "assets/sounds/game_over.wav")
        self.sound_manager.load_sound(
            "background_music", "assets/sounds/background_music.wav", volume=0.3
        )

    def play_background_music(self):
        self.sound_manager.play_sound("background_music")

    def reset_game(self):
        self.is_game_over = False
        self.scoreboard.reset_position()
        self.spaceship = Spaceship(
            self.spaceship_frames, self.projectile_frames, self.sound_manager
        )
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
                alien = Alien(self.alien_speed, self.alien_frames)
                alien.goto(col * 50 - 250, row * 30 + 150)
                aliens.append(alien)
        return aliens

    def create_barriers(self):
        barriers = [Barrier(pos, self.barrier_frames) for pos in BARRIER_POSITION]
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
            self.update_animations()
            self.update_background()
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
                    self.sound_manager.play_sound("alien_hit")
                    break

            for barrier in self.barriers:
                if projectile.distance(barrier) < 20:
                    projectile.hideturtle()
                    self.spaceship.projectiles.remove(projectile)
                    self.sound_manager.play_sound("barrier_hit")
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
                    self.sound_manager.play_sound("barrier_hit")
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
            projectile = Projectile(
                shooter.xcor(),
                shooter.ycor(),
                direction=-1,
                frames=self.projectile_frames,
            )
            self.alien_projectiles.append(projectile)
            self.sound_manager.play_sound("alien_shoot")

    def game_over(self):
        self.scoreboard.show_game_over()
        self.sound_manager.play_sound("game_over")
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

    def update_animations(self):
        self.spaceship.update_animation()
        for alien in self.aliens:
            alien.update_animation()
        for projectile in self.spaceship.projectiles:
            projectile.update_animation()
        for projectile in self.alien_projectiles:
            projectile.update_animation()
        for barrier in self.barriers:
            barrier.update_animation()

    def update_background(self):
        frame_index = int(time.time() * 10) % len(self.background_frames)
        self.screen.bgpic(self.background_frames[frame_index])
