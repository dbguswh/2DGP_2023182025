"""Sonic 스프라이트 시트의 애니메이션을 재생하는 뷰어."""

from pathlib import Path

from pico2d import SDL_QUIT, clear_canvas, close_canvas, delay, get_events, load_image, open_canvas, update_canvas

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
FPS = 10
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0
SPRITE_PATH = Path(__file__).with_name("sonic-sprite.png")

# 프레임 좌표는 pico2d의 좌하단 원점 기준 (x, y, 너비, 높이).
SEQUENCES = (
    ("기본 자세·걷기", (
        (1, 447, 29, 39), (31, 447, 26, 38), (58, 447, 29, 39),
        (87, 447, 29, 38), (118, 447, 30, 38), (150, 447, 30, 38),
        (182, 447, 30, 38), (212, 448, 28, 38), (240, 448, 29, 38),
        (270, 448, 24, 32), (302, 448, 29, 26),
    )),
    ("달리기", (
        (8, 408, 26, 37), (37, 408, 27, 37), (65, 407, 31, 38),
        (97, 408, 37, 37), (135, 410, 32, 35), (170, 408, 32, 38),
        (206, 408, 26, 38), (238, 408, 24, 37), (263, 408, 30, 37),
        (295, 408, 36, 37), (334, 409, 32, 36), (370, 408, 29, 38),
    )),
    ("빠른 달리기", (
        (1, 361, 33, 40), (39, 362, 35, 39), (89, 362, 35, 38),
        (130, 362, 34, 42), (181, 362, 34, 41), (228, 363, 33, 40),
    )),
)


def main():
    if not SPRITE_PATH.is_file():
        raise FileNotFoundError(f"스프라이트 이미지를 찾을 수 없습니다: {SPRITE_PATH}")

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
