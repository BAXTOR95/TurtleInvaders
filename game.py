from spaceship import Spaceship
from alien import Alien
from barrier import Barrier
from scoreboard import Scoreboard
from projectile import Projectile
from sound_manager import SoundManager
from PIL import Image
from _tkinter import TclError
import time
import os
import sys
from config import (
    SCREEN_HEIGHT,
    ALIEN_ROWS,
    ALIEN_COLUMNS,
    BARRIER_POSITION,
    ALIEN_MOVE_INTERVAL,
    INITIAL_ALIEN_SPEED,
    INITIAL_PROJECTILE_SPEED,
)
import pygame


class Game:
    """
    The main game class that handles the overall game logic.

    Attributes:
        screen (Screen): The turtle screen where the game is displayed.
        sound_manager (SoundManager): The manager for game sounds.
        alien_speed (float): The initial speed of the aliens.
        projectile_speed (float): The initial speed of the projectiles.
        scoreboard (Scoreboard): The game scoreboard.
        last_alien_move_time (float): The last time the aliens moved.
        can_restart (bool): Flag to indicate if the game can be restarted.
    """

    def __init__(self, screen):
        """
        Initializes the game with the given screen.

        Args:
            screen (Screen): The turtle screen where the game is displayed.
        """
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
        self.can_restart = False

    def load_assets(self):
        """Loads all game assets including frames for animations."""
        self.spaceship_frames = self.extract_frames("assets/spaceship.gif", "spaceship")
        self.alien_frames = self.extract_frames("assets/alien.gif", "alien")
        self.projectile_frames = self.extract_frames(
            "assets/projectile.gif", "projectile"
        )
        self.barrier_frames = self.extract_frames("assets/barrier.gif", "barrier")
        self.background_frames = self.extract_frames(
            "assets/background.gif", "background"
        )

        for frame in (
            self.spaceship_frames
            + self.alien_frames
            + self.projectile_frames
            + self.barrier_frames
            + self.background_frames
        ):
            self.screen.register_shape(frame)

        self.screen.bgpic(self.background_frames[0])  # Set the initial background frame

    def extract_frames(self, gif_path, name_prefix):
        """
        Extracts frames from a GIF and saves them as separate images.

        Args:
            gif_path (str): The path to the GIF file.
            name_prefix (str): The prefix for the frame image filenames.

        Returns:
            list: A list of file paths to the extracted frames.
        """
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
        """Loads all game sounds."""
        self.sound_manager.load_sound("shoot", "assets/sounds/shoot.wav")
        self.sound_manager.load_sound("alien_hit", "assets/sounds/alien_hit.wav")
        self.sound_manager.load_sound("barrier_hit", "assets/sounds/barrier_hit.wav")
        self.sound_manager.load_sound("alien_shoot", "assets/sounds/alien_shoot.wav")
        self.sound_manager.load_sound("game_over", "assets/sounds/game_over.wav")
        self.sound_manager.load_sound(
            "background_music", "assets/sounds/background_music.wav", volume=0.3
        )

    def play_background_music(self):
        """Plays the background music for the game."""
        self.sound_manager.play_sound("background_music")

    def reset_game(self):
        """Resets the game state for a new game or level."""
        self.is_game_over = False
        self.is_level_complete = False
        self.scoreboard.reset_position()
        self.spaceship = Spaceship(
            self.spaceship_frames, self.projectile_frames, self.sound_manager
        )
        self.aliens = self.create_aliens()
        self.barriers = self.create_barriers()
        self.spaceship.projectiles = []
        self.alien_projectiles = []

        self.screen.listen()
        self.screen.onkey(self.spaceship.move_left, "Left")
        self.screen.onkey(self.spaceship.move_right, "Right")
        self.screen.onkey(self.spaceship.shoot, "space")
        self.screen.onkey(self.quit_game, "q")  # Add keypress for quitting the game

    def create_aliens(self):
        """
        Creates and positions the aliens on the screen.

        Returns:
            list: A list of Alien objects.
        """
        aliens = []
        for row in range(ALIEN_ROWS):
            for col in range(ALIEN_COLUMNS):
                alien = Alien(self.alien_speed, self.alien_frames)
                alien.goto(col * 50 - 250, row * 30 + 150)
                aliens.append(alien)
        return aliens

    def create_barriers(self):
        """
        Creates and positions the barriers on the screen.

        Returns:
            list: A list of Barrier objects.
        """
        return [Barrier(pos, self.barrier_frames) for pos in BARRIER_POSITION]

    def run(self):
        """Main game loop."""
        try:
            while not self.is_game_over and not self.is_level_complete:
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
                    self.is_level_complete = True
                    self.level_complete()
        except TclError:
            sys.exit(1)

    def move_aliens(self):
        """Moves all aliens on the screen."""
        for alien in self.aliens:
            alien.move()

    def move_projectiles(self):
        """Moves all projectiles on the screen and removes them if they go out of bounds."""
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
        """Checks for and handles collisions between projectiles, aliens, barriers, and the spaceship."""
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
        """Handles the shooting logic for the aliens."""
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
        """Handles the game over logic."""
        self.scoreboard.show_game_over()
        self.sound_manager.play_sound("game_over")
        self.can_restart = True
        self.screen.onkey(self.restart, "r")
        self.screen.listen()

    def level_complete(self):
        """Handles the logic for completing a level."""
        self.hide_objects()
        self.alien_speed *= 1.2
        self.projectile_speed *= 1.2
        self.scoreboard.save_high_score()
        self.reset_game()
        self.run()

    def restart(self):
        """Restarts the game if allowed."""
        if self.can_restart:
            self.hide_objects()
            self.scoreboard.reset_score()
            self.alien_speed = INITIAL_ALIEN_SPEED
            self.projectile_speed = INITIAL_PROJECTILE_SPEED
            self.reset_game()
            self.run()

    def quit_game(self):
        """Quits the game and saves the high score."""
        self.scoreboard.save_high_score()
        self.screen.bye()
        pygame.quit()

    def hide_objects(self):
        """Hides all objects on the screen."""
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
        """Updates the animations for all objects."""
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
        """Updates the background animation."""
        frame_index = int(time.time() * 10) % len(self.background_frames)
        self.screen.bgpic(self.background_frames[frame_index])
