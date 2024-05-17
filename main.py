from turtle import Screen
from game import Game


def main():
    """
    The main function to initialize and start the Turtle Invaders game.
    """
    # Set up the screen
    screen = Screen()
    screen.setup(width=800, height=600)
    screen.bgcolor("black")
    screen.title("Turtle Invaders")
    screen.tracer(0)

    # Create the game instance
    game = Game(screen)

    # Set up key bindings
    screen.listen()
    screen.onkey(game.spaceship.move_left, "Left")
    screen.onkey(game.spaceship.move_right, "Right")
    screen.onkey(game.spaceship.shoot, "space")

    # Run the game
    game.run()

    # Keep the window open
    screen.mainloop()


if __name__ == "__main__":
    main()
