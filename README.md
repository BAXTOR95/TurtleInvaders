# Turtle Invaders

Turtle Invaders is a classic shoot 'em up game inspired by Space Invaders, implemented using Python and the Turtle graphics library. The player controls a spaceship that can move left and right and shoot projectiles to destroy alien ships. The aliens move closer to the ship every second, and the game ends if they reach the ship.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Control a spaceship using the arrow keys
- Shoot projectiles using the space bar
- Destroy alien ships and avoid their projectiles
- Animated spaceship, aliens, and projectiles
- Barriers that offer defensive positions
- Score tracking and high score saving
- Background music and sound effects

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/BAXTOR95/TurtleInvaders.git
   cd TurtleInvaders
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Ensure you have the `pygame` and `Pillow` libraries installed:

   ```bash
   pip install pygame Pillow
   ```

## Usage

1. Run the game:

   ```bash
   python main.py
   ```

2. Use the arrow keys to move the spaceship left and right.
3. Press the space bar to shoot projectiles at the alien ships.
4. Press 'R' to restart the game after a game over.
5. Press 'Q' to quit the game.

## Project Structure

```arduino
TurtleInvaders/
├── assets/
│   ├── spaceship.gif
│   ├── alien.gif
│   ├── projectile.gif
│   ├── barrier.gif
│   ├── background.gif
│   ├── sounds/
│   │   ├── shoot.wav
│   │   ├── alien_hit.wav
│   │   ├── barrier_hit.wav
│   │   ├── alien_shoot.wav
│   │   ├── game_over.wav
│   │   └── background_music.wav
│   └── frames/  # Extracted frames for animations
├── spaceship.py
├── alien.py
├── barrier.py
├── projectile.py
├── scoreboard.py
├── sound_manager.py
├── config.py
├── game.py
├── main.py
├── high_score.txt
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
