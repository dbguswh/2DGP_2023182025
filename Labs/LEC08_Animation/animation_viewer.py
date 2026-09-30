"""Drill #8: play four animations from the supplied sprite sheet."""

from dataclasses import dataclass
from pathlib import Path

from pico2d import clear_canvas, close_canvas, delay, load_image, open_canvas, update_canvas


SHEET_PATH = Path(__file__).with_name("sprite_sheet.png")
SHEET_WIDTH = 3840
SHEET_HEIGHT = 10933
DISPLAY_HEIGHT = 500
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0


@dataclass(frozen=True)
class Frame:
    left: int
    bottom: int
    width: int
    height: int


@dataclass(frozen=True)
class Animation:
    name: str
    frames: tuple[Frame, ...]
    fps: int


def frames_from_edges(x_edges: tuple[int, ...], top: int, bottom: int) -> tuple[Frame, ...]:
    """Convert top-left image coordinates to pico2d bottom-left rectangles."""
    return tuple(
        Frame(left, SHEET_HEIGHT - bottom, right - left, bottom - top)
        for left, right in zip(x_edges, x_edges[1:])
    )


# Original sheet coordinates: top-left origin, unevenly sized frames.
IDLE = Animation(
    "Idle",
    frames_from_edges((1, 292, 599, 896, 1213, 1539, 1856), 54, 402),
    8,
)


WALK = Animation(
    "Walk",
    frames_from_edges(
        (1, 246, 425, 605, 788, 977, 1121, 1231, 1342, 1476, 1643, 1768, 1879, 2023),
        1511,
        1825,
    ),
    10,
)


RUN = Animation(
    "Run",
    frames_from_edges((1, 256, 507, 761, 974, 1210, 1479, 1735, 1964, 2178), 1865, 2138),
    14,
)


JUMP = Animation(
    "Jump",
    frames_from_edges(
        (1252, 1438, 1613, 1830, 2041, 2221, 2367, 2524, 2703, 2908, 3065, 3216, 3370, 3592, 3763),
        1165,
        1510,
    ),
    12,
)

ANIMATIONS = (IDLE, WALK, RUN, JUMP)


def validate_animations(animations: tuple[Animation, ...]) -> None:
    for animation in animations:
        if not animation.frames or animation.fps <= 0:
            raise ValueError(f"Invalid animation: {animation.name}")
        for frame in animation.frames:
            if (
                frame.left < 0
                or frame.bottom < 0
                or frame.width <= 0
                or frame.height <= 0
                or frame.left + frame.width > SHEET_WIDTH
                or frame.bottom + frame.height > SHEET_HEIGHT
            ):
                raise ValueError(f"Frame outside sprite sheet: {animation.name} {frame}")


def draw_frame(image, frame: Frame) -> None:
    clear_canvas()
    display_width = round(frame.width * DISPLAY_HEIGHT / frame.height)
    image.clip_draw(
        frame.left, frame.bottom, frame.width, frame.height,
        400, 300, display_width, DISPLAY_HEIGHT,
    )
    update_canvas()


def play_animation_once(image, animation: Animation) -> None:
    for frame in animation.frames:
        draw_frame(image, frame)
        delay(1.0 / animation.fps)


def play_animation(image, animation: Animation) -> None:
    for _ in range(REPEAT_COUNT):
        play_animation_once(image, animation)
    # Keep the final frame visible during the pause.
    delay(PAUSE_SECONDS)


def main():
    validate_animations(ANIMATIONS)
    open_canvas(800, 600)
    image = load_image(str(SHEET_PATH))
    while True:
        for animation in ANIMATIONS:
            play_animation(image, animation)
    close_canvas()


if __name__ == "__main__":
    main()
