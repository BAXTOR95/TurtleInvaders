import turtle
from PIL import Image, ImageTk


def extract_frames(gif_path):
    frames = []
    with Image.open(gif_path) as img:
        for frame in range(0, img.n_frames):
            img.seek(frame)
            frame_image = img.copy().convert("RGBA")
            frames.append(frame_image)
    return frames


gif_path = "assets/background.gif"
frames = extract_frames(gif_path)

# Setup turtle screen
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.bgcolor("white")

# Create a turtle
gif_turtle = turtle.Turtle()
gif_turtle.hideturtle()


# Function to display frames
def display_frame(frame):
    screen_image = ImageTk.PhotoImage(frame)
    screen.addshape("frame_image", turtle.Shape("image", screen_image))
    gif_turtle.shape("frame_image")
    gif_turtle.showturtle()


# Animation loop
frame_delay = 100  # milliseconds between frames
frame_index = 0


def animate():
    global frame_index
    display_frame(frames[frame_index])
    frame_index = (frame_index + 1) % len(frames)
    screen.ontimer(animate, frame_delay)


# Start animation
animate()
screen.mainloop()
