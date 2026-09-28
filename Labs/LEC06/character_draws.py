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

        clear_canvas()
        character.draw(centerX, centerY)
        update_canvas()
    
    pass

def move_rectangle():
    print("RECTANGLE")
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