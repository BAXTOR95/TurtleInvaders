import pygame


class SoundManager:
    """
    A class that manages sound effects for a game.

    Attributes:
    - sounds (dict): A dictionary that stores the loaded sound effects.

    Methods:
    - __init__(): Initializes the SoundManager object.
    - load_sound(name, sound_path, volume=0.5): Loads a sound file and stores it in the sound manager.
    - play_sound(name): Plays the sound with the given name.
    """

    def __init__(self):
        """
        Initializes the SoundManager object.

        This method initializes the SoundManager object by initializing the mixer module
        with the specified frequency, size, channels, and buffer. It also initializes
        an empty dictionary to store the sounds.

        Parameters:
            None

        Returns:
            None
        """
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.sounds = {}

    def load_sound(self, name, sound_path, volume=0.5):
        """
        Load a sound file and store it in the sound manager.

        Parameters:
        - name (str): The name to associate with the loaded sound.
        - sound_path (str): The path to the sound file.
        - volume (float, optional): The volume level of the sound (default is 0.5).

        Returns:
        None
        """
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(volume)
        self.sounds[name] = sound

    def play_sound(self, name):
        """
        Plays the sound with the given name.

        Parameters:
        - name (str): The name of the sound to be played.

        Returns:
        None
        """
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"Sound '{name}' not loaded.")
