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
    pass

def move_triangle():
    print("TRIANGLE")
    pass

while (True):
    move_circle()
    move_rectangle()
    move_triangle()
    pass

close_canvas()