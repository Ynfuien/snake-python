from tkinter import *
import random
import math
from enum import Enum



# Configuration variables
GRID_SIZE = 32
SCALE = 20
SIZE = GRID_SIZE * SCALE + GRID_SIZE - 1
SNAKE_SIZE = 5
TICK_TIME = 100


# Colors
class Colors(str, Enum):
    Background = "#242424"
    SnakeHead = "#FFD43B"
    SnakeBody = "#5A9FD4"
    Berry = "#FF5555"
    Border = "#555555"
    GameOver = "#FF5555"
    Score = "#FFFF55"
    ScoreNumber = "#FFAA00"


# Game variables
border = None
snake = None
berry = None
direction = None
newDirection = None
gameOver = False



# Create window
window = Tk()
window.title("Python")
window.resizable(False, False)

# Create canvas
canvas = Canvas(window, bg=Colors.Background, height=SIZE, width=SIZE, highlightthickness=0)
canvas.pack()
window.update()

# Center the window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

lx = int(screen_width / 2 - window_width / 2)
ly = int(screen_height / 2 - window_height / 2)

window.geometry(f"{window_width}x{window_height}+{lx}+{ly}")

# Bind key press events
window.bind('<Left>', lambda event: keypress('left'))
window.bind('<Right>', lambda event: keypress('right'))
window.bind('<Up>', lambda event: keypress('up'))
window.bind('<Down>', lambda event: keypress('down'))


# Game classes
class Pixel:

    def __init__(self, x, y):
        x = min(x, GRID_SIZE - 1)
        y = min(y, GRID_SIZE - 1)

        if x < 0: x = 0
        if y < 0: y = 0

        self.x = math.floor(x)
        self.y = math.floor(y)

    def render(self, color):
        x = self.x * SCALE + self.x
        y = self.y * SCALE + self.y
        canvas.create_rectangle(x, y, x + SCALE, y + SCALE, fill=color, width=0)

    def equals(self, pixel):
        return pixel.x == self.x and pixel.y == self.y


class Border:

    def __init__(self, size):
        borderPixels = []

        for i in range(size):
            # Border in width
            borderPixels.append(Pixel(i, 0))
            borderPixels.append(Pixel(i, size))

            # Border in height
            if i == 0 or i == size - 1: continue
            borderPixels.append(Pixel(0, i))
            borderPixels.append(Pixel(size, i))

        self.borderPixels = borderPixels

    def render(self, color):
        for p in self.borderPixels:
            p.render(color)

    def contains(self, pixel):
        for p in self.borderPixels:
            if p.equals(pixel): return True

        return False


class Snake:

    def __init__(self, size):
        self.bodyPixels = []

        self.headPixel = Pixel(GRID_SIZE / 2 + (size / 2), GRID_SIZE / 2 - 1)
        # for (int i = size - 1; i > 0; i--):
        for i in reversed(range(1, size)):
            self.bodyPixels.append(Pixel(self.headPixel.x - i, self.headPixel.y))

    def render(self, headColor, bodyColor):
        self.headPixel.render(headColor)

        for p in self.bodyPixels:
            p.render(bodyColor)

    def move(self, direction):
        x = self.headPixel.x
        y = self.headPixel.y

        if direction == self.Direction.Up: y -= 1
        elif direction == self.Direction.Right: x += 1
        elif direction == self.Direction.Down: y += 1
        elif direction == self.Direction.Left: x -= 1

        newHead = Pixel(x, y)
        if snake.contains(newHead): return False
        if border.contains(newHead): return False

        self.bodyPixels.append(self.headPixel)
        del self.bodyPixels[0]
        self.headPixel = newHead
        return True

    def grow(self):
        newBody = Pixel(self.bodyPixels[0].x, self.bodyPixels[0].y)
        self.bodyPixels.insert(0, newBody)

    def getSize(self):
        return len(self.bodyPixels) + 1

    def contains(self, pixel):
        if self.headPixel.equals(pixel): return True

        for p in self.bodyPixels:
            if p.equals(pixel): return True

        return False

    class Direction(Enum):
        Up = 0
        Down = 1
        Left = 2
        Right = 3


class Berry:

    def __init__(self, snake):
        while True:
            self.position = Pixel(random.randrange(1, GRID_SIZE - 1), random.randrange(1, GRID_SIZE - 1))

            if not snake.contains(self.position): break

    def render(self, color):
        self.position.render(color)



# Game functions
def start():
    setup()
    render()
    tick()


def setup():
    global border, snake, berry, direction, newDirection

    border = Border(GRID_SIZE)
    snake = Snake(SNAKE_SIZE)
    berry = Berry(snake)
    direction = Snake.Direction.Right
    newDirection = direction


def render():
    global border, snake, berry

    # Clear screen
    canvas.delete("all")

    # Game over screen
    if (gameOver):
        scale = (int) (SCALE * 1.3)
        score = snake.getSize() - SNAKE_SIZE

        canvas.create_text(SIZE / 2, SIZE / 2 - (scale * 2), fill=Colors.GameOver, text="Game over!", font=("Arial", scale, "bold"), anchor="center")
        canvas.create_text(SIZE / 2, SIZE / 2 - (scale / 1.5), fill=Colors.ScoreNumber, text=f"Score: {score}", font=("Arial", scale, "bold"), anchor="center")
        canvas.create_text(SIZE / 2, SIZE / 2 - (scale / 1.5), fill=Colors.Score, text=f"Score: {' ' * (len(str(score)) * 2)}", font=("Arial", scale, "bold"), anchor="center")

        border.render(Colors.Border)
        return


    # render everything
    snake.render(Colors.SnakeHead, Colors.SnakeBody)
    berry.render(Colors.Berry)
    border.render(Colors.Border)


def tick():
    global border, snake, berry, gameOver, direction, newDirection

    direction = newDirection

    # Move snake and check if it actually moved
    if not snake.move(direction):
        # Game over
        gameOver = True
        render()
        return

    # Check if snake got the berry
    if snake.contains(berry.position):
        berry = Berry(snake)
        snake.grow()


    # render everything to user
    render()
    window.after(TICK_TIME, tick)


def keypress(key):
    global direction, newDirection

    match (key):
        case "up":
            if (direction == Snake.Direction.Down): return
            newDirection = Snake.Direction.Up
        case "down":
            if (direction == Snake.Direction.Up): return
            newDirection = Snake.Direction.Down
        case "left":
            if (direction == Snake.Direction.Right): return
            newDirection = Snake.Direction.Left
        case "right":
            if (direction == Snake.Direction.Left): return
            newDirection = Snake.Direction.Right



start()


window.mainloop()
