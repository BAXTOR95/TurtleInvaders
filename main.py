from turtle import Screen
from game import Game


def main():
    screen = Screen()
    screen.setup(width=800, height=600)
    screen.bgcolor("black")
    screen.title("Turtle Invaders")
    screen.tracer(0)

    game = Game(screen)

    screen.listen()
    screen.onkey(game.spaceship.move_left, "Left")
    screen.onkey(game.spaceship.move_right, "Right")
    screen.onkey(game.spaceship.shoot, "space")

    game.run()

    screen.mainloop()


if __name__ == "__main__":
    main()
