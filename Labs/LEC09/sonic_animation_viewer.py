"""Sonic 스프라이트 시트의 애니메이션을 재생하는 뷰어."""

from pathlib import Path

from pico2d import SDL_KEYDOWN, SDL_QUIT, SDLK_ESCAPE, clear_canvas, close_canvas, delay, get_events, get_time, load_image, open_canvas, update_canvas

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
FPS = 10
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0
DISPLAY_SCALE = 4
FRAME_SECONDS = 1 / FPS
SPRITE_PATH = Path(__file__).with_name("sonic-sprite.png")

# 프레임 좌표는 pico2d의 좌하단 원점 기준 (x, y, 너비, 높이).
SEQUENCES = (
    ("기본 자세·걷기", (
        (1, 447, 29, 39), (31, 447, 26, 38), (58, 447, 28, 39),
        (86, 447, 30, 38), (118, 447, 30, 38), (150, 447, 30, 38),
        (182, 447, 29, 38), (211, 448, 29, 38), (240, 448, 29, 38),
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
    ("몸 말기", (
        (1, 326, 29, 30), (35, 327, 29, 31), (67, 327, 30, 29),
        (98, 327, 31, 29), (131, 327, 29, 30), (162, 326, 29, 31),
        (193, 326, 30, 29), (230, 326, 31, 29),
    )),
    ("공 회전", (
        (268, 325, 30, 30), (1, 292, 30, 27), (36, 292, 29, 27),
        (70, 292, 29, 27), (105, 292, 29, 27), (139, 292, 29, 27),
        (174, 292, 29, 27),
    )),
    ("대시 동작 A", (
        (1, 251, 29, 35), (36, 251, 30, 35), (74, 251, 31, 35),
        (111, 251, 31, 36), (149, 251, 30, 35), (186, 251, 31, 36),
    )),
    ("대시 동작 B", (
        (1, 207, 29, 35), (36, 207, 30, 35), (72, 208, 39, 31),
        (123, 208, 39, 32), (172, 208, 39, 31), (218, 208, 38, 32),
    )),
    ("방향 전환", (
        (1, 154, 24, 45), (31, 154, 29, 44), (65, 154, 20, 44),
        (90, 155, 25, 43), (119, 155, 25, 43), (149, 154, 20, 44),
    )),
    ("공중 자세", (
        (184, 156, 40, 28), (232, 157, 39, 27),
    )),
    ("정면 달리기", (
        (1, 108, 27, 38), (31, 110, 31, 36), (64, 110, 31, 36),
        (99, 110, 33, 38), (136, 110, 32, 36), (176, 110, 33, 36),
        (217, 110, 33, 36), (254, 111, 33, 36),
    )),
    ("두 팔 든 자세", (
        (6, 71, 34, 25), (49, 71, 34, 28),
    )),
    ("마지막 자세", (
        (96, 71, 23, 27), (125, 71, 23, 27),
    )),
)

# 시퀀스 순서에 대응하는 화면 이동 속도 (x, y), 픽셀/초.
MOVE_VELOCITIES = (
    (90, 0), (180, 0), (260, 0), (0, 0),
    (160, 0), (220, 0), (280, 0), (0, 0),
    (0, -100), (0, -130), (0, 0), (0, 0),
)


def validate_sequences(image_width, image_height):
    """PRD의 프레임 수와 이미지 내부 좌표를 확인한다."""
    expected_counts = (11, 12, 6, 8, 7, 6, 6, 6, 2, 8, 2, 2)
    actual_counts = tuple(len(frames) for _, frames in SEQUENCES)
    if actual_counts != expected_counts:
        raise ValueError(f"동작별 프레임 수가 PRD와 다릅니다: {actual_counts}")
    if len(MOVE_VELOCITIES) != len(SEQUENCES):
        raise ValueError("동작별 이동 속도 목록의 길이가 다릅니다")

    used_rectangles = set()
    for name, frames in SEQUENCES:
        for rectangle in frames:
            x, y, width, height = rectangle
            if min(x, y) < 0 or min(width, height) <= 0:
                raise ValueError(f"{name}: 잘못된 프레임 영역 {rectangle}")
            if x + width > image_width or y + height > image_height:
                raise ValueError(f"{name}: 이미지 밖의 프레임 영역 {rectangle}")
            if rectangle in used_rectangles:
                raise ValueError(f"{name}: 중복된 프레임 영역 {rectangle}")
            used_rectangles.add(rectangle)


def draw_frame(image, rectangle, position=None):
    """시트에서 프레임 하나만 잘라 그린다."""
    x, y, width, height = rectangle
    scale = min(DISPLAY_SCALE, CANVAS_WIDTH / width, CANVAS_HEIGHT / height)
    if position is None:
        position = (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
    image.clip_draw(
        x, y, width, height,
        *position,
        width * scale, height * scale,
    )


class Playback:
    def __init__(self):
        self.sequence_index = 0
        self.frame_index = 0
        self.completed_loops = 0
        self.phase = "playing"
        self.elapsed = 0.0

    @property
    def current_frame(self):
        return SEQUENCES[self.sequence_index][1][self.frame_index]

    @property
    def current_position(self):
        velocity_x, velocity_y = MOVE_VELOCITIES[self.sequence_index]
        center_x, center_y = CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2
        if velocity_x == velocity_y == 0:
            return center_x, center_y

        frames = SEQUENCES[self.sequence_index][1]
        frame_count = len(frames)
        if self.phase == "waiting":
            moving_seconds = REPEAT_COUNT * frame_count * FRAME_SECONDS
        else:
            moving_seconds = (
                (self.completed_loops * frame_count + self.frame_index)
                * FRAME_SECONDS + self.elapsed
            )

        half_width = max(frame[2] for frame in frames) * DISPLAY_SCALE / 2
        half_height = max(frame[3] for frame in frames) * DISPLAY_SCALE / 2
        x = center_x + velocity_x * moving_seconds
        y = center_y + velocity_y * moving_seconds
        if velocity_x:
            x = (x + half_width) % (CANVAS_WIDTH + 2 * half_width) - half_width
        if velocity_y:
            y = (y + half_height) % (CANVAS_HEIGHT + 2 * half_height) - half_height
        return x, y

    def update(self, delta_seconds):
        self.elapsed += max(0.0, delta_seconds)
        while True:
            if self.phase == "playing":
                if self.elapsed + 1e-9 < FRAME_SECONDS:
                    break
                self.elapsed = max(0.0, self.elapsed - FRAME_SECONDS)
                if self.elapsed < 1e-9:
                    self.elapsed = 0.0
                last_frame = len(SEQUENCES[self.sequence_index][1]) - 1
                if self.frame_index < last_frame:
                    self.frame_index += 1
                else:
                    self.completed_loops += 1
                    if self.completed_loops < REPEAT_COUNT:
                        self.frame_index = 0
                    else:
                        self.phase = "waiting"
            elif self.phase == "waiting":
                if self.elapsed + 1e-9 < PAUSE_SECONDS:
                    break
                self.elapsed = max(0.0, self.elapsed - PAUSE_SECONDS)
                if self.elapsed < 1e-9:
                    self.elapsed = 0.0
                self.sequence_index = (self.sequence_index + 1) % len(SEQUENCES)
                self.frame_index = 0
                self.completed_loops = 0
                self.phase = "playing"
            else:
                raise RuntimeError(f"알 수 없는 재생 상태: {self.phase}")


def main():
    if not SPRITE_PATH.is_file():
        raise FileNotFoundError(f"스프라이트 이미지를 찾을 수 없습니다: {SPRITE_PATH}")

    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite_image = load_image(str(SPRITE_PATH))
        validate_sequences(sprite_image.w, sprite_image.h)
        playback = Playback()
        last_time = get_time()
        running = True
        while running:
            for event in get_events():
                if event.type == SDL_QUIT or (
                    event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
                ):
                    running = False
            if not running:
                break

            now = get_time()
            playback.update(now - last_time)
            last_time = now
            clear_canvas()
            draw_frame(sprite_image, playback.current_frame, playback.current_position)
            update_canvas()
            delay(0.01)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
