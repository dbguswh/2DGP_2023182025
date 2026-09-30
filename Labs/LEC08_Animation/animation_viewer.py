"""Drill #8: play four animations from the supplied sprite sheet."""

from dataclasses import dataclass
from pathlib import Path

from pico2d import close_canvas, load_image, open_canvas


SHEET_PATH = Path(__file__).with_name("sprite_sheet.png")
SHEET_HEIGHT = 10933


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


def main():
    open_canvas(800, 600)
    load_image(str(SHEET_PATH))
    close_canvas()


if __name__ == "__main__":
    main()
