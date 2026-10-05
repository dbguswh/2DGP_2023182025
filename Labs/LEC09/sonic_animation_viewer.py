"""Sonic 스프라이트 시트의 애니메이션을 재생하는 뷰어."""

from pathlib import Path

from pico2d import SDL_QUIT, clear_canvas, close_canvas, delay, get_events, load_image, open_canvas, update_canvas

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
FPS = 10
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0
SPRITE_PATH = Path(__file__).with_name("sonic-sprite.png")


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite_image = load_image(str(SPRITE_PATH))
        running = True
        while running:
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False

            clear_canvas()
            update_canvas()
            delay(0.01)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
