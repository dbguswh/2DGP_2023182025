# 실습 과제 진행
import math
from pico2d import *

open_canvas(800, 600)

character = load_image('character.png')

def move_circle():
    print("CIRCLE")

    centerX = 400
    centerY = 300
    radius = 200

    for degree in range(360):
        theta = math.radians(degree)

        x = centerX + radius * math.cos(theta)
        y = centerY + radius * math.sin(theta)

        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.01)
        
    
    pass

def move_top():
    print("top")
    for x in range(50, 750, 5):
        draw_character(x, 550)

def move_right():
    print("right")
    for y in range(550, 49, -5):
        draw_character(745, y)

def move_bottom():
    print("bottom")
    for x in range(745, 49, -5):
        draw_character(x, 50)

def move_left():
    print("left")
    for y in range(50, 551, 5):
        draw_character(50, y)


def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)

def move_rectangle():
    print("RECTANGLE")
    move_top()
    move_right()
    move_bottom()
    move_left()
    pass

def move_triangle_side1():
    print("triangle side 1")
    for x in range(50, 750, 5):
        draw_character(x, 550)

def move_triangle():
    print("TRIANGLE")
    pass

while (True):
    move_circle()
    move_rectangle()
    move_triangle()
    pass

close_canvas()