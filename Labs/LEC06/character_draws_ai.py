from pico2d import *
import math

open_canvas(800, 600)
character = load_image('character.png')


def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)


def move_circle():
    center_x = 400
    center_y = 300
    radius = 200

    for degree in range(360):
        angle = math.radians(degree)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        draw_character(x, y)


def move_line(start_x, start_y, end_x, end_y, steps=200):
    for i in range(steps):
        ratio = i / steps
        x = start_x + (end_x - start_x) * ratio
        y = start_y + (end_y - start_y) * ratio
        draw_character(x, y)


def move_square():
    move_line(200, 150, 600, 150)
    move_line(600, 150, 600, 450)
    move_line(600, 450, 200, 450)
    move_line(200, 450, 200, 150)


def move_triangle():
    move_line(200, 150, 600, 150)
    move_line(600, 150, 400, 500)
    move_line(400, 500, 200, 150)


while True:
    move_circle()
    move_square()
    move_triangle()