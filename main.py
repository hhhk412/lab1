import tkinter as tk
import random

WIDTH = 900
HEIGHT = 600

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

STAR_COUNT = 250

root = tk.Tk()
root.title("Полёт через звёздное поле")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="black",
    highlightthickness=0
)
canvas.pack()

colors = ["white", "#87CEFA", "#FFD700", "#FFB6C1", "#9370DB"]

stars = []

speed = 3
direction_x = 0
direction_y = 0


def create_star():
    return {
        "x": random.uniform(-WIDTH / 2, WIDTH / 2),
        "y": random.uniform(-HEIGHT / 2, HEIGHT / 2),
        "z": random.uniform(1, 1000),
        "color": random.choice(colors)
    }


for i in range(STAR_COUNT):
    stars.append(create_star())


def move_mouse(event):
    global direction_x, direction_y

    direction_x = (event.x - CENTER_X) / CENTER_X
    direction_y = (event.y - CENTER_Y) / CENTER_Y


def change_speed(event):
    global speed

    if event.keysym == "Up":
        speed = min(speed + 1, 20)

    elif event.keysym == "Down":
        speed = max(speed - 1, 1)


def draw_stars():
    canvas.delete("all")

    for star in stars:
        star["z"] -= speed

        star["x"] -= direction_x * speed * 0.5
        star["y"] -= direction_y * speed * 0.5

        if star["z"] <= 1:
            star.update(create_star())
            continue

        scale = 300 / star["z"]

        x = CENTER_X + star["x"] * scale
        y = CENTER_Y + star["y"] * scale

        size = max(1, 5 * scale)

        if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
            star.update(create_star())
            continue

        canvas.create_oval(
            x - size,
            y - size,
            x + size,
            y + size,
            fill=star["color"],
            outline=""
        )

    canvas.create_text(
        15, 15,
        anchor="nw",
        text=f"Скорость: {speed}",
        fill="white",
        font=("Arial", 12)
    )

    canvas.create_text(
        15, 40,
        anchor="nw",
        text="Стрелка вверх — ускорение | Стрелка вниз — замедление",
        fill="white",
        font=("Arial", 10)
    )

    canvas.create_text(
        15, 60,
        anchor="nw",
        text="Перемещай мышь, чтобы менять направление",
        fill="white",
        font=("Arial", 10)
    )

    root.after(30, draw_stars)


canvas.bind("<Motion>", move_mouse)
root.bind("<KeyPress>", change_speed)

draw_stars()

root.mainloop()
