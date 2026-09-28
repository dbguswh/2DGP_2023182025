import math
from pathlib import Path
from pico2d import *

open_canvas(800, 600)

image_path = Path(__file__).resolve().parent / "character.png"
character = load_image(str(image_path))


def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)


def move_circle():
    for degree in range(360):
        angle = math.radians(degree)
        x = 400 + 200 * math.cos(angle)
        y = 300 + 200 * math.sin(angle)
        draw_character(x, y)


def move_line(start, end):
    start_x, start_y = start
    end_x, end_y = end

    distance = math.hypot(end_x - start_x, end_y - start_y)
    steps = max(1, round(distance / 5))

    for i in range(steps + 1):
        ratio = i / steps
        x = start_x + (end_x - start_x) * ratio
        y = start_y + (end_y - start_y) * ratio
        draw_character(x, y)


def move_rectangle():
    points = [
        (50, 550),
        (745, 550),
        (745, 50),
        (50, 50),
        (50, 550),
    ]

    for i in range(len(points) - 1):
        move_line(points[i], points[i + 1])


def move_triangle():
    points = [
        (50, 550),
        (745, 550),
        (400, 50),
        (50, 550),
    ]

    for i in range(len(points) - 1):
        move_line(points[i], points[i + 1])


try:
    while True:
        move_circle()
        move_rectangle()
        move_triangle()
finally:
    close_canvas()