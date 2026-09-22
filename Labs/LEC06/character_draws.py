# 실습 과제 진행
from pico2d import *
import math

open_canvas(800, 600)

character = load_image('character.png')

centerx = 400
centery = 300
radius = 200
angle = 0

def move_circle():
    print("CIRCLE")
    global angle
    angle = 0
    while angle < math.pi * 2:
        clear_canvas()
        x = centerx + radius * math.cos(angle)
        y = centery + radius * math.sin(angle)
        character.draw(x, y)
        update_canvas()

        angle += 0.05
        delay(0.03)
        pass

def move_rectangle():
    print("RECTANGLE")
    x = 200
    while (x <= 600):
        clear_canvas()
        character.draw(x, 150)
        update_canvas()
        x += 2
        delay(0.01)

    y = 150
    while (y <= 450):
        clear_canvas()
        character.draw(600, y)
        update_canvas()
        y += 2
        delay(0.01)

    x = 600
    while (x >= 200):
        clear_canvas()
        character.draw(x, 450)
        update_canvas()
        x -= 2
        delay(0.01)

    y = 450
    while (y >= 150):
        clear_canvas()
        character.draw(200, y)
        update_canvas()
        y -= 2
        delay(0.01)
    pass

def move_triangle():
    print("TRIANGLE")

    x = 200
    while (x <= 600):
        clear_canvas()
        character.draw(x, 150)
        update_canvas()
        x += 2
        delay(0.01)

    x = 600
    y = 150
    while (x >= 400):
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        x -= 2
        y += 3
        delay(0.01)

    x = 400
    y = 450
    while (x >= 200):
        pass
    pass

while (True):
    move_circle()
    move_rectangle()
    move_triangle()
    pass

close_canvas()